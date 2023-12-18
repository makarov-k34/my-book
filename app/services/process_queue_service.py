"""
Сервис получает исходных данные из топика брокера сообщений
вычисляет количество вхождений буквы "Х" в строках текста из поля "text"
сохраняет результат в БД
"""
import asyncio
from app.shemas.database_schemas import TextData
from app.services.rmq import RmqInterface

from app.shemas.pydantic_schemas import QueueData

from pydantic import ValidationError
from app.repository.text_data_repository import TextDataRepository


class ProcessDataFromBroker:
    """Обрабатывает очередь из брокера сообщений"""

    def __init__(self, rmq_interface: RmqInterface, time_delta_seconds: int = 3):
        self.rmq_interface = rmq_interface
        self.time_delta_seconds = time_delta_seconds
        self.entity_service = TextDataRepository(model=TextData)

    async def _process_data(self, data: QueueData) -> TextData:
        """
        вычисляет количество вхождений буквы "Х" в строках текста из поля "text",
        сохраняет результат в БД
        """

        data_to_save = TextData(
            datetime=data.datetime,
            title=data.title,
            x_avg_count_in_line=data.text.count("X"),
        )
        async with self.session as session:
            instance = await self.entity_service.create(
                session, data_to_save
            )

        return instance

    async def _process_message_from_broker(self, message) -> bool:
        """берет сообщение из брокера, обрабатывает и пишет с базу данных"""

        try:
            # валидируем сообщение из брокера
            data = QueueData(message)

            if self._process_data(data):
                return True
        except ValidationError:
            return False

        return False

    async def run(self):
        """Запуск обработки очереди"""

        while True:
            await asyncio.sleep(self.time_delta_seconds * 1000)
            await rmq_interface.consume(self._process_message_from_broker)
