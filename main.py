from fastapi import FastAPI
from common.config import get_settings
from common.config.logger import configure_logging
from product_service.api import router as product_router

# if project gets bigger should decide to create a setup folder for this even 
configure_logging()
app = FastAPI() 

app.include_router(router=product_router, prefix='/product')