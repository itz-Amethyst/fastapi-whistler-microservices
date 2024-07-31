from user_service.api import user, auth
from fastapi import APIRouter

router = APIRouter() 

router.include_router(user.router)
router.include_router(auth.router)