#!/bin/sh
set -e

echo "Running Aerich migrations..."
aerich -c pyproject.toml upgrade

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000