from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, EmailStr, validator


class CreatedMixin(BaseModel):
    created: Optional[datetime] = None

    @validator("created", pre=True, always=True)
    def set_created(cls, v):

        return v or datetime.now(timezone.utc) 

class TokenResponse(CreatedMixin):
    access_token: str
    token_type: str 