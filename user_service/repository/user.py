from typing import Any, Dict, List, Optional
from fastapi import Depends, UploadFile
from slugify import slugify
from sqlalchemy import delete, or_, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload
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
    
    def prepare_query(self):
        return select(User).options(
            joinedload(User.scopes),
            joinedload(User.products)
        )

    async def retrieve_all_users(self) -> Optional[List[UserResponse]]:
        query = self.prepare_query
        result = await self.session.execute(query)
        return result.unique().scalars().all()
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        query = self.prepare_query()
        result = await self.session.execute(query.filter(User.id == user_id))
        return result.unique().scalar_one_or_none()
    
    async def get_user_by_username(self, user_name: str)-> Optional[UserResponse]:
        query = self.prepare_query()
        result = await self.session.execute(query.filter(User.username == user_name))
        return result.unique().scalar_one_or_none()

    async def create_user(self, user_data: UserCreate, email_verified: bool = False, is_superuser: int = False) -> Optional[UserResponse]:
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            email_verified=email_verified,
            is_active=True,
            is_superuser=is_superuser,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(new_user)
        return new_user

    async def create_super_user(self, user_data: SuperUserCreate) -> User:
        new_user = await self.create_user(user_data, True, True)
        
        # Add full_permission scope
        
        scope = await self.session.execute(select(Scope).where(Scope.name == 'full_permission'))
        full_permission_scope = scope.scalar()
        if not full_permission_scope:
            full_permission_scope = Scope(name='full_permission')
            self.session.add(full_permission_scope)
            await self.session.commit()
            await self.session.refresh(full_permission_scope)
        
        new_user.scopes.append(full_permission_scope)
        await self.session.commit()
        await self.session.refresh(new_user)
        
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
    
    async def update_user_verification(self, user_id: int) -> None:
        await self.session.execute(
            update(User).where(User.id == user_id).values(email_verified=True)
        )
        await self.session.commit()
    
db: AsyncSession = Depends(DBSessionDepAsync)
user_repository = UserRepository(db)