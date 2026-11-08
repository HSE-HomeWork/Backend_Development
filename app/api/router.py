"""Роутинг всего проекта."""

from fastapi import APIRouter

from app.api.moderation.router import router as users_router

router = APIRouter()

router.include_router(users_router)
