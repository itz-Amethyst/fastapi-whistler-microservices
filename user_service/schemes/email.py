from pydantic import BaseModel, EmailStr, SecretStr

class EmailValidation(BaseModel):
    email: EmailStr
    subject: str
    token: SecretStr