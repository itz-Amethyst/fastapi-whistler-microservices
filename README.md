## FastAPI-Whistler Microservices Project

This project is a collection of microservices for managing `Products`, `Orders`, `Discounts`, and `Users`. Each service is built using FastAPI, with PostgreSQL as the primary database. The Discount Service uses `MongoDB`. The project also includes support for managing generic pictures associated with different entities.

- > Service Communication

In this microservices architecture, services communicate with each other through APIs when required.

- > Async-Oriented Architecture

This project uses asynchronous programming to handle tasks, including
in some areas, concurrency has been applied to further optimize performance.

### Purpose:
The main purpose of this proejct is to explore the potentials of FastAPI in building high scale applications


## Features

- `Product Management`: CRUD operations for products, including image upload (handled via sql queries).
- `Order Management`: Create and manage orders, track order status (handled via sql queries).
- `Discount Management`: Apply and manage discounts on products or orders.
- `User Management`: User registration, authentication with scope permissions through application.
- `Generic Picture Support`: Upload and associate images with various entities.


## Built With :

[![FastAPI](https://img.shields.io/badge/FASTAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-2.0.31-d32f2f?style=for-the-badge&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Asyncpg](https://img.shields.io/badge/ASYNC_PG-0.29.0-039be5?style=for-the-badge)](https://github.com/MagicStack/asyncpg)
[![Alembic](https://img.shields.io/badge/ALEMBIC-1.13.2-8bc34a?style=for-the-badge)](https://alembic.sqlalchemy.org/)
[![pymongo](https://img.shields.io/badge/PYMONGO-4.8.0-47a248?style=for-the-badge&logo=mongodb)](https://pypi.org/project/pymongo/)
[![Beanie](https://img.shields.io/badge/BEANIE-1.26.0-0d9488?style=for-the-badge)](https://pypi.org/project/beanie/)
[![structlog](https://img.shields.io/badge/STRUCTLOG-24.4.0-00d084?style=for-the-badge)](https://www.structlog.org/)
[![tenacity](https://img.shields.io/badge/TENACITY-8.5.0-ff2e63?style=for-the-badge)](https://pypi.org/project/tenacity/)
[![aiohttp](https://img.shields.io/badge/AIOHTTP-3.10.3-009688?style=for-the-badge&logo=aiohttp)](https://docs.aiohttp.org/en/stable/)
[![PyJWT](https://img.shields.io/badge/PYJWT-2.8.0-7f7f7f?style=for-the-badge)](https://pypi.org/project/PyJWT/)
[![emails](https://img.shields.io/badge/EMAILS-0.6-d44638?style=for-the-badge)](https://pypi.org/project/emails/)
[![aiosmtplib](https://img.shields.io/badge/AIOSMTPLIB-3.0.1-39a7a1?style=for-the-badge)](https://pypi.org/project/aiosmtplib/)
[![APScheduler](https://img.shields.io/badge/APScheduler-3.10.4-512da8?style=for-the-badge)](https://pypi.org/project/APScheduler/)
[![prometheus-fastapi-instrumentator](https://img.shields.io/badge/PROMETHEUS_FASTAPI_INSTRUMENTATOR-7.0.0-f56c42?style=for-the-badge)](https://pypi.org/project/prometheus-fastapi-instrumentator/)
[![aiofiles](https://img.shields.io/badge/AIOFILES-24.1.0-2196f3?style=for-the-badge)](https://pypi.org/project/aiofiles/)

---
### **You can use my .env as an example but be aware to change that later**
---

## Running with Docker

To quickly get started with Docker, follow these steps:


#### Start the services using Docker Compose:

```sh
docker-compose up
```

This command will start all the services defined in docker-compose.yml file, including:

- `db`: PostgreSQL database
- `web`: Your FastAPI application
- `pgadmin`: PgAdmin for managing the PostgreSQL database
- `prometheus`: Prometheus for monitoring
- `grafana`: Grafana for visualization

You can access your FastAPI application at http://localhost:8000

PgAdmin at http://localhost:5050

Grafana at http://localhost:3000

and Prometheus at http://localhost:9090

#### Stop the services:
```sh
docker-compose down
```

### Running localy:
Running Locally with Poetry

(Because we're using `PostgreSQL` docker image as a database we have to first start the db)

1. **Start the PostgreSQL database service using Docker Compose**:


```sh
./scripts/run_migration.sh
```

This script starts the PostgreSQL Docker container and then performs database migrations to prepare the model for use.


2. Install the dependencies using Poetry:

```sh
poetry install
```

3. Run the FastAPI application using Uvicorn:

```sh
poetry run uvicorn main:app --reload
```

FastAPI application will be available at http://localhost:8000.


### Contribution

Feel free to open a PR; I'd appreciate that! 