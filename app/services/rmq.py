"""Класс для работы с брокером реббит"""

import copy
import aio_pika

from typing import Callable

class RmqInterface:
    """AMQP-интерфейс для работы с RabbitMQ"""

    def __init__(self):
        self.connection = None
        self.callback = None
        self._exchange = None
        self._input_queue = None
        self._input_routing_keys = None
        self._output_queue = None
        self._output_routing_key = None


    @classmethod
    async def create(
        cls,
        uri: str,
        exchange_conf: dict,
        max_concurrent_messages: int = 1,
        input_queue_conf: dict = None,
        output_queue_conf: dict = None,
    ):
        """Создает объект интерфейса для работы с реббит"""

        self = cls()
        self.callback = None

        # инициализация подключения к RMQ
        self.connection = await aio_pika.connect_robust(uri)
        # создаем канал
        channel = await self.connection.channel()
        # максимальное количество конкурентно обрабатываемых сообщений
        await channel.set_qos(prefetch_count=max_concurrent_messages)

        # объявляем точку обмена, входную очередь и связываем их
        self._exchange = await channel.declare_exchange(**exchange_conf)

        if input_queue_conf:
            input_queue_conf = copy.deepcopy(input_queue_conf)
            self._input_routing_keys = input_queue_conf.pop(
                "routing_keys", None
            )

            if input_queue_conf:
                self._input_queue = await channel.declare_queue(
                    **input_queue_conf
                )
                for input_key in self._input_routing_keys:
                    await self._input_queue.bind(
                        exchange=self._exchange, routing_key=input_key
                    )

        if output_queue_conf:
            output_queue_conf = copy.deepcopy(output_queue_conf)
            self._output_routing_key = output_queue_conf.pop(
                "routing_key", None
            )

            if output_queue_conf:
                self._output_queue = await channel.declare_queue(
                    **output_queue_conf
                )
                await self._output_queue.bind(
                    exchange=self._exchange,
                    routing_key=self._output_routing_key,
                )

        return self

    async def _process_message(self, message: aio_pika.IncomingMessage) -> None:
        """Обрабатывает сообщение"""

        async with message.process(ignore_processed=True):
            # без ignore_processed сделать nack не получится
            json_message = json.loads(message.body.decode())
            result = await self.callback(json_message)
            # при успешном выполнении callback ожидаем получить True
            if not result:
                # возвращаем сообщение обратно в очередь
                await message.nack()

    async def consume(self, callback: Callable):
        """Берет сообщение из очереди"""
        # сохраняем callback-функцию как атрибут экземпляра класса,
        # чтобы не передавать её параметрами по методам
        self.callback = callback
        # слушаем входящую очередь, запуская callback на каждое сообщение
        await self._input_queue.consume(self._process_message)



    async def send(self, message: dict) -> None:
        """Отправляет сообщение"""
        await self._exchange.publish(
            aio_pika.Message(
                json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._output_routing_key,
        )