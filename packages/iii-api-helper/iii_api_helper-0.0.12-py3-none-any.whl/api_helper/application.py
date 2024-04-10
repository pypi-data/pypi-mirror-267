from collections.abc import Callable
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import uvicorn
from fastapi import FastAPI as FastAPIBase
from starlette.middleware import Middleware
from typing_extensions import Self
from uvicorn._types import ASGIApplication

from . import config
from .config import LoggerBuilder
from .errors import FastAPIError
from .errors.app_error import ApplicationError
from .errors.app_error import handle_application_error
from .middlewares import LogRequestMiddleware
from .sentry import sentry_init

logger: Logger = getLogger(__name__)


class FastAPI(FastAPIBase):
    def __init__(
        self: Self,
        *,
        base_folder: Path,
        **extra: Any,
    ) -> None:
        """

        Args:
            base_folder:
            **extra:
        """
        if not base_folder.exists():
            msg: str = "The base folder does not exist. Please provide a valid base folder."
            raise FastAPIError(msg)

        self.setup_logger(base_folder, extra.pop("log_builder", None), **extra)

        middlewares: list[Middleware] = extra.pop("middleware", [])
        middlewares.append(
            Middleware(LogRequestMiddleware),  # type: ignore
        )

        if config.is_debug() or extra.get("debug", False) is True:
            extra.pop("debug", None)
            super().__init__(
                debug=True,
                title=config.get("APP_NAME"),
                middleware=middlewares,
                **extra,
            )
        else:
            openapi_url: str | None = extra.pop("openapi_url", None)

            super().__init__(
                title=config.get("APP_NAME"),
                middleware=middlewares,
                openapi_url=openapi_url,
                **extra,
            )

        self.add_exception_handler(ApplicationError, handle_application_error)

    def setup_logger(
        self: Self,
        base_folder: Path,
        log_builder: LoggerBuilder = None,
        **extra: Any,
    ) -> None:
        if log_builder:
            _logger: LoggerBuilder = log_builder

        else:
            options: dict[str, Any] = {}

            for key in extra:
                if key == "logging_base_folder":
                    continue

                if key.startswith("logging_"):
                    options[key.replace("logging_", "")] = extra.pop(key)

            _logger: LoggerBuilder = LoggerBuilder(base_folder, **options)

        _logger.setup()

        self.LOGGING_CONFIG: dict[str, Any] = _logger.config

    if TYPE_CHECKING:
        run = uvicorn.run

    else:

        def run(
            self: Self,
            host: str = "127.0.0.1",
            port: int = 8000,
            *,
            app: ASGIApplication | Callable[..., Any] | str | None = None,
            show_swagger: bool = False,
            **kwargs: Any,
        ) -> None:
            error_message: str = ""

            if show_swagger and self.openapi_url is None:
                if self.title is None:
                    error_message = "A title must be provided for OpenAPI, e.g.: 'My API'"
                if self.version is None:
                    error_message = "A version must be provided for OpenAPI, e.g.: '2.1.0'"
                self.openapi_url = "/openapi.json"

                if error_message:
                    raise FastAPIError(error_message)

                self.setup()

            should_reload: bool = kwargs.pop("reload", config.is_reload())

            if should_reload and not isinstance(app, str):
                error_message = "The 'reload' option can only be used with 'app' as a string path to the application."
                raise FastAPIError(error_message)

            uvicorn.run(
                app or self,
                host=host,
                port=port,
                log_config=self.LOGGING_CONFIG,
                **kwargs,
            )

    setup_sentry = sentry_init
