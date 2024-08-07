from fastapi import FastAPI
from product_service import api


app = FastAPI()

app.include_router(api.router)