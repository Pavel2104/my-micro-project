import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from api_gateway.main import app
from order_service.models import Order
import os

# Используем DATABASE_URL для Docker / CI
DATABASE_URL = os.environ["DATABASE_URL"]

# Асинхронный движок и сессии
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.mark.asyncio
async def test_e2e_order_creation_flow(monkeypatch):
    """
    CI-friendly версия:
    - мокаем Kafka (не используем настоящий продьюсер)
    - проверяем, что API создаёт заказ в базе
    """

    # 1. Мокаем Kafka, чтобы продьюсер не был нужен
    monkeypatch.setattr("api_gateway.kafka_producer.producer", None)

    transport = ASGITransport(app=app)

    # 2. Данные для заказа
    order_payload = {
        "user_id": 999,
        "status": "pending",
        "items": [{"product_id": 10, "quantity": 1}]
    }

    # 3. Делаем запрос к FastAPI
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201

    # 4. Проверяем базу напрямую (не через Kafka)
    async with AsyncSessionLocal() as session:
        stmt = select(Order).where(Order.user_id == 999)
        result = await session.execute(stmt)
        db_order = result.scalars().first()

        assert db_order is not None
        assert db_order.user_id == 999
        print(f"\nИнтеграция прошла успешно! Заказ ID {db_order.id} найден в БД.")

