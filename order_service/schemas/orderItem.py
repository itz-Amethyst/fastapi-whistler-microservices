from common.schemas.base import BaseModel

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    product_price: float

class OrderItem(OrderItemBase):
    pass

    class Config:
        orm_mode = True


class OrderItemCreate(OrderItemBase):
    pass 

class OrderItemUpdate(OrderItemBase):
    pass