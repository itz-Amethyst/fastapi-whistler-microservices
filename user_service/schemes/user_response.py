from typing import Optional

from pydantic import ConfigDict, Field, SecretStr, field_validator

from user_service.schemes.user import UserBase


class UserInDBBase(UserBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)



class UserReponse(UserInDBBase):
    is_verified: bool 
    username: str
    email: str
    is_superuser: bool
    is_active: bool
    email_verified: bool
    # tfa_enabled: bool
    # totp_secret: bool = Field(default= False, alias = "password")
    model_config = ConfigDict(populate_by_name=True)

    class Config:
        # used for having multiple response type like single and plural (list)
        orm_mode = True