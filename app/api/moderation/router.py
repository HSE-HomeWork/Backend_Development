"""Роутинг приложения пользователей."""

from fastapi import APIRouter

from app.schemas.moderation import AnnoncePredict
from app.service import moderation as moderation_service

router = APIRouter()


@router.post("/predict")
async def predict(user_in: AnnoncePredict) -> bool:
    """Предсказание для юзера."""
    return await moderation_service.predict(
        verify=user_in.is_verified_seller,
        image_number=user_in.images_qty,
    )
