from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # Добавили DeclarativeBase
from typing import AsyncGenerator
import os

# --- Современный способ объявления Base ---
class Base(DeclarativeBase):
    pass

# --- DATABASE_URL ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@orders_db:5432/orders_db"
)

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
