import sys
import logging
from typing import Tuple, Dict, Any

from pydantic import BaseSettings
from loguru import logger

from app.core.logging import InterceptHandler


class AppSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Topic recommendation"
    version: str = "1.0.0"

    api_prefix: str = ""

    sentry_dsn: str = ""
    database_path: str

    server_host: str = "0.0.0.0"
    server_port: int = 8000

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = AppSettings()
