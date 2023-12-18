"""
Модуль для получения результата из БД в виде
[{"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012},
{"datetime": "18.01.2023 12:00:25.001", "title": "Other very fun book", "x_avg_count_in_line": 0.032} ]
 где x_avg_count_in_line -- среднее значение количества вхождений по каждому из загруженых текстов
 """

import database_service
from app.shemas.database_schemas import TextData, SchemaBase
from app.repository.text_data_repository import TextDataRepository
from rmq import RmqInterface

from app.shemas.pydantic_schemas import QueueData

from pydantic import ValidationError

import time


class ProcessDataFromDatabase:
    """Предоставляет обработанные данные из бд"""

    def __init__(self, model: SchemaBase):
        self.time_delta_seconds = time_delta_seconds
        self.entity_service = TextDataRepository(model)

    async def get_books_data(self) -> TextData:
        """
        Вычисляет результат из БД в виде
        [{"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012},
        """

        async with self.session as session:
            pivot_data = await self.entity_service.get_pivot_data(
                session
            )

        return pivot_data