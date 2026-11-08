"""Сервисный слой для модерации."""


async def predict(verify: bool, image_number: int) -> bool:
    """Определяет, допустимо ли объявление."""
    return verify or image_number > 0
