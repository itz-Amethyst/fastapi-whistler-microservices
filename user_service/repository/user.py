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
from user_service.models.scope import Scope
from user_service.models.user import User
from user_service.schemes import UserReponse
from user_service.schemes.user import SuperUserCreate, UserCreate
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

    async def create_user(self, user_data: UserCreate) -> Optional[UserReponse]:
        hashed_password = await hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            email_verified=user_data.email_verified,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser
        )
        async with self.session() as session:
            async with session.begin():
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
        return new_user

    async def create_super_user(self, user_data: SuperUserCreate) -> User:
        new_user = await self.create_user(user_data)
        
        # Add full_permission scope
        async with self.session() as session:
            scope = await session.execute(select(Scope).where(Scope.name == 'full_permission'))
            full_permission_scope = scope.scalar()
            if not full_permission_scope:
                full_permission_scope = Scope(name='full_permission')
                session.add(full_permission_scope)
                await session.commit()
                await session.refresh(full_permission_scope)
            
            new_user.scopes.append(full_permission_scope)
            await session.commit()
            await session.refresh(new_user)
            
        return new_user

    async def get_by_email(self, email: str) -> Optional[UserReponse]:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalars().first()
    
db: AsyncSession = Depends(DBSessionDepAsync)
user_repository = UserRepository(db)