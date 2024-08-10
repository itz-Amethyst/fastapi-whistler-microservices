from pydantic import BaseModel 

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    product_price: float

class OrderItem(OrderItemBase):
    id: int
    
    class Config:
        orm_mode = True


class OrderItemCreate(OrderItemBase):
    pass 

class OrderItemUpdate(OrderItemBase):
    pass