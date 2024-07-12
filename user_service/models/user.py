
import re
from sqlalchemy import Boolean, Column, String
from common.models.base import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    pasword_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String, nullable=True, unique=True)


    # Todo hashing operations

    @validates("email")
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address: {email}")
        
        return email
    
    def __repr__(self):
        return f"User: {self.username}, email={self.email}, is_verified: {self.is_verified}"