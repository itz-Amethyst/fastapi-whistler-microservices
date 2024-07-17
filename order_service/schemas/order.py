from typing import List
import uuid
from common.models.base import BaseModel
from order_service.schemas import OrderItemCreate, OrderItem , OrderItemUpdate

class OrderBase(BaseModel):
    reference_id : uuid.UUID
    total_amount: float
    status: str
    user_id: int
    
class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    order_items: List[OrderItemUpdate]

class Order(OrderBase):
    order_items: List[OrderItem]
    
    class Config:
        orm_mode = True