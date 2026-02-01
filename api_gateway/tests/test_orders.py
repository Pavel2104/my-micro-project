import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from main import app

@pytest.mark.asyncio
async def test_api_is_alive():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/orders/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_order_success():
    transport = ASGITransport(app=app)

    with patch("api_gateway.kafka_producer.send_order_event", new_callable=AsyncMock) as mock_kafka:
        mock_kafka.return_value = True

        order_payload = {
            "user_id": 1,
            "status": "pending",
            "items": [{"product_id": 10, "quantity": 2}]
        }

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/orders/", json=order_payload)

        assert response.status_code == 201
        assert mock_kafka.called

        # Проверяем данные, ушедшие в мок Kafka
        args, kwargs = mock_kafka.call_args
        sent_data = args[0] if args and isinstance(args[0], dict) else kwargs

        assert sent_data["user_id"] == 1
        assert sent_data["items"][0]["product_id"] == 10
        print("\nУра! Данные в Kafka проверены.")

@pytest.mark.asyncio
async def test_create_order_validation_error():
    transport = ASGITransport(app=app)
    # Ошибка: items не список
    invalid_payload = {"user_id": 1, "items": "not-a-list"}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=invalid_payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_order_kafka_failure():
    """
    НОВЫЙ ТЕСТ: Проверяем, что API возвращает 500 ошибку,
    если брокер сообщений (Kafka) внезапно 'упал'.
    """
    transport = ASGITransport(app=app)

    # Имитируем жесткий сбой Kafka через side_effect
    with patch("api_gateway.kafka_producer.send_order_event", side_effect=Exception("Kafka connection error")):
        order_payload = {
            "user_id": 1,
            "status": "pending",
            "items": [{"product_id": 10, "quantity": 2}]
        }

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/orders/", json=order_payload)

        # Ожидаем, что сервер не упадет с ошибкой Python,
        # а вернет корректный HTTP 500
        assert response.status_code == 500
        # Если твой роутер пробрасывает описание ошибки, можно проверить и текст:
        # assert "Kafka connection error" in response.text








