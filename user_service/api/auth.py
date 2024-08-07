from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from user_service.config import settings
from user_service.repository.scope import ScopeRepository
from user_service.repository.user import UserRepository
from user_service.schemes import TokenResponse,UserLogin 
from user_service.utils.security.token import create_access_token, set_jwt_cookie 
from user_service.utils.security.hash import verify_password
from common.utils.logger import logger_system

router = APIRouter()

async def determine_scopes(existing_user, db: AsyncSession) -> list:
    if existing_user.is_superuser:
        scope_repo = ScopeRepository(sess=db)
        # Adds the scope to user if hadn't been applied
        await scope_repo.add_scope_to_user(existing_user.id, "full_control")
        return ['full_control']
    elif existing_user.scopes:
        return [scope.title for scope in existing_user.scopes]
    else:
        return []

async def authenticate_user(username: str, password: str, db: AsyncSession, request: Request):
    user_repo = UserRepository(db)
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = datetime.utcnow() + expires_delta

    existing_user = await user_repo.get_user_by_username(username)
    if not existing_user:
        logger_system.warning(f"Failed login attempt for username: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not existing_user.email_verified:
        logger_system.warning(f"Failed attempt with unverified email : {username}")
        raise HTTPException(status_code=401, detail="Unverified email")

    is_password_valid = await verify_password(password, existing_user.password_hash)
    if not is_password_valid:
        logger_system.warning(f"Failed login attempt for username: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    scope = await determine_scopes(existing_user, db)

    token = create_access_token(subject=existing_user.id, scopes=scope, expires_delta=expires_delta, request = request)
    
    return token, expiration, existing_user

@router.post("/login", response_model=TokenResponse)
async def login_json(request: Request, user: UserLogin, response: Response, db: AsyncSession = DBSessionDepAsync):
    token, expiration, user = await authenticate_user(user.username, user.password, db, request)
    set_jwt_cookie(response, "jwt_token", token, expiration)
    return TokenResponse(access_token=token, token_type="bearer")

@router.post("/oauth2", response_model=TokenResponse)
async def login_oauth(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = DBSessionDepAsync):
    token, expiration, user = await authenticate_user(form_data.username, form_data.password, db, request)
    set_jwt_cookie(response, "jwt_token", token, expiration)
    return TokenResponse(access_token=token, token_type="bearer")

