"""Описывает пути к концевым точкам для фронта"""

from fastapi import APIRouter

from app.api.endpoints import (
    load_data,
    get_data,
)

router = APIRouter(prefix="/api", tags=["api"])
router.include_router(load_data.router)
router.include_router(get_data.router)
