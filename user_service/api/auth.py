from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from common.dep.db import DBSessionDepAsync
from contextmngr import SessionLocal
from user_service.repository.user import UserRepository
from user_service.schemes import TokenResponse, UserCreate
from user_service.utils.security.token import create_access_token 

router = APIRouter()

@router.post("/token/oauth2", response_model=TokenResponse)
async def login(user: UserCreate, db: AsyncSession = Depends(DBSessionDepAsync)):
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_user_by_username(user.username)
    if existing_user is None or not existing_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Decide later about scope
    token = create_access_token(subject=user.username, scopes=["full_control"])
    return {"access_token": token, "token_type": "bearer"}

