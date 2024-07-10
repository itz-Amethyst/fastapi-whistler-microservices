from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.middlewares.correlation import CorrelationMiddleware
from app.config.settings import settings

def setup_cors_middleware(app):
    if settings.general.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.general.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )
        # Guards against HTTP Host Header attacks
        app.add_middleware(
            TrustedHostMiddleware ,
            #? TO Allow all for now
            # allowed_hosts = get_settings().security.allowed_hosts ,
        )
        app.add_middleware(
            CorrelationMiddleware
        )


