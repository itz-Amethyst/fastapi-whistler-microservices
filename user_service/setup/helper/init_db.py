from pymongo.database import Database
from user_service.repository.user import user_repository
from user_service.schemes import UserCreate 
from common.utils.logger import logger_system
from user_service.config import settings
from tenacity import retry, stop_after_attempt, wait_fixed
from user_service.utils.security.hash import hash_password

FIRST_SUPERUSER = settings.FIRST_SUPERUSER_NAME

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
async def init_db(db: Database) -> None:
    # Todo
    print("inside")
    logger_system.warning("Creating initial data")
    user = await user_repository.get_user_by_username(user_name=settings.FIRST_SUPERUSER_NAME)
    if not user:
        hashed_password = hash_password(settings.FIRST_SUPERUSER_PASSWORD)
        # Create user auth
        user_data = UserCreate(
            email=FIRST_SUPERUSER,
            password=hashed_password,
            is_superuser=True,
            email_verified=True,
            username=FIRST_SUPERUSER,
        )
        user = await user_repository.create_super_user(user_data) 
    logger_system.warning("Initial data created")