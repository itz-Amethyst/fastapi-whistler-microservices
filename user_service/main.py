from user_service import api
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from user_service.utils.scope_update import check_and_update_scopes

scheduler = BackgroundScheduler()
scheduler.start()
app = FastAPI(docs_url='/docs/')
app.include_router(api.router)

# To update scopes in db
scheduler.add_job(
    check_and_update_scopes,
    trigger=IntervalTrigger(minutes=15),
    id="check_scopes",
    name="Check and update scopes every 15 minutes",
    replace_existing=True
)
