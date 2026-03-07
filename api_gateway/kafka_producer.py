import asyncio
import json
from aiokafka import AIOKafkaProducer, errors
from api_gateway.config import settings

producer: AIOKafkaProducer | None = None
MAX_RETRIES = 5
RETRY_DELAY = 3

async def init_kafka():
    global producer
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            await producer.start()
            print("✅ Kafka producer initialized and started")
            return
        except errors.KafkaConnectionError as e:
            print(f"⚠️ Attempt {attempt} failed to connect to Kafka: {e}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)
            else:
                raise RuntimeError("Failed to connect to Kafka after multiple attempts") from e

async def send_order_event(order_data: dict):
    global producer
    if producer is None:
        print("❌ Kafka producer is None! Trying to initialize...")
        await init_kafka()

    try:
        await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_data)
        print(f"📡 Successfully sent order to {settings.KAFKA_ORDER_TOPIC}: {order_data}")
    except Exception as e:
        print(f"❌ Failed to send message to Kafka: {e}")
        raise e

async def close_kafka():
    global producer
    if producer is not None:
        await producer.stop()
        print("🛑 Kafka producer stopped")