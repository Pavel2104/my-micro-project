import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Загружаем .env только если он есть
load_dotenv()

# Определяем DATABASE_URL
# Если переменная окружения уже установлена (например в Docker), берем её
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # fallback на локальный .env
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/orders_db"

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

async def test():
    async with engine.begin() as conn:
        # Выполняем тестовый запрос
        result = await conn.execute(text("SELECT 1"))
        row = result.fetchone()  # Для asyncpg через SQLAlchemy fetchone() работает синхронно
        print(f"Result: {row[0]}")  # Ожидаем 1

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(test())



