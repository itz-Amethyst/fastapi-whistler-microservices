from typing import List, Optional
import uuid
from common.schemes.base import BaseModel
from pydantic import BaseModel as pydantic_basemodel
from pydantic import UUID4 
from order_service.models.order import OrderStatus
from order_service.schemas.orderItem import OrderItem, OrderItemCreate, OrderItemUpdate 

class OrderBase_Without_Pydantic(BaseModel):
    reference_id : UUID4 
    total_amount: float
    status: OrderStatus 
    user_id: int
    discount_token: Optional[str] = None
    
class OrderCreate(BaseModel):
    discount_token: Optional[str]
    order_items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    order_items: List[OrderItemUpdate]

class Order(OrderBase_Without_Pydantic):
    order_items: List[OrderItem]
    
    class Config:
        orm_mode = True