import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from config import settings
from database import AsyncSessionLocal
from models import Order

# Настроим логирование, чтобы видеть что происходит в Docker logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume_orders():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_ORDER_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="order-service",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    logger.info(f"🚀 Kafka consumer started on topic: {settings.KAFKA_ORDER_TOPIC}")

    try:
        async for msg in consumer:
            event = msg.value
            logger.info(f"📥 Received event from Kafka: {event}")

            try:
                # Открываем сессию с базой
                async with AsyncSessionLocal() as session:
                    # Создаем объект заказа на основе данных из Kafka
                    # Поля: user_id, status (мы привели их к согласию со шлюзом)
                    new_order = Order(
                        user_id=event.get("user_id"),
                        status=event.get("status", "pending").upper(),
                        total_amount=0.0  # Пока заглушка, можно расширить позже
                    )

                    session.add(new_order)

                    # Фиксируем изменения в PostgreSQL
                    await session.commit()

                    # Обновляем объект, чтобы получить сгенерированный базой ID
                    await session.refresh(new_order)

                    logger.info(f"✅ SUCCESS: Order saved to DB with ID: {new_order.id}")

            except Exception as e:
                logger.error(f"❌ DATABASE ERROR: Could not save order: {e}")
                # Здесь можно добавить логику retry (повтора), если база временно недоступна

    except Exception as e:
        logger.error(f"❌ KAFKA ERROR: Consumer loop crashed: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped")


if __name__ == "__main__":
    asyncio.run(consume_orders())