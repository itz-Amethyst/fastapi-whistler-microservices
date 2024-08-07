from contextlib import asynccontextmanager

from fastapi import FastAPI
from common.db.session import sessionManager
from common.utils.logger import logger_system
from common.db.session import Base



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_system.info("Starting server ...")

    with sessionManager.session_sync() as conn:
        Base.metadata.create_all(bind=conn.get_bind())
        conn.commit()
    
    yield

    logger_system.info("Shutting down the system.")

    await sessionManager.close_async()
