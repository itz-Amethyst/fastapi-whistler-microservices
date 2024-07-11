from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import SecretStr
from common.config.helper import config

class Settings(BaseSettings):
    POSTGRES_USER: str = config.get("POSTGRES_USER")
    POSTGRES_PASSWORD: SecretStr = config.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = config.get("POSTGRES_DB")
    FULL_DATABASE_PG_URL: str = config.get("FULL_DATABASE_PG_URL")



@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()