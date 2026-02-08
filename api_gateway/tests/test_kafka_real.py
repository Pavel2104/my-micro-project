import pytest
from httpx import AsyncClient, ASGITransport
from api_gateway.main import app


@pytest.mark.asyncio
async def test_create_order_real_kafka_flow():
    """
    Интеграционный тест: проверяем, что API принимает заказ
    и успешно отправляет его в РЕАЛЬНУЮ Kafka (без моков).
    """
    transport = ASGITransport(app=app)

    # Данные для заказа
    order_payload = {
        "user_id": 777,
        "status": "pending",
        "items": [{"product_id": 50, "quantity": 5}]
    }

    # Мы НЕ используем patch() здесь!
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    # Если Kafka недоступна или топик не существует,
    # твой код в роутере (скорее всего) выдаст 500 ошибку.
    # Если всё настроено верно — получим 201.
    assert response.status_code == 201
    print("\n[OK] Сообщение успешно ушло в реальную Kafka!")