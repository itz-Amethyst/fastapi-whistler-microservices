from common.dep.db import DBSessionDepAsync
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from product_service.repository.product import ProductRepository
from product_service.schemas import Product, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.schemas.product import ProductUpdate

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
        raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
    return product

@router.get("/products/{product_slug}", response_model=Product)
async def get_product_by_slug(product_slug : str, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    product = await repo.get_product_by_slug(product_slug)
    if not product:
        raise HTTPException(status=404, detail=f"Product with slug {product_slug} not found")
    return product


@router.get("/products/", response_model=List[Product])
async def get_all_products_with_picture(db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    products = await repo.get_all_products_with_pictures()
    return products

@router.delete("/products/{product_id}", response_model=bool)
async def delete_product(product_id: int, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    success = await repo.delete_product(product_id)
    if not success:
        raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
    return success 


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, details: ProductUpdate, picture: UploadFile = None, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = ProductRepository(db)
    try:
        updated_product = await repo.update_product(product_id, details, picture)
        if not updated_product:
            raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
        return updated_product
    except Exception as e:
        raise HTTPException(status=500, detail=f"Failed to update {product_id}")