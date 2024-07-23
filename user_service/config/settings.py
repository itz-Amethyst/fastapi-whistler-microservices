from functools import lru_cache
from pydantic import validator
from pydantic_settings import BaseSettings
from common.config.helper import DOTENV

class Settings(BaseSettings):
    VERIFICATION_METHOD: str = "OTP"
    PASSWORD_CRYPT_ALGO: str = "bcrypt"
    OTP_SECRET_KEY: str

    class Config:
        env_flie = DOTENV
    
    @validator("VERIFICATION_METHOD", pre=True, always=True)
    def validate_verification_method(cls, value):
        if value not in ("OPT", "Magic"):
            return "OTP"
        return value

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings