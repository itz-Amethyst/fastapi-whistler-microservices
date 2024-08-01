from user_service import api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from common.setup.helper.lifespan import lifespan
from common.config import settings
from common.utils.logger import logger_system
from common.config.logger import configure_logging

configure_logging()

app = FastAPI(docs_url='/docs/', lifespan=lifespan, debug=True)
app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )
app.include_router(api.router)