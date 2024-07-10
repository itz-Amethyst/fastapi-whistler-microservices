from pymongo.database import Database

from app import crud , schemas
from app.config.settings import settings
from app.utils.logger import logger_system
from tenacity import retry, stop_after_attempt, wait_fixed
FIRST_SUPERUSER = settings.general.FIRST_SUPERUSER

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
async def init_db(db: Database) -> None:
    print("inside")
    logger_system.warning("Creating initial data")
    user = await crud.user.get_by_email(db, email=FIRST_SUPERUSER)
    if not user:
        # Create user auth
        user_in = schemas.UserCreate(
            email=FIRST_SUPERUSER,
            password=settings.general.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name=FIRST_SUPERUSER,
        )
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841
    logger_system.warning("Initial data created")