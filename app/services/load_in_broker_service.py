"""Чтение данных из файла и отправку их в брокер"""

from datetime import datetime
import asyncio

from rmq import RmqInterface


TIME_DELTA = 3000  # интервал отправки в МС


class PutDataInBroker:
    """Класс, отвечающий за чтение данных из файла и отправку их в брокер"""

    def __init__(self, rmq_interface: RmqInterface, time_delta: int = TIME_DELTA):
        self.rmq_interface = rmq_interface
        self.time_delta = time_delta

    async def _send_message(self, message):
        await self.rmq_interface.send(
            message
        )

    async def _format_message(self, message_text: str):
        """формирует текст сообщения для брокера"""

        message = {
            "datetime": datetime.now().strftime("%Y.%m.%d %h:%m:%s.%f"),
            "title": "Very fun book",
            "text": message_text,
        }

        return message

    async def put_message_in_broker(self, title: str, text: str) -> None:
        message = {
            "datetime": datetime.now().strftime("%Y.%m.%d %h:%m:%s.%f"),
            "title": title,
            "text": text,
        }

        self._send_message(message)

    async def process_text(self, title: str, text: str):
        """обрабатывает текст, отправляя построчно в брокер"""

        lines = text.split('\n')

        for line in lines:
            asyncio.sleep()
            self.put_message_in_broker(title=title, text=line)
