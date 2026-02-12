#!/bin/bash
set -e

# Wait for database to be ready
echo "Starting application..."

# Run Alembic migrations
python -m alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port $PORT
