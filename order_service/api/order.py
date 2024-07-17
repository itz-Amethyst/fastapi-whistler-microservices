from common.dep.db import DBSessionDepAsync
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from order_service.repository.order import OrderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.schemas import Order, OrderCreate, OrderUpdate

router = APIRouter()


# @router.get("/products", response_model=List[Product])
# async def get_all_products(skip:int = 0, limit:int = 10, db: AsyncSession = Depends(DBSessionDepAsync)):
#     repo = ProductRepository(db)
#     products = await repo.get_all_products(skip=skip, limit=limit)
#     return products

# Todo: later add security retrive id dependency
@router.post("/orders", response_model=Order)
async def create_product(req: Request, order: OrderCreate, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = OrderRepository(db)
    created_order = await repo.create_order(order) 
    if not created_order:
        raise HTTPException(status_code = 400, detail= "order creation Failed")

    return created_order 

@router.put("/order/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderUpdate, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = OrderRepository(db)
    updated_order = repo.update_order(order_id, order)
        
    if not updated_order:
        raise HTTPException(status=404, detail=f"Order with id {order_id} not found")
    
    return updated_order

@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id :int, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = OrderRepository(db)
    order = await repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status=404, detail=f"Order with id {order_id} not found")
    return order 

@router.get("/orders/{reference_id}", response_model=Order)
async def get_order_by_reference_id(reference_id : str, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = OrderRepository(db)
    order = await repo.get_order_by_reference_id(reference_id)
    if not order:
        raise HTTPException(status=404, detail=f"Order with reference id {reference_id} not found")
    return order 
