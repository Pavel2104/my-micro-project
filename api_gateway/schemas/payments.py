from pydantic import BaseModel, ConfigDict # Добавили ConfigDict

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    status: str = "unpaid"

class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str

    # Финальный штрих для схем
    model_config = ConfigDict(from_attributes=True)