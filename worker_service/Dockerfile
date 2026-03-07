FROM python:3.12-slim

RUN useradd -m worker

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER worker

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
