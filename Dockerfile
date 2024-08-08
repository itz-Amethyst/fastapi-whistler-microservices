# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Install dependencies
RUN apk add --no-cache build-base

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /code

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

RUN chmod +x /code/scripts/run-migration.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run Alembic migrations and then Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]