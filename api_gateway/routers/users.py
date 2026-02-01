from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from api_gateway.database import get_db
from api_gateway.models import User
from api_gateway.schemas.users import UserCreate, UserRead, UserUpdate
from api_gateway.core.security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])


# Получить список всех пользователей (только авторизованные)
@router.get("/", response_model=List[UserRead])
async def get_users(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


# Получить пользователя по ID
@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


# Создать нового пользователя
@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Обновить данные пользователя
@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Удалить пользователя
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    await db.delete(db_user)
    await db.commit()