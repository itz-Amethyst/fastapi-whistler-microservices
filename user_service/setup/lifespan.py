from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from common.utils.logger import logger_system
from user_service.utils.scope_update import check_and_update_scopes 
from user_service.setup.init_db import init_db


scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_system.info("Starting User_service ...")

    scheduler.start()
    await init_db() 
    yield

    logger_system.info("Shutting down the system.")
    scheduler.shutdown()


# Schedule the job
scheduler.add_job(
    check_and_update_scopes,
    trigger=IntervalTrigger(minutes=15),
    id="check_scopes",
    name="Check and update scopes every 15 minutes",
    replace_existing=True,
)