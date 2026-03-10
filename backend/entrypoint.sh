#!/bin/sh
set -e

echo "Running Tortoise migrations..."
tortoise migrate

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000