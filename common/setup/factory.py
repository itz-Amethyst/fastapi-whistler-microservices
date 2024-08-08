from http import HTTPStatus
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from common.config.logger import configure_logging
from common.setup.helper.lifespan import lifespan

from common.config import settings
# from app.messages.code.main import responses
# from app.schemas.error.main import CommonHTTPError , APIValidationError
# from app.setup.helper.custom_exception import setup_custom_exceptions

from common.setup.helper.middleware import setup_middlewares 
from common.setup.helper.route import setup_routers
# from app.setup.helper.static import serve_static_app
# from app.setup.helper.init_db import init_db


tags_metadata = [
    {
        "name": "Authentication",
        "description": "Get authentication token",
    },
    {
        "name": "Users",
        "description": "User registration and management",
    },
    {
        "name": "Product",
        "description": "Product management",
    },
    {
        "name": "Discount",
        "description": "Discount management",
    },
    {
        "name": "Order",
        "description": "Order management",
    },
]

def create_app():
    configure_logging()
    description = f"Whistler Apis"
    app = FastAPI(
        title="Whistler",
        debug = settings.DEBUG,
        version = "0.2.0",
        openapi_url=f"/api/v1/openapi.json",
        docs_url="/docs/",
        default_response_class = ORJSONResponse,
        openapi_tags = tags_metadata,
        description=description,
        redoc_url=None,
        # TODO
        # responses = {
        #     status.HTTP_422_UNPROCESSABLE_ENTITY: {
        #         "description": "Validation Error" ,
        #         "model": APIValidationError ,  # Adds OpenAPI schema for 422 errors
        #     } ,
        #     **{
        #         code: {
        #             "description": HTTPStatus(code).phrase ,
        #             "model": CommonHTTPError ,
        #         }
        #         for code in responses
        #     } ,
        # } ,
        # Todo Ping atlas mongo db
        lifespan = lifespan
    )
    # /metrics
    Instrumentator().instrument(app).expose(app)
    setup_routers(app)
    setup_middlewares(app)
    # serve_static_app(app)
    # Todo
    # setup_custom_exceptions(app)
    return app





