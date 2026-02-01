# Используем официальный Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 1. Копируем requirements (путь теперь от корня проекта)
COPY order_service/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 2. Копируем всё содержимое папки order_service в текущую директорию (/app)
COPY order_service/ .

# 3. Копируем ОДИН нужный файл из соседнего сервиса в /app
# Теперь он будет лежать рядом с main.py
COPY api_gateway/kafka_producer.py .

# 4. Явно указываем Python искать модули в /app
ENV PYTHONPATH=/app

# Экспонируем порт
EXPOSE 8000

# Команда для запуска (main:app сработает, так как файл в корне /app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]