from user_service import api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from common.config.logger import configure_logging
from user_service.setup.lifespan import lifespan

configure_logging()

app = FastAPI(docs_url='/docs/', lifespan=lifespan, debug=True)
app.include_router(api.router)