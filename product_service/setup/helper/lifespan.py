from contextlib import asynccontextmanager
# from app.db.session import ping
from app.setup.helper.init_db import init_db
from app.utils.logger import logger_system


@asynccontextmanager
async def lifespan(app):
    logger_system.info("Starting ping command.")
    # await ping()
    await init_db()

    yield
    logger_system.info("Shutting down the system.")