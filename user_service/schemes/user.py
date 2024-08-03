from pydantic import EmailStr, StringConstraints, BaseModel
# from common.schemes.base import BaseModel
from typing import Annotated, Optional
from datetime import datetime

# class UserBase(BaseModel):
#     email: Optional[EmailStr] = None
#     email_verified: Optional[bool] = False
#     is_superuser: Optional[bool] = False
#     is_active: Optional[bool] = True
#     user_name: Optional[str] = ""

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    # email_verified: Optional[bool] = False
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False


class SuperUserCreate(UserCreate):
    is_superuser: bool = True
    

class UserUpdate(BaseModel):
    original: Annotated[str, StringConstraints(min_length=8, max_length=64)]
    new_password: Annotated[str, StringConstraints(min_length=8, max_length=64)]

    
class UserLogin(BaseModel):
    username: str
    # login through username or email decide later
    # email: EmailStr
    password: str

class UserVerify(BaseModel):
    token: str