from typing import List
import uuid
from common.schemes.base import BaseModel
from pydantic import UUID4 
from order_service.models.order import OrderStatus
from order_service.schemas.orderItem import OrderItem, OrderItemCreate, OrderItemUpdate 

class OrderBase(BaseModel):
    reference_id : UUID4 
    total_amount: float
    status: OrderStatus 
    user_id: int
    
class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    order_items: List[OrderItemUpdate]

class Order(OrderBase):
    order_items: List[OrderItem]
    
    class Config:
        orm_mode = True