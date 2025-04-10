FROM python:3.12-slim

WORKDIR /app


COPY gateway/organization_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gateway/organization_service/main.py /app/main.py
COPY gateway/organization_service/src /app/src
COPY shared /app/shared
COPY gateway/organization_service/.env /app/.env
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

ENV PYTHONPATH=/app/src:/app/shared

CMD ["bash", "-c", "sleep 5 && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
