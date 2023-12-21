"""
Эндпоинт предоставляет  результат из БД в виде
 [
    {"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012},
    {"datetime": "18.01.2023 12:00:25.001", "title": "Other very fun book", "x_avg_count_in_line": 0.032}
] где x_avg_count_in_line
   """

from fastapi import (
    APIRouter,
)

from app.shemas.database_schemas import TextData
from app.shemas import response
from app.services.process_data_from_db_service import ProcessDataFromDatabase

router = APIRouter(prefix="/load-data")


@router.get(
    "/get-data",
    response_model=response.ResponseReturnData,
)
async def get_data():
    """Точка входа для получения сводных данных."""

    pivot_data = ProcessDataFromDatabase(model=TextData)

    return response.ResponseReturnData(data=pivot_data, is_ok=True)
