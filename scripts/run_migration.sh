#!/bin/bash

set -e
cd "$(dirname "$0")/.."
echo "Starting Docker containers..."
docker-compose up -d db

function wait_for_postgres() {
  echo "Waiting for PostgreSQL to be ready..."

  until docker-compose exec -T db pg_isready -U "itz-amethyst" -d "whistler-db"; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
  done
}

wait_for_postgres


# echo "getting alembic revision"
alembic revision --autogenerate -m "init"

if [ -d "code/alembic/versions" ]; then
    # If 'code' directory exists
    LATEST_REVISION_FILE=$(ls code/alembic/versions/*.py | head -n 1)
else
    # If 'code' directory does not exist
    LATEST_REVISION_FILE=$(ls alembic/versions/*.py | head -n 1)
fi

echo "Checking if the migration file is valid"
if grep -q "def downgrade" "$LATEST_REVESION_FILE" && ! grep -q "pass" "$LATEST_REVESION_FILE"; then
  echo "Alembic revesion file generated and contains valid files"
else 
  echo "Alembic revesion file is empty or invalid (might be case that database and models are up to date)"
  exit 1
fi

sleep 1
alembic upgrade head

echo "run-migration script completed successfully."
