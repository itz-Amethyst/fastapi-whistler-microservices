from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.models.base import BaseModel
from product_service.models.product import Product


class OrderItem(BaseModel):
    __tablename__ = 'order_items'
     
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete="CASCADE"), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    product_price: Mapped[float] = mapped_column(Float, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,index= True)

    product = relationship(Product, back_populates="order_items") 
    order = relationship("Order", back_populates="order_items")