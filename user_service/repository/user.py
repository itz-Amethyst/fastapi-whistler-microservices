from typing import Any, Dict, List, Optional
from fastapi import Depends, UploadFile
from slugify import slugify
from sqlalchemy import delete, or_, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from common.dep.db import DBSessionDepAsync
from product_service.models.product import Product as ProductModel
from user_service.models.scope import Scope
from user_service.models.user import User
from user_service.schemes import UserResponse 
from user_service.schemes.user import SuperUserCreate, UserCreate
from user_service.utils.security.hash import hash_password
class UserRepository:
    
    def __init__(self, sess: AsyncSession) -> None:
        self.session: AsyncSession = sess

    #! Todo create is_email_verified = false -> send email
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        return self.session.get(User, user_id)
    
    async def get_user_by_username(self, user_name: str)-> Optional[UserResponse]:
        result = await self.session.execute(select(User).filter_by(username= user_name))
        return result.scalars().first()

    async def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        hashed_password = await hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            email_verified=False,
            is_active=True,
            is_superuser=False,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(new_user)
        return new_user.id

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

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        result = await self.session.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_user_by_email_or_username(self, email: str, username: str) -> Optional[UserResponse]:
        result = await self.session.execute(
            select(User).filter(
                or_(
                    User.email == email,
                    User.username == username
                )
            )
        )
        return result.scalar_one_or_none()
    
db: AsyncSession = Depends(DBSessionDepAsync)
user_repository = UserRepository(db)