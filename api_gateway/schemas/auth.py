from pydantic import BaseModel, EmailStr, ConfigDict # Добавили ConfigDict
from typing import Optional

# Схема для регистрации пользователя
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

# Схема для логина
class UserLogin(BaseModel):
    username: str
    password: str

# Схема для ответа с токеном
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Схема для ответа о текущем пользователе
class CurrentUser(BaseModel):
    id: int
    username: str
    email: EmailStr

    # Обновляем на современный синтаксис
    model_config = ConfigDict(from_attributes=True)

