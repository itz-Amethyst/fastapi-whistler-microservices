from fastapi import APIRouter, Depends, HTTPException, Security
from common.utils.email import send_email
from user_service.repository.user import UserRepository
from user_service.schemes import UserCreate
from sqlalchemy import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from user_service.utils.security.auth import auth_dependency
from user_service.schemes import UserReponse, TokenResponse
from user_service.models.user import User
from user_service.utils.security.hash import hash_password
from common.config import settings

router = APIRouter()

@router.get("/me", response_model=UserReponse)
async def get_me(user: User = Security(auth_dependency)):
    return user

@router.get("/current", response_model=TokenResponse)
async def get_current_token(auth_data: Tuple[User, str] = Security(auth_dependency(return_token=True))):
    return auth_data[1]


@router.post('/create', response_model=dict)
async def create_user(user: UserCreate, db: AsyncSession = Depends(DBSessionDepAsync)):
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

    token = create_access_token(subject=str(new_user.id), expires_delta=timedelta(hours=24))
    await send_email(
        email_to=user.email,
        subject="Verify your email",
        template_name="confirm_email.html",
        environment={"link": f"{settings.SERVER_HOST}/user/verify-email?token={token}"}
    )
    return new_user
    
