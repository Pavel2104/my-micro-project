from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "order_service"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/orders_db"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_ORDER_TOPIC: str = "orders_new"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()