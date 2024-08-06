from user_service import api as user_api
from order_service import api as order_api
from discount_service import api as discount_api
from product_service import api as product_api
from fastapi import FastAPI


def setup_routers(app: FastAPI) -> None:
    
    app.include_router(user_api.router)
    app.include_router(order_api.router)
    app.include_router(discount_api.router)
    app.include_router(product_api.router)