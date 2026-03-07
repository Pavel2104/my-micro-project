from pydantic import BaseModel, ConfigDict # Добавили ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductRead(BaseModel):
    id: int
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)