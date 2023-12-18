"""Схемы для валидации данных"""
from pydantic import BaseModel


class ResponseTextData(BaseModel):
    """Схема данных, возвращаемы с бд"""

    datetime: str
    title: str
    x_avg_count_in_line: int


class QueueData(BaseModel):
    """Схема данных, получаемых из очереди"""

    datetime: str  # можно отдельно проверку формата сделать, но наверно лишнее
    title: str
    text: str
