from fastapi import APIRouter
from api_gateway.kafka_producer import send_order_event

router = APIRouter()

@router.post("/send-test-order/")
async def send_test_order():
    # Тестовое сообщение
    await send_order_event(order_id=999, status="created")
    return {"message": "Test order sent"}
