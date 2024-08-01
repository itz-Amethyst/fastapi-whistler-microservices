from contextlib import asynccontextmanager

from sqlalchemy import text
from common.db.session import sessionManager, DBSessionManager
from fastapi import FastAPI
from common.utils.logger import logger_system
from common.db.session import Base, metadata, DATABASE_ENGINE, DATABASE_ENGINE_ASYNC
import logging 

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("PRINTINGGGGG")
    logger_system.info("Starting server ...")

    with sessionManager.session_sync() as conn:

        # conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
        Base.metadata.create_all(bind=conn.get_bind())
        conn.commit()
    # async with sessionManager._async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield

    logger_system.info("Shutting down the system.")

    await sessionManager.close_async()
