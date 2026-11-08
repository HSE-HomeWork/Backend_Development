"""Тесты бизнес-логики и API модерации объявлений."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.exception_handlers import BAD_REQUEST
from app.main import app
from app.service import moderation as moderation_service

Payload = dict[str, int | bool | str]

client = TestClient(app)

SUCCESSFUL_RESPONSE = 200
SERVER_ERROR = 500

VALID_PAYLOAD: Payload = {
    "seller_id": 1,
    "is_verified_seller": False,
    "item_id": 100,
    "name": "Test",
    "description": "Description",
    "category": 1,
    "images_qty": 0,
}


@pytest.mark.parametrize(
    ("verify", "images", "expected"),
    [
        (True, 0, True),
        (True, 5, True),
        (False, 0, False),
        (False, 1, True),
    ],
)
def test_predict_service(
    verify: bool,
    images: int,
    expected: bool,
) -> None:
    """Проверяет результаты бизнес-логики модерации."""
    result = asyncio.run(
        moderation_service.predict(verify, images),
    )

    assert result is expected


@pytest.mark.parametrize(
    ("verify", "images", "expected"),
    [
        (True, 0, True),
        (False, 0, False),
        (False, 3, True),
    ],
)
def test_predict_endpoint(
    monkeypatch: pytest.MonkeyPatch,
    verify: bool,
    images: int,
    expected: bool,
) -> None:
    """Проверяет HTTP-ответ и вызов сервиса модерации."""
    mock = AsyncMock(return_value=expected)
    monkeypatch.setattr(moderation_service, "predict", mock)

    payload = {
        **VALID_PAYLOAD,
        "is_verified_seller": verify,
        "images_qty": images,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == SUCCESSFUL_RESPONSE
    assert response.json() is expected
    mock.assert_awaited_once()


@pytest.mark.parametrize(
    "payload",
    [
        {**VALID_PAYLOAD, "images_qty": -1},
        {**VALID_PAYLOAD, "images_qty": "abc"},
        {
            key: value
            for key, value in VALID_PAYLOAD.items()
            if key != "category"
        },
    ],
)
def test_predict_validation(payload: Payload) -> None:
    """Проверяет валидацию входных данных API."""
    response = client.post("/predict", json=payload)

    assert response.status_code == BAD_REQUEST


def test_predict_service_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет обработку исключений бизнес-логики."""
    mock = AsyncMock(side_effect=RuntimeError("Internal error"))
    monkeypatch.setattr(moderation_service, "predict", mock)

    with TestClient(
        app, raise_server_exceptions=False
    ) as test_client:
        response = test_client.post(
            "/predict", json=VALID_PAYLOAD
        )

    assert response.status_code == SERVER_ERROR
