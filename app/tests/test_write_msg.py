"""Интеграционные тесты точек входа для проверки работы всей
функциональности.
"""
import pytest
from fastapi.testclient import TestClient

from main import create_app

client = TestClient(create_app(), base_url="http://testserver.ru")


def test_write_message():
    """Проверяет работу точки входа load-data"""
    response = client.get("/load-data")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_rmq():
    from app.services.rmq import RmqInterface
    from app.config.settings import settings
    rmq_interface = await RmqInterface.create(
        **settings.RMQ_INTERFACE
    )

    assert True
