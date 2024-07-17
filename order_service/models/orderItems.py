from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.models.base import BaseModel
from product_service.models.product import Product


class OrderItem(BaseModel):
    __tablename__ = 'order_items'
     
    product_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), index=True, nullable=False)
    quantity: Mapped[Integer] = mapped_column(Integer, nullable=False)
    product_price: Mapped[Float] = mapped_column(Float, nullable=False)

    product = relationship(Product, back_populates="order_items") 