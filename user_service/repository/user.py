from typing import Any, Dict, List, Optional
from fastapi import Depends, UploadFile
from slugify import slugify
from sqlalchemy import delete, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from common.dep.db import DBSessionDepAsync
from product_service.models.product import Product as ProductModel
from user_service.models.user import User
from user_service.schemes import UserReponse
from user_service.utils.security.hash import hash_password
class UserRepository:
    
    def __init__(self, sess: Session) -> None:
        self.session: Session = sess
    
    #! Todo create is_email_verified = false -> send email
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserReponse]:
        return self.session.get(User, user_id)
    
    async def get_user_by_username(self, user_name: str)-> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(username= user_name))
        return result.scalars().first()

    async def create_user(self, username: str, password: str, is_superuser: bool = False):
        hashed_password = hash_password(password)
        new_user = User(id=username, username=username, hashed_password=hashed_password, is_superuser=is_superuser)
        async with self.session() as session:
            async with session.begin():
                session.add(new_user)

    async def get_by_email(self, email: str) -> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalars().first()
    
db: AsyncSession = Depends(DBSessionDepAsync)
user_repository = UserRepository(db)