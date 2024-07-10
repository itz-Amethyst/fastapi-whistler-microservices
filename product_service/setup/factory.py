from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status

from app.config.settings import settings
from app.messages.code.main import responses
from app.schemas.error.main import CommonHTTPError , APIValidationError
from app.setup.helper.custom_exception import setup_custom_exceptions
from app.setup.helper.lifespan import lifespan

from app.setup.helper.middleware import setup_cors_middleware
from app.setup.helper.static import serve_static_app
from app.setup.route.main import setup_routers
from app.config.logger.main import configure_logging
from app.setup.helper.init_db import init_db


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
        "name": "URLs",
        "description": "Shorten and manage URLs",
    },
]

def create_app():
    configure_logging()
    # init_db()
    description = f"{settings.general.PROJECT_NAME} API"
    app = FastAPI(
        title=settings.general.PROJECT_NAME,
        debug = settings.general.DEBUG,
        version = settings.general.VERSION,
        openapi_url=f"/api/{settings.general.API_V1_STR}/openapi.json",
        docs_url="/docs/",
        default_response_class = ORJSONResponse,
        openapi_tags = tags_metadata,
        description=description,
        redoc_url=None,
        responses = {
            status.HTTP_422_UNPROCESSABLE_ENTITY: {
                "description": "Validation Error" ,
                "model": APIValidationError ,  # Adds OpenAPI schema for 422 errors
            } ,
            **{
                code: {
                    "description": HTTPStatus(code).phrase ,
                    "model": CommonHTTPError ,
                }
                for code in responses
            } ,
        } ,
        # Todo Ping atlas mongo db
        lifespan = lifespan
    )
    setup_routers(app)
    setup_cors_middleware(app)
    serve_static_app(app)
    # Todo
    setup_custom_exceptions(app)
    return app





