from typing import List
from sqlalchemy import Column, Integer, String
from common.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Scope(BaseModel):
    __tablename__ = "scopes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    users: Mapped[List["User"]] = relationship("User", secondary="user_scopes", back_populates="scopes")