#!/bin/bash

set -e

echo "Starting Docker containers..."
docker-compose up -d

function wait_for_postgres() {
  echo "Waiting for PostgreSQL to be ready..."

  until pg_isready -h db -U "$POSTGRES_USER"; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
  done
}

wait_for_postgres


echo "getting alembic revision"
alembic revision --autogenerate -m "init"

LATEST_REVESION_FILE=$(ls code/alembic/versions/*.py | head -n 1)

echo "Checking if the migration file is valid"
if grep -q "def downgrade" "$LATEST_REVESION_FILE" && ! grep -q "pass" "$LATEST_REVESION_FILE"; then
  echo "Alembic revesion file generated and contains valid files"
else 
  echo "Alembic revesion file is empty or invalid (might be case that database and models are up to date)"
  exit 1
fi

alembic upgrade head

echo "run-migration script completed successfully."
