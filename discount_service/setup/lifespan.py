from contextlib import asynccontextmanager
from fastapi import FastAPI
from common.utils.logger import logger_system
from discount_service.db.mongo import create_db_connection, close_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_system.info("Starting MongoDB server ...")

    #? Mongodb
    await create_db_connection()
    
    yield

    logger_system.info("Shutting down the system.")
    await close_db_connection()
