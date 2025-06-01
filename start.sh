#!/bin/bash
set -e

echo "==== Checking for model changes and generating Alembic migrations ===="
alembic revision --autogenerate -m "Auto migration" || true

echo "==== Applying Alembic migrations ===="
alembic upgrade head

echo "==== Starting backend ===="
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
