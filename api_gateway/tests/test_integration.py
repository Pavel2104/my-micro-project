import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from api_gateway.main import app
from order_service.models import Order
import os

# Используем DATABASE_URL для Docker, как в .env.local
DATABASE_URL = os.environ["DATABASE_URL"]

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.mark.asyncio
async def test_e2e_order_creation_flow():
    transport = ASGITransport(app=app)

    # 1. Данные для заказа
    order_payload = {
        "user_id": 999,
        "status": "pending",
        "items": [{"product_id": 10, "quantity": 1}]
    }

    # 2. Делаем запрос к FastAPI
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201

    # 3. Ждем обработки Kafka воркером
    await asyncio.sleep(2)

    # 4. Проверяем базу данных
    async with AsyncSessionLocal() as session:
        stmt = select(Order).where(Order.user_id == 999)
        result = await session.execute(stmt)
        db_order = result.scalars().first()

        assert db_order is not None
        assert db_order.user_id == 999
        print(f"\nИнтеграция прошла успешно! Заказ ID {db_order.id} найден в БД.")
