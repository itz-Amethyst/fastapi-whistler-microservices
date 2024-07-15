from product_service.api import product
from fastapi import APIRouter


router = APIRouter()

router.include_router(product.router , tags=['Product'])