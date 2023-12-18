"""Модели исключений для http запросов"""
from fastapi import status
from pydantic import BaseModel, PydanticValueError


class ErrorModel(BaseModel):
    """Модель ошибки"""

    message: str
    detail: str = ""
