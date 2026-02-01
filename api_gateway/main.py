from fastapi import FastAPI
from contextlib import asynccontextmanager  # Добавили для lifespan
from api_gateway.database import engine
from api_gateway.routers import users, auth, orders, products, payments, test_kafka
from api_gateway.models import Base


# Современный способ управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется при СТАРТЕ
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Здесь приложение работает и принимает запросы

    # Код после yield выполняется при ОСТАНОВКЕ (если нужно что-то закрыть)
    # Например: await engine.dispose()


app = FastAPI(
    title="Real-Time Order Processing Platform",
    version="1.0",
    description="API Gateway для работы с заказами, продуктами, пользователями и платежами",
    lifespan=lifespan  # Подключаем lifespan здесь
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(payments.router)
app.include_router(test_kafka.router)


@app.get("/")
async def root():
    return {"message": "API Gateway is running"}