from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_gateway.database import AsyncSessionLocal
from api_gateway.models import Product
from api_gateway.schemas.products import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_session)):
    obj = Product(**product.dict())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.get("/", response_model=list[ProductRead])
async def list_products(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Product.__table__.select())
    return result.scalars().all()