from uuid import UUID
from pydantic import UUID4
from common.dep.db import DBSessionDepAsync
from typing import List, Optional, Tuple, Union
from fastapi import APIRouter, Depends, HTTPException, Request, Security, UploadFile
from order_service.repository.order import OrderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.schemas import Order, OrderCreate, OrderUpdate
from user_service.models.user import User
from user_service.utils.security.auth import AuthDependency

router = APIRouter()


@router.get("/orders", response_model=List[Order])
async def get_all_orders(skip:int = 0, limit:int = 10, db: AsyncSession = DBSessionDepAsync):
    repo = OrderRepository(db)
    orders = await repo.get_all_orders(skip=skip, limit=limit)
    return orders 

@router.post("/orders", response_model=Order)
async def create_order(req: Request, order: OrderCreate,
                            auth_data: Union[None, Tuple[Optional[User], str]] = Security(
                            AuthDependency(token_required=True, return_token=False), scopes=["full_control"]),
                       db: AsyncSession = DBSessionDepAsync):
    repo = OrderRepository(db)
    created_order = await repo.create_order(user_id=int(req.session['sub']), order=order) 
    if not created_order:
        raise HTTPException(status_code = 400, detail= "order creation Failed")

    return created_order 

@router.put("/order/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderUpdate, db: AsyncSession = DBSessionDepAsync):
    repo = OrderRepository(db)
    updated_order = repo.update_order(order_id, order)
        
    if not updated_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    return updated_order

@router.get("/orders/id/{order_id}", response_model=Order)
async def get_order_by_id(order_id :int, db: AsyncSession = DBSessionDepAsync):
    repo = OrderRepository(db)
    order = await repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order 

@router.get("/orders/reference/{reference_id}", response_model=Order)
async def get_order_by_reference_id(reference_id : str, db: AsyncSession = DBSessionDepAsync):
    repo = OrderRepository(db)
    order = await repo.get_order_by_reference_id(reference_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with reference id {reference_id} not found")
    return order 
