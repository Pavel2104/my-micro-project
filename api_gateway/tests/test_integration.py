import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from api_gateway.main import app
from order_service.models import Order
import os

# CI-флаг
CI = os.getenv("CI") == "true"

# Используем DATABASE_URL для Docker / CI
DATABASE_URL = os.environ["DATABASE_URL"]

# Асинхронный движок и сессии
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.mark.asyncio
async def test_e2e_order_creation_flow():
    """
    CI- и локально-дружелюбный тест:
    - Не использует Kafka
    - Проверяет, что API создаёт заказ в базе
    """

    # --- Отключаем Kafka ---
    try:
        from api_gateway import kafka_producer

        # Не стартуем продьюсер
        kafka_producer.producer = None

        # Заменяем функцию отправки события на "пустышку"
        async def fake_send_order_event(order_data):
            print("⚡ Kafka event skipped in test:", order_data)

        kafka_producer.send_order_event = fake_send_order_event
    except ImportError:
        # Если файла kafka_producer.py нет, просто игнорируем
        pass

    transport = ASGITransport(app=app)

    # --- Данные для заказа ---
    order_payload = {
        "user_id": 999,
        "status": "pending",
        "items": [{"product_id": 10, "quantity": 1}]
    }

    # --- Делаем запрос к FastAPI ---
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201

    # --- Проверяем базу напрямую ---
    async with AsyncSessionLocal() as session:
        stmt = select(Order).where(Order.user_id == 999)
        result = await session.execute(stmt)
        db_order = result.scalars().first()

        assert db_order is not None
        assert db_order.user_id == 999
        print(f"\n✅ Интеграция прошла успешно! Заказ ID {db_order.id} найден в БД.")

