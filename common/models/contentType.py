

from sqlalchemy import Column, String 
from common.models.base import BaseModel


class ContentType(BaseModel):
    __tablename__ = "content_types"
     
    model = Column(String, nullable=False, unique=True)