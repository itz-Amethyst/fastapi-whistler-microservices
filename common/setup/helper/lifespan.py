from contextlib import asynccontextmanager
from common.db.session import sessionManager
from fastapi import FastAPI
from common.utils.logger import logger_system
from common.db.session import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_system.info("Starting server ...")

    async with sessionManager._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    logger_system.info("Shutting down the system.")

    await sessionManager.close_async()
