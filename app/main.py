from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core.settings import settings
from app.api.routes import router as api_router


def get_application() -> FastAPI:
    sentry_sdk.init(dsn=settings.sentry_dsn)

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(SentryAsgiMiddleware)
    application.include_router(api_router)

    return application


app = get_application()
