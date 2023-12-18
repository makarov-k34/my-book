"""
Настройки приложения.
"""

from enum import Enum
from pathlib import Path

from aio_pika import ExchangeType
from pydantic import BaseModel, validator
from typing import Any, Union

APP_DIR = Path(__file__).resolve(strict=True).parent.parent


class Environment(Enum):
    """Где запущен сервис"""

    LOCAL = "local"



class EnvironmentSettings(BaseModel):
    """
    Настройки в части окружения и локации файла с переменными окружения.
    """

    #т.к. задача тестовая, путсь будет только LOCAL
    environment: Environment = Environment.LOCAL

    class Config:
        """
        Класс-конфигуратор для определения дополнительных свойств класса
        настроек.

        Подтягивает переменные из файла, указанного в поле env_file.
        """

        env_file = f"{APP_DIR}/config/.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

    # Database engine
class PostgresConfig(EnvironmentSettings):
    """конфигурация для БД"""

    # Database engine
    DB_DIALECT: str = "postgresql"
    DB_API: str = "asyncpg"
    DB_USER: str = "mybook"
    DB_PASSWORD: str = "mybook"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_NAME: str = "mybook"

    url: str = "postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy"

    @validator("url", pre=True)
    def build_url(cls, value: Union[str,None], values: dict[str, Any]) -> Any:
        """Построение урла pgsql для реплики бд EAIS"""

        url = "{scheme}://{user}:{password}@{host}:{port}/{dbname}".format(
            scheme=f"{values['DB_DIALECT']}+{values['DB_API']}",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            dbname=values.get("DB_NAME"),  # для передачи имени бд в конструкторе
        )

        return url

class CommonSettings(EnvironmentSettings):
    """Настройки, общие для всех окружений."""

    # DEBUG
    debug: bool = True

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8888
    server_reload: bool = False
    title: str = "mybook"
    root_path: str = "/my-book"

    postgres: PostgresConfig = PostgresConfig()

    #интервал времени обработки запроса
    TIME_DELTA: int = 3000 #миллисекунд
    #настройки кролика
    RMQ_INTERFACE: dict = {
        "uri": "",
        "exchange_conf": {
            "name": "my_book",
            "durable": True,
            "type": ExchangeType.DIRECT,
        },
        "input_queue_conf": {
            "name": "my_book_queue",
            "routing_keys": ["my_book_queue"],
            "auto_delete": False,
            "durable": True,
        },
        "output_queue_conf": {
            "name": "my_book_queue",
            "routing_keys": ["my_book_queue"],
            "auto_delete": False,
            "durable": True,
        },
        "max_concurrent_messages": 20,
    }

    engine_config: dict[str, Any] = {}


settings = CommonSettings()
