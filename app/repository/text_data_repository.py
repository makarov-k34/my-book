"""Модуль работы с базой данных"""

from app.shemas.database_schemas import SchemaBase
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import func


class TextDataRepository:
    """Класс по созданию/чтению сущностей из БД

    Управление сессией вынесено за пределы класса, поэтому для закрытия
    транзакций и ORM объектов необходимо использовать: db_session.close()
    """

    def __init__(self, model: SchemaBase):
        self._model = model

    async def create(
            self,
            db_session: AsyncSession,
            obj_in: SchemaBase,
    ) -> SchemaBase:
        """Делает запись объекта в БД"""

        db_session.add(obj_in)
        await db_session.commit()
        await db_session.refresh(obj_in)
        return obj_in

    async def get_multi_processed(
            self,
            db_session: AsyncSession,
    ) -> dict[list]:
        """
        Возвращает сводные данные
        в виде:
        [
            {"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012},
        ]
        """
        res = await db_session.execute(
            select(self._model.datetime,
                   self._model.title,
                   (func.sum(self._model.column) / func.count(self._model.column)).alias("x_avg_count_in_line")
                   ).group_by(self._model.title).all()
        )

        return res
