"""Классы для работы с бд"""
# предоставляет эндроинт для получения результата из БД в виде
# [{"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012}, {"datetime": "18.01.2023 12:00:25.001", "title": "Other very fun book", "x_avg_count_in_line": 0.032} ]
# где x_avg_count_in_line -- среднее значение количества вхождений по каждому из загруженых текстов

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

SchemaBase = declarative_base()


class TextData(SchemaBase):
    """Данные обработанной строки"""
    __tablename__ = 'TextData'

    id = Column(Integer(), primary_key=True,)
    datetime = Column(DateTime())
    title = Column(Text())
    x_count_in_line = Column(Integer())

    def __repr__(self):
        """представление данных класса"""
        return {"datetime": self.datetime, "title": self.title, "x_avg_count_in_line": self.x_avg_count_in_line},
