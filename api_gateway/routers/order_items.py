from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_gateway.database import AsyncSessionLocal
from api_gateway.models import OrderItem
from api_gateway.schemas.orders import OrderItemCreate, OrderItemRead

router = APIRouter(prefix="/order-items", tags=["Order Items"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=OrderItemRead)
async def create_item(item: OrderItemCreate, session: AsyncSession = Depends(get_session)):
    obj = OrderItem(**item.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.get("/", response_model=list[OrderItemRead])
async def list_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(OrderItem.__table__.select())
    return result.scalars().all()