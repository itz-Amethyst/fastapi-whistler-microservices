from typing import List, Optional
from pydantic import  Field, SecretStr, field_validator,BaseModel
# from user_service.schemes.user import UserBa 


# class UserInDBBase(UserBase):
#     id: Optional[int] = None
#     model_config = ConfigDict(from_attributes=True)



class UserResponse(BaseModel):
    id: Optional[int] = None
    is_verified: bool 
    username: str
    email: str
    is_superuser: bool
    is_active: bool
    email_verified: bool
    # tfa_enabled: bool
    # totp_secret: bool = Field(default= False, alias = "password")
    scopes: List[str]

    class Config:
        # used for having multiple response type like single and plural (list)
        populate_by_name = True
        orm_mode = True