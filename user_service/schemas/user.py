from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, Optional
from datetime import datetime


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None
    

class UserUpdate(UserBase):
    original: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None
    new_password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None

    
class UserLogin(UserBase):
    # username: str
    # login through username or email decide later
    email: EmailStr
    password: str
