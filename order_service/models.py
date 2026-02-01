from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric
)
from sqlalchemy.orm import DeclarativeBase  # Добавили это
from datetime import datetime, timezone

# Создаем свою базу для этого микросервиса
class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default="CREATED")
    total_amount = Column(Numeric(10, 2), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} status={self.status}>"