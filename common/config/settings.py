from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import SecretStr
from common.config.helper import DOTENV

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: SecretStr 
    POSTGRES_DB: str 
    FULL_DATABASE_PG_URL: str 


    class Config:
        env_file = DOTENV

@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()