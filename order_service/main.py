from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from config import settings

# Добавили send_order_event в импорт ниже:
from kafka_producer import init_kafka, send_order_event, close_kafka
from kafka_consumer import consume_orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Запуск Продюсера для отправки сообщений
    await init_kafka()

    # 2. Запуск Консьюмера в фоновой задаче для чтения сообщений
    consumer_task = asyncio.create_task(consume_orders())
    print("Background Kafka Consumer task started")

    yield

    # 3. Чистое завершение работы
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print("Consumer task cancelled")
    await close_kafka()


app = FastAPI(title="Order Service", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {
        "service": settings.SERVICE_NAME,
        "status": "ok",
        "timestamp": datetime.now(timezone.utc)
    }


@app.get("/orders/status/{order_id}")
async def get_order_status(order_id: int):
    # Теперь эта функция будет работать, так как она импортирована выше
    status = "CREATED"
    await send_order_event(order_id, status)
    return {"order_id": order_id, "status": status}

