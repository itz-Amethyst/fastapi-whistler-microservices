from discount_service import api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from discount_service.setup.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(api.router)