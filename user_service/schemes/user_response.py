from datetime import datetime
from typing import Any, List, Optional, Union
from pydantic import  Field, SecretStr, field_validator,BaseModel
# from user_service.schemes.user import UserBa 


# class UserInDBBase(UserBase):
#     id: Optional[int] = None
#     model_config = ConfigDict(from_attributes=True)



class UserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    is_superuser: bool
    is_active: bool
    email_verified: bool
    created_time: datetime
    # tfa_enabled: bool
    # totp_secret: bool = Field(default= False, alias = "password")
    scopes: Optional[List[str]] = []
    products: Optional[List]
    
    class Config:
        # used for having multiple response type like single and plural (list)
        populate_by_name = True
        orm_mode = True