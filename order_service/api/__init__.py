from order_service.api import order
from fastapi import APIRouter


router = APIRouter()

router.include_router(order.router , tags=['Order'])