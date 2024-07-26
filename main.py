from contextlib import asynccontextmanager
from fastapi import FastAPI
from common.config import get_settings
from common.config.logger import configure_logging
from common.db.session import sessionManager, Base
from product_service.api import router as product_router
from common.utils.logger import logger_system

# if project gets bigger should decide to create a setup folder for this even 
configure_logging()
app = FastAPI() 

app.include_router(router=product_router, prefix='/product')

@asynccontextmanager
async def lifespan(app):
    logger_system.info("Starting server ...")

    async with sessionManager._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    logger_system.info("Shutting down the system.")

    await sessionManager.close_async()