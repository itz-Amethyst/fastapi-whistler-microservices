from typing import Optional, Tuple, Union
from fastapi import APIRouter, Depends, HTTPException, Security
from user_service.models.user import User
from common.dep.db import DBSessionDepAsync
from user_service.repository.scope import ScopeRepository
from user_service.utils.security.auth import AuthDependency
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/users/{user_id}/scopes")
async def add_scope_to_user(
    user_id: int,
    scope_name: str,
    auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"]
    ),
    db: AsyncSession = DBSessionDepAsync
):
    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user_repo = ScopeRepository(db)
    try:
        success = await user_repo.add_scope_to_user(user_id, scope_name)
        if success:
            return {"message": f"Scope {scope_name} added to user {user_id}"}
        else:
            return {"message": f"Scope {scope_name} already exists for user {user_id}"}
    except HTTPException as e:
        raise e

@router.delete("/users/{user_id}/scopes/{scope_name}")
async def remove_scope_from_user(
    user_id: int,
    scope_name: str,
    auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"]
    ),
    db: AsyncSession = DBSessionDepAsync
):
    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user_repo = ScopeRepository(db)
    try:
        success = await user_repo.remove_scope_from_user(user_id, scope_name)
        if success:
            return {"message": f"Scope {scope_name} removed from user {user_id}"}
        else:
            return {"message": f"Scope {scope_name} was not assigned to user {user_id}"}
    except HTTPException as e:
        raise e

@router.get("/scopes")
async def get_all_scopes(
    auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"]
    ),
    db: AsyncSession = DBSessionDepAsync
):
    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user_repo = ScopeRepository(db)
    scopes = await user_repo.get_all_scopes()
    return {"scopes": [scope.name for scope in scopes]}