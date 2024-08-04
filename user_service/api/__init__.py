from user_service.api import user, auth, scopes
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"]) 

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(scopes.router)