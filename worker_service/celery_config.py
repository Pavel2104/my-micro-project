# Простая конфигурация брокера и backend для Redis через переменные окружения.
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
RESULT_BACKEND = BROKER_URL

# Дополнительные опции Celery (необязательно)
CELERY_CONFIG = {
    "broker_url": BROKER_URL,
    "result_backend": RESULT_BACKEND,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "task_track_started": True,
    "worker_send_task_events": True,
    "result_expires": 3600,  # секунды
}
