"""Обработчики исключений приложения."""

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

BAD_REQUEST = 400


async def validation_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """Обрабатывает ошибки валидации входных данных."""
    if not isinstance(exc, RequestValidationError):
        raise exc
    return JSONResponse(
        status_code=BAD_REQUEST,
        content={"detail": jsonable_encoder(exc.errors())},
    )
