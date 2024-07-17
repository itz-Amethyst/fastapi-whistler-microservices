from sqlalchemy import ForeignKey, Integer, Float, Enum as SQLAEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID 
from common.models.base import BaseModel
from user_service.models.user import User
from enum import Enum
import uuid

class OrderStatus(Enum):
    PENDING = "Pending"
    CANCELED = "Canceled"
    ACCEPTED = "Accepted"


class Order(BaseModel):
    
    # Later can change the ref alghorithm
    reference_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False) 
    status: Mapped[OrderStatus] = mapped_column(SQLAEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False) 
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="orders", uselist=False)
    
    # ?! uselist=?!
    user = relationship(User, back_populates="orders", uselist=False)
    order_items = relationship("OrderItems", backref="order")
