from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import SecretStr
from common.config.helper import DOTENV

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: SecretStr 
    POSTGRES_DB: str 
    FULL_DATABASE_PG_URL: str 
    FULL_MONGODB_URL: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    LOG_LEVEL: str = "WARNING"
    DEBUG: str = True

    # imagine something like this lit print("")
    EMAIL_TEMPLATES_DIR: str
    SERVER_HOST: str
    EMAIL_TEMPLATES_DIR: str
    SMTP_PASSWORD: str
    SMTP_USER: str

    class Config:
        extra = 'ignore'
        env_file = DOTENV

@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()