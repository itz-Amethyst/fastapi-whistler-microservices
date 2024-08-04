from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from user_service.models.scope import Scope
from user_service.repository.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ScopeRepository:
    
    def __init__(self, sess: AsyncSession) -> None:
        self.session = sess
        self.user_repo = UserRepository(sess)
    
    
    async def add_scope_to_user(self, user_id: int, scope_name: str) -> bool:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        scope = await self.session.execute(select(Scope).filter(Scope.name == scope_name))
        scope = scope.scalar_one_or_none()
        if not scope:
            raise HTTPException(status_code=404, detail=f"Scope '{scope_name}' does not exist")

        if scope not in user.scopes:
            user.scopes.append(scope)
            await self.session.commit()
            return True
        return False

    async def remove_scope_from_user(self, user_id: int, scope_name: str) -> bool:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        scope = await self.session.execute(select(Scope).filter(Scope.name == scope_name))
        scope = scope.scalar_one_or_none()
        if not scope:
            raise HTTPException(status_code=404, detail=f"Scope '{scope_name}' does not exist")

        if scope in user.scopes:
            user.scopes.remove(scope)
            await self.session.commit()
            return True
        return False

    async def get_all_scopes(self) -> List[Scope]:
        result = await self.session.execute(select(Scope))
        return result.scalars().all()