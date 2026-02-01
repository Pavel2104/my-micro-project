FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости API Gateway
COPY api_gateway/requirements.txt ./api_gateway/requirements.txt
RUN pip install --no-cache-dir -r ./api_gateway/requirements.txt

# Устанавливаем зависимости Worker Service
COPY worker_service/requirements.txt ./worker_service/requirements.txt
RUN pip install --no-cache-dir -r ./worker_service/requirements.txt

# Копируем весь код
COPY api_gateway /app/api_gateway
COPY worker_service /app/worker_service

# Команда запуска
CMD ["uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]




