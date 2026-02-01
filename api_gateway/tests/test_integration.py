import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from main import app
# Импортируем модель из соседнего сервиса (убедись, что пути в Docker позволяют это)
from order_service.models import Order

# Настройка подключения к БД order_service
# Вставь сюда свои данные из docker-compose (DB_USER, DB_PASSWORD, DB_NAME)
DATABASE_URL = "postgresql://user:password@db_orders:5432/order_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@pytest.mark.asyncio
async def test_e2e_order_creation_flow():
    transport = ASGITransport(app=app)

    # 1. Данные для заказа
    order_payload = {
        "user_id": 999,  # Уникальный ID для теста
        "status": "pending",
        "items": [{"product_id": 10, "quantity": 1}]
    }

    # 2. Делаем реальный запрос (БЕЗ МОКОВ!)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/", json=order_payload)

    assert response.status_code == 201

    # 3. Ждем немного, пока Kafka передаст сообщение, а воркер его обработает
    await asyncio.sleep(2)

    # 4. Проверяем базу данных order_service
    with SessionLocal() as session:
        # Ищем заказ, который только что создали
        stmt = select(Order).where(Order.user_id == 999)
        db_order = session.execute(stmt).scalars().first()

        assert db_order is not None
        assert db_order.user_id == 999
        print(f"\nИнтеграция прошла успешно! Заказ ID {db_order.id} найден в БД.")