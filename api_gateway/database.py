from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator
import os
from dotenv import load_dotenv  # для локальной работы через .env

# --- Загружаем .env (локально) ---
load_dotenv()

# --- Современный способ объявления Base ---
class Base(DeclarativeBase):
    pass

# --- DATABASE_URL ---
# Обязательная переменная окружения
DATABASE_URL = os.environ["DATABASE_URL"]

# --- Асинхронный движок ---
engine = create_async_engine(DATABASE_URL, echo=True)

# --- sessionmaker ---
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# --- генератор для FastAPI ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

