#!/bin/bash

# Wait for PostgreSQL to be ready before proceeding
/app/wait-for-it.sh postgres:5432 --timeout=30 --strict -- echo "PostgreSQL is up"

# Run database initialization
python /app/init_db.py

# Start the FastAPI application
exec uvicorn api.api:app --host 0.0.0.0 --port 8000
