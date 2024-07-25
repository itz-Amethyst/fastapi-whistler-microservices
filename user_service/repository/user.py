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
class UserRepository:
    
    def __init__(self, sess: Session) -> None:
        self.session: Session = sess
        
    async def get_user_by_id(self, user_id: str) -> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()
    
    async def get_user_by_username(self, user_name: str)-> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(username= user_name))
        return result.scalars().first()

    async def create_user(self, username: str, password: str, is_superuser: bool = False):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(id=username, username=username, hashed_password=hashed_password, is_superuser=is_superuser)
        async with self.session() as session:
            async with session.begin():
                session.add(new_user)

    async def get_by_email(self, email: str) -> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalars().first()
    
db: AsyncSession = Depends(DBSessionDepAsync)
user_repository = UserRepository(db)