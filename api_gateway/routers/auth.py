from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api_gateway.database import get_db
from api_gateway.models import User
from api_gateway.schemas.auth import UserRegister, UserLogin, Token, CurrentUser
from api_gateway.core.security import hash_password, verify_password, create_access_token, get_current_user
from sqlalchemy.future import select

router = APIRouter(prefix="/auth", tags=["Auth"])


# Регистрация пользователя
@router.post("/register", response_model=CurrentUser)
async def register_user(user: UserRegister, db: AsyncSession = Depends(get_db)):
    # Проверяем, есть ли уже пользователь с таким username или email
    result = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Логин и получение токена
@router.post("/token", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Получение информации о текущем пользователе
@router.get("/me", response_model=CurrentUser)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
