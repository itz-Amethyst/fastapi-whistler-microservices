from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from common.config import settings
from user_service.config import settings as user_settings

def setup_middlewares(app):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH"],
        expose_headers=["Authorization", "Content-Range", "Range",
                        "Access-Control-Allow-Origin",
                        "Access-Control-Allow-Credentials",
                        "Access-Control-Allow-Headers",
                        "Access-Control-Max-Age"
                        ],
    )
    # Guards against HTTP Host Header attacks
    app.add_middleware(
        TrustedHostMiddleware ,
        #? TO Allow all for now
        # allowed_hosts = get_settings().security.allowed_hosts ,
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key = user_settings.SECRET_KEY 
    )
    # app.add_middleware(
    #     CorrelationMiddleware
    # )


