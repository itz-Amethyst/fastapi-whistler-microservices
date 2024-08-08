from user_service.repository.user import UserRepository
from user_service.schemes import UserCreate 
from common.utils.logger import logger_system
from user_service.config import settings
from tenacity import retry, stop_after_attempt, wait_fixed
from common.db.session import get_db_session_async

FIRST_SUPERUSER = settings.FIRST_SUPERUSER_NAME
FIRST_SUPERUSER_EMAIL = FIRST_SUPERUSER + "@gmail.com"

max_tries = 60 * 5  # 5 minutes
wait_seconds = 30 


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
async def init_db() -> None:
    async for db in get_db_session_async():
        user_repository = UserRepository(sess=db)
        logger_system.warning("Creating initial data")
        user = await user_repository.get_user_by_username(user_name=settings.FIRST_SUPERUSER_NAME)
        if not user:
            # Create user auth
            user_data = UserCreate(
                email=FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                username=FIRST_SUPERUSER,
            )
            user = await user_repository.create_super_user(user_data) 
    logger_system.warning("Initial data created")