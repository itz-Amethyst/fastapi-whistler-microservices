from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Security, BackgroundTasks
from common.utils.email import send_email_validation_email 
from user_service.repository.user import UserRepository
from user_service.schemes import UserCreate
from sqlalchemy import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from user_service.utils.email import create_email_verification_token
from user_service.utils.security.auth import AuthDependency 
from user_service.schemes import UserResponse, TokenResponse, EmailValidation
from user_service.models.user import User
from common.config import settings

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Security(AuthDependency(session=DBSessionDepAsync))):
    return user

# Todo anotation
@router.get("/current", response_model=TokenResponse)
async def get_current_token(auth_data = Security(AuthDependency(session=DBSessionDepAsync,return_token=True))):
    return auth_data[1]


@router.post('/create', response_model=dict)
async def create_user(user: UserCreate, tasks: BackgroundTasks, db: AsyncSession = Depends(DBSessionDepAsync)):
    user_repo = UserRepository(db)
    db_user = await user_repo.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password,
        is_verified=False,
    )
    await user_repo.create_user(new_user)

    token = create_email_verification_token(user_id=str(new_user.id), expires_delta=timedelta(hours=12))
    email_validation_data = EmailValidation(email=user.email, subject="Verify Your Account", token=token)
    tasks.add_task(send_email_validation_email, email_validation_data)
    return new_user
    
@router.post('/resend-verification', response_model=dict)
async def resend_verification(email: str, tasks: BackgroundTasks, db: AsyncSession = Depends(DBSessionDepAsync)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=400, detail="Email not registered")
    if user.email_verified:
        return {"message": "Email is already verified"}

    token = create_email_verification_token(user_id=str(user.id), expires_delta=timedelta(hours=12))
    email_validation_data = EmailValidation(email=user.email, subject="Verify Your Account", token=token)
    tasks.add_task(send_email_validation_email, email_validation_data)
    return {"message": "Verification email has been resent. Please check your email."}