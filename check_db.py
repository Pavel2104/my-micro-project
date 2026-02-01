import asyncio
import database
from models import Order
from sqlalchemy import select, func

async def check():
    # Пробуем найти сессию под разными именами
    session_maker = getattr(database, 'async_session_maker', 
                    getattr(database, 'async_sessionmaker', None))
    
    if not session_maker:
        print(f'\n[ERROR] Could not find session maker in database.py. Available: {dir(database)}')
        return

    try:
        async with session_maker() as s:
            res = await s.execute(select(func.count()).select_from(Order))
            print(f'\n[SUCCESS] Total orders in DB: {res.scalar()}')
    except Exception as e:
        print(f'\n[ERROR] Something went wrong: {e}')

if __name__ == '__main__':
    asyncio.run(check())
