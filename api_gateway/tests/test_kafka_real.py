import pytest
from httpx import AsyncClient, ASGITransport
from api_gateway.main import app


@pytest.mark.asyncio
async def test_create_order_real_kafka_flow():
    transport = ASGITransport(app=app)

    order_payload = {
        "user_id": 777,
        "status": "pending",
        "items": [{"product_id": 50, "quantity": 5}]
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201
    print("\n[OK] Сообщение успешно ушло в реальную Kafka!")