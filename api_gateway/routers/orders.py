from fastapi import APIRouter, HTTPException
from api_gateway.schemas.orders import OrderCreate
from api_gateway import kafka_producer

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", status_code=201)
async def create_order(order: OrderCreate):
    try:
        # 1. Модель Pydantic превращается в полноценный словарь со всеми полями
        order_data = order.model_dump()

        # 2. Отправляем в Kafka весь словарь целиком
        await kafka_producer.send_order_event(order_data)

        return {"status": "success", "message": "Order sent to Kafka", "order": order_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {str(e)}")


@router.get("/")
async def list_orders():
    return {"message": "Use Order Service to fetch orders list"}
