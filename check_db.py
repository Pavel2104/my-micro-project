import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/orders_db"

engine = create_async_engine(DATABASE_URL, echo=True)

async def test():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        row = result.fetchone()
        print(f"Result: {row[0]}")

if __name__ == "__main__":
    asyncio.run(test())



