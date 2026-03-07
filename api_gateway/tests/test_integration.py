import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from api_gateway.main import app
from order_service.models import Order
import os

CI = os.getenv("CI") == "true"

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.mark.asyncio
@pytest.mark.skipif(CI, reason="Kafka integration skipped on CI if real Kafka is unavailable")
async def test_e2e_order_creation_flow(monkeypatch):
    try:
        from api_gateway import kafka_producer

        async def fake_send_order_event(order_data):
            print(f"⚡ Kafka event skipped in test: {order_data}")
            return

        monkeypatch.setattr(kafka_producer, "send_order_event", fake_send_order_event)

    except ImportError:
        pass

    transport = ASGITransport(app=app)

    order_payload = {
        "user_id": 999,
        "status": "pending",
        "items": [{"product_id": 10, "quantity": 1}]
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201

    async with AsyncSessionLocal() as session:
        stmt = select(Order).where(Order.user_id == 999)
        result = await session.execute(stmt)
        db_order = result.scalars().first()

        assert db_order is not None
        assert db_order.user_id == 999
        print(f"\n✅ Интеграция прошла успешно! Заказ ID {db_order.id} найден в БД.")





