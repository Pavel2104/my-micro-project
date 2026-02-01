from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_gateway.database import AsyncSessionLocal
from api_gateway.models import Payment
from api_gateway.schemas.payments import PaymentCreate, PaymentRead

router = APIRouter(prefix="/payments", tags=["Payments"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=PaymentRead)
async def create_payment(payment: PaymentCreate, session: AsyncSession = Depends(get_session)):
    obj = Payment(**payment.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.get("/", response_model=list[PaymentRead])
async def list_payments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Payment.__table__.select())
    return result.scalars().all()