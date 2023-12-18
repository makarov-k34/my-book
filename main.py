import uvicorn
from fastapi import FastAPI

from app.db_session_maker import async_engine

from app.services.process_queue_service import ProcessDataFromBroker
from app.services.rmq import RmqInterface
from app.config.settings import settings


def create_app():
    app = FastAPI(docs_url='/')

    @app.on_event("startup")
    async def startup_event():
        rmq_interface = await RmqInterface.create(
            **settings.RMQ_INTERFACE
        )

        app["my_book_interface"] = rmq_interface
        app["settings"] = settings
        # создаем обработчик брокера сообщений при запуске, он будет реботать вне АПИ
        data_brocker_processor = ProcessDataFromBroker(rmq_interface)
        data_brocker_processor.run()


    @app.on_event("shutdown")
    async def shutdown():
        """При завершении работы сервера, закрывает соединения с БД."""
        await async_engine.close_connections()
        app["my_book_interface"] = None

    return app


def main():
    try:
        uvicorn.run(
            f"main:create_app",
            host=settings.server_host,
            port=settings.server_port,
        )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
