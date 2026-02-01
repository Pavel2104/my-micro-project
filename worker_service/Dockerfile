FROM python:3.12-slim

# Создаем обычного пользователя
RUN useradd -m worker

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код worker_service
COPY . .

# Меняем пользователя на обычного
USER worker

# Запуск Celery
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
