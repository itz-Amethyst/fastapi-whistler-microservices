

from sqlalchemy import String 
from common.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column 


class ContentType(BaseModel):
    __tablename__ = "content_types"
     
    model: Mapped[str]= mapped_column(String, nullable=False, unique=True)