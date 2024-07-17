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

@router.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id :int, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    product = await repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status=404, detail="Product with id {product_id} not found")
    return product

@router.get("/products/{product_slug}", response_model=Product)
async def get_product_by_slug(product_slug : str, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    product = await repo.get_product_by_slug(product_slug)
    if not product:
        raise HTTPException(status=404, detail="Product with id {product_id} not found")
    return product


@router.get("/products/", response_model=List[Product])
async def get_all_products_with_picture(db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    products = await repo.get_all_products_with_pictures()
    if not products:
        raise HTTPException(status=404, detail="Product with id {product_id} not found")
    return products