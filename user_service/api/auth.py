from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from contextmngr import SessionLocal
from user_service.config import settings
from user_service.repository.user import UserRepository
from user_service.schemes import TokenResponse, UserCreate
from user_service.utils.security.token import create_access_token, set_jwt_cookie 
from user_service.utils.security.hash import verify_password

router = APIRouter()

@router.post("/token/oauth2", response_model=TokenResponse)
async def login(user: UserCreate, response: Response, db: AsyncSession = Depends(DBSessionDepAsync)):
    user_repo = UserRepository(db)
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = datetime.utcnow() + expires_delta
    existing_user = await user_repo.get_user_by_username(user.username)
    if existing_user is None or not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    scopes = ['full_control'] if existing_user.is_superuser else [scope.title for scope in existing_user.scopes]
    # Decide later about scope
    token = create_access_token(subject=user.id, scopes=scopes, expires_delta=expires_delta)
    set_jwt_cookie(response, "jwt_token", token, expiration)
    # Refresh token ? where is it
    return {"access_token": token, "token_type": "bearer"}

