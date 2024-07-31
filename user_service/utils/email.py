import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.config import settings
from common.utils.logger import logger_system
from user_service.models.user import User
from user_service.schemes import UserCreate, UserResponse, EmailValidation
from user_service.repository.user import UserRepository
from common.dep.db import DBSessionDep 

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def create_email_verification_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": user_id}
    current_time = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_email_verification_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is None:
            raise ValueError("Token has no expiration")
        now = datetime.now(timezone.utc).timestamp()
        if now > exp:
            raise ValueError("Token has expired")
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.DecodeError:
        raise ValueError("Invalid token")
