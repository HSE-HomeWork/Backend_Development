"""Тут находится основной файл приложения."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.router import router as main_router
from app.exception_handlers import validation_exception_handler


def create_app() -> FastAPI:
    """Создает экземпляр проекта FastAPI."""
    app = FastAPI()

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.include_router(main_router)
    return app


app = create_app()
