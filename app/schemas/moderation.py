"""DTO для ручки /predict."""

from pydantic import BaseModel, Field


class AnnoncePredict(BaseModel):
    """Данные для предсказания."""

    seller_id: int
    is_verified_seller: bool
    item_id: int
    name: str
    description: str
    category: int
    images_qty: int = Field(ge=0)
