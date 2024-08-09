from contextlib import asynccontextmanager

from fastapi import FastAPI
from common.db.session import sessionManager
from common.utils.logger import logger_system
from common.db.session import Base
from discount_service.db.mongo import create_db_connection
from user_service.setup.init_db import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_system.info("Starting server ...")

    with sessionManager.session_sync() as conn:
        Base.metadata.create_all(bind=conn.get_bind())
        conn.commit()
    
    await init_db()
    await create_db_connection()
    yield

    logger_system.info("Shutting down the system.")

    await sessionManager.close_async()
