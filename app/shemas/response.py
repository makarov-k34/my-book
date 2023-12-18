"""Схемы ответов от апи"""
from pydantic import BaseModel


class ResponseOKSchema(BaseModel):
    """Успешный ответ"""

    message: str
    is_ok: bool

class ResponseReturnData(BaseModel):
    """Успешный ответ"""

    data: list[dict]
