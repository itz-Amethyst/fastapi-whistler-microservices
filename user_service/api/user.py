from datetime import timedelta
from typing import Dict, List, Optional, Tuple, Union
from fastapi import APIRouter, Depends, HTTPException, Security, BackgroundTasks
from fastapi.responses import JSONResponse
from common.utils.email import send_email_validation_email 
from user_service.repository.user import UserRepository
from user_service.schemes import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from common.db.session import get_db_session_async
from user_service.utils.email import create_email_verification_token, decode_email_verification_token
from user_service.utils.security.auth import AuthDependency 
from user_service.schemes import UserResponse, TokenResponse, EmailValidation
from user_service.models.user import User
from common.config import settings

router = APIRouter()
db: AsyncSession = get_db_session_async()

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Security(AuthDependency())):
    return user

# Todo anotation
@router.get("/current", response_model=TokenResponse)
async def get_current_token(auth_data = Security(AuthDependency(return_token=True))):
    return TokenResponse(access_token=auth_data[1], token_type="Bearer")

@router.get("/getall", response_model=List[UserResponse])
async def get_all_users(
    auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"]
    ),
    db: AsyncSession = DBSessionDepAsync):
    user, token = auth_data
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user_repo = UserRepository(db)
    result = await user_repo.retrieve_all_users()
    return result


@router.post('/create', response_model=Dict[str, str])
async def create_user(user: UserCreate, tasks: BackgroundTasks, db: AsyncSession = DBSessionDepAsync):
    user_repo = UserRepository(db)
    db_user = await user_repo.get_user_by_email_or_username(user.email, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="seems you already have an account try log in")
    new_user = UserCreate(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    new_user = await user_repo.create_user(new_user)

    token = create_email_verification_token(user_id=str(new_user.id), expires_delta=timedelta(hours=12))
    email_validation_data = EmailValidation(email=user.email, subject="Verify Your Account", token=token)
    tasks.add_task(send_email_validation_email, email_validation_data)
    # Todo dict response 200, ok
    response_data = {
        "message": "User created successfully. Please check your email for verification.",
        "email_sent_to": user.email,
    }
    return JSONResponse(content= response_data, status_code = 201) 
    
@router.post('/resend-verification', response_model=dict)
async def resend_verification(email: str, tasks: BackgroundTasks, db: AsyncSession = DBSessionDepAsync):
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

@router.get('/verify', response_model=Dict[str, str])
async def verify_account(token: str, db: AsyncSession = DBSessionDepAsync):
    user_repo = UserRepository(db)
    decoded_payload =  decode_email_verification_token(token)
    user = await user_repo.get_user_by_id(user_id=decoded_payload['sub'])
    if not user:
        raise HTTPException(422, "Invalid code")
    
    await user_repo.update_user_verification(int(decoded_payload['sub']))
    return {"message": "Successfully verified the account"}
