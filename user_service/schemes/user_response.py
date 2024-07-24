from typing import Optional

from pydantic import ConfigDict, Field, SecretStr, field_validator

from user_service.schemes.user import UserBase


class UserInDBBase(UserBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# todo decide later 
# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[SecretStr] = None
    totp_secret: Optional[SecretStr] = None
    totp_counter: Optional[int] = None


class UserReponse(UserInDB):
    hashed_password: bool = Field(default= False, alias = "password")
    # totp_secret: bool = Field(default= False, alias = "password")
    model_config = ConfigDict(populate_by_name=True)

    
    @classmethod
    @field_validator("hashed_password", model="before")
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False

    # @classmethod
    # @field_validator("totp_secret", model="before")
    # def evaluate_totp_secret(cls, totp_secret):
    #     if totp_secret:
    #         return True
    #     return False

    class Config:
        # used for having multiple response type like single and plural (list)
        orm_mode = True