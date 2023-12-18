"""Инициализация подключения к базе данных."""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


class AsyncDBEngine:
    """Класс для работы с асинхронным движком БД."""

    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(url = settings.postgres.url)


    async def close_connections(self):
        """Закрывает активные соединения с БД."""
        await self.engine.dispose()


async_engine = AsyncDBEngine()

async_session = sessionmaker(
    async_engine.engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Генерирует новый объект сессии базы данных.

    По завершении работы с ним - закрывает.
    """
    async with async_session() as session:
        yield session