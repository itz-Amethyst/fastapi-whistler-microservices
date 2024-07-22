
import re
from sqlalchemy import Boolean, String
from common.models.base import BaseModel
from sqlalchemy.orm import validates, mapped_column, Mapped


class User(BaseModel):
    __tablename__ = 'users'
    
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_token: Mapped[str] = mapped_column(String, nullable=True, unique=True)


    # Todo hashing operations

    @validates("email")
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address: {email}")
        
        return email
    
    def __repr__(self):
        return f"User: {self.username}, email={self.email}, is_verified: {self.is_verified}"