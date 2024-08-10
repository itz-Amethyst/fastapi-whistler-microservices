from common.dep.db import DBSessionDepAsync
from typing import List, Optional, Tuple, Union
from fastapi import APIRouter, Body, Depends, File, HTTPException, Request, Security, UploadFile
from product_service.repository.product import ProductRepository
from product_service.schemas import Product, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.schemas.product import ProductUpdate
from user_service.models.user import User
from user_service.utils.security.auth import AuthDependency

router = APIRouter()


@router.get("/products", response_model=List[Product])
async def get_all_products(skip:int = 0, limit:int = 10, db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    products = await repo.get_all_products_with_pictures(skip, limit)
    return products

# Todo: later add security retrive id dependency
@router.post("/products", response_model=Product)
async def create_product(req: Request, product: ProductCreate = Depends(), picture: UploadFile = File(None),
                            auth_data: Union[None, Tuple[Optional[User], str]] = Security(
                            AuthDependency(token_required=True, return_token=False), scopes=["full_control"]),
                         db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    
    product_result, success = await repo.insert_product(seller_id=int(req.session['sub']), product=product.model_dump(), picture=picture)
    if not success:
        raise HTTPException(status_code = 400, detail= product_result)

    return product_result

@router.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id :int, db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    product = await repo.get_product_with_pictures(product_id)
    if not product:
        raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
    return product

# Todo 
@router.get("/products/{product_slug}", response_model=Product)
async def get_product_by_slug(product_slug : str, db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    product_id = await repo.get_product_by_slug(product_slug)
    if not product_id:
        raise HTTPException(status_code=404, detail=f"Product with slug {product_slug} not found")
    
    product = await repo.get_product_with_pictures(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found or has no pictures")
    
    return product


@router.get("/products/", response_model=List[Product])
async def get_all_products_with_picture(db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    products = await repo.get_all_products_with_pictures()
    return products

@router.delete("/products/{product_id}", response_model=bool)
async def delete_product(product_id: int,auth_data: Union[None, Tuple[Optional[User], str]] = Security(
                            AuthDependency(token_required=True, return_token=False), scopes=["full_control"]),
                            db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    success = await repo.delete_product(product_id)
    if not success:
        raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
    return success 


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, details: ProductUpdate = Depends(), picture: UploadFile = File(None),
                            auth_data: Union[None, Tuple[Optional[User], str]] = Security(
                            AuthDependency(token_required=True, return_token=False), scopes=["full_control"]),
                         db: AsyncSession = DBSessionDepAsync):
    repo = ProductRepository(db)
    try:
        updated_product = await repo.update_product(product_id, details, picture)
        if not updated_product:
            raise HTTPException(status=404, detail=f"Product with id {product_id} not found")
        return updated_product
    except Exception as e:
        raise HTTPException(status=500, detail=f"Failed to update {product_id}")