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

@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id :int, db: AsyncSession = Depends(DBSessionDepAsync)):
    repo = OrderRepository(db)
    order = await repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status=404, detail=f"Order with id {order_id} not found")
    return order 
