from discount_service import api
from fastapi import FastAPI


app = FastAPI(docs_url='/docs/')
app.include_router(api.router)