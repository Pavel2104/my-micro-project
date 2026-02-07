import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_async_engine(DATABASE_URL, echo=True)

async def test():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        row = result.fetchone()  # <--- убрали await
        print(row)

asyncio.run(test())


