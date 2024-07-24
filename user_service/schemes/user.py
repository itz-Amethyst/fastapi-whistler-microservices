from pydantic import EmailStr, StringConstraints
from common.schemes.base import BaseModel
from typing import Annotated, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True
    user_name: Optional[str] = ""

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None
    

class UserUpdate(UserBase):
    original: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None
    new_password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None

    
class UserLogin(UserBase):
    username: str
    # login through username or email decide later
    # email: EmailStr
    password: str
