from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import text
from common.db.session import sessionManager, DBSessionManager
from fastapi import FastAPI
from common.utils.logger import logger_system
from common.db.session import Base, metadata, DATABASE_ENGINE, DATABASE_ENGINE_ASYNC
import logging

from user_service.utils.scope_update import check_and_update_scopes 

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

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
    # Start the scheduler
    scheduler.start()
    yield

    logger_system.info("Shutting down the system.")
    scheduler.shutdown()

    await sessionManager.close_async()

# Schedule the job
scheduler.add_job(
    check_and_update_scopes,
    trigger=IntervalTrigger(minutes=15),
    id="check_scopes",
    name="Check and update scopes every 15 minutes",
    replace_existing=True,
)