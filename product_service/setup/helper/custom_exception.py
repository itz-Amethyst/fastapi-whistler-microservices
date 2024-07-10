from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.error.main import APIValidationError


def setup_custom_exceptions(app: FastAPI) -> None:
    # Custom HTTPException handler
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler( _ , exc: StarletteHTTPException ) -> ORJSONResponse:
        return ORJSONResponse(
            content = {
                "message": exc.detail ,
            } ,
            status_code = exc.status_code ,
            headers = exc.headers ,
        )

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(
            _ ,
            exc: RequestValidationError ,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            content = APIValidationError.from_pydantic(exc).dict(exclude_none = True) ,
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY ,
        )