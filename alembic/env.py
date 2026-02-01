import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Добавляем корень проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ВАЖНО: Импортируем Base только ПОСЛЕ настройки путей
from order_service.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Принудительно очищаем URL от asyncpg, если он туда попал
raw_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@orders_db:5432/orders_db")
if "+asyncpg" in raw_url:
    DATABASE_URL = raw_url.replace("+asyncpg", "")
else:
    DATABASE_URL = raw_url

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Создаем СТРОГО синхронный движок
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()