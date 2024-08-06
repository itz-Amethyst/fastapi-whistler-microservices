from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from common.config import settings
def setup_cors_middleware(app):

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
    # app.add_middleware(
    #     CorrelationMiddleware
    # )


