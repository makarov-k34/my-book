""""Эндпоинты для загрузки данных"""

from fastapi import (
    APIRouter,
    Request,
    UploadFile,
)

from app.shemas import response
from app.services.load_in_broker_service import PutDataInBroker

router = APIRouter(prefix="/load-data")


@router.put(
    "/load-file",
    response_model=response.ResponseOKSchema,
)
async def load_file(
        request: Request,
        file: UploadFile,
):
    """Точка входа для обновления данных на основе загруженного файла."""

    contents = await file.read()
    rmq_interface = request.app["my_book_interface"]
    await PutDataInBroker(rmq_interface=rmq_interface,
                          time_delta=request.app["settings"].TIME_DELTA,
                          ).process_text(file.filename, contents)

    return response.ResponseOKSchema(message="Текст загружен в брокер!", is_ok=True)
