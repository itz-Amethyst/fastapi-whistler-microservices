from fastapi import FastAPI
from order_service import api


app = FastAPI()

app.include_router(api.router)