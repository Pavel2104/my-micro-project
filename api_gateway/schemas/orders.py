from pydantic import BaseModel, ConfigDict
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    status: str = "pending"
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int

    # Обновленный синтаксис V2
    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    items: List[OrderItemRead] = []

    # Обновленный синтаксис V2
    model_config = ConfigDict(from_attributes=True)
