import asyncio
import json
from aiokafka import AIOKafkaProducer, errors
from config import settings

producer: AIOKafkaProducer | None = None
MAX_RETRIES = 5       # максимальное количество попыток
RETRY_DELAY = 3       # задержка между попытками в секундах

async def init_kafka():
    global producer
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            await producer.start()
            print("Kafka producer started")
            return
        except errors.KafkaConnectionError as e:
            print(f"Attempt {attempt} failed to connect to Kafka: {e}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)
            else:
                raise RuntimeError("Failed to connect to Kafka after multiple attempts") from e


async def send_order_event(order_id: int, status: str):
    from aiokafka import AIOKafkaProducer
    import json

    # Создаем продюсера прямо внутри функции
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.start()
    try:
        # Создаем тело сообщения
        data = {"order_id": order_id, "status": status}
        await producer.send_and_wait("orders_new", {"order_id": order_id, "status": status})
        print("Successfully sent to orders_new")
    finally:
        # Важно закрыть соединение
        await producer.stop()

async def close_kafka():
    if producer is not None:
        await producer.stop()
        print("Kafka producer stopped")