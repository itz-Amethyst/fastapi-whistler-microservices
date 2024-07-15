from common.dep.db import DBSessionDepAsync
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from product_service.repository.product import ProductRepository
from product_service.schemas import Product, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/products", response_model=List[Product])
async def get_all_products(skip:int = 0, limit:int = 10, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    products = await repo.get_all_products(skip=skip, limit=limit)
    return products

# Todo: later add security retrive id dependency
@router.post("/products", response_model=Product)
async def create_product(req: Request, product: ProductCreate, picture: UploadFile = None, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    product_result, success = await repo.insert_product(product.model_dump(), picture)
    if not success and not product_result:
        raise HTTPException(status_code = 400, detail= "Error while creating a product")

    return product_result