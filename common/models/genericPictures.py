from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from common.models.base import BaseModel


class GenericPictures(BaseModel):
    
    __tablename__ = 'generic_pictures'
    
    picture_url: Mapped[String] = mapped_column(String, nullable=False)
    content_type_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('content_types.id'), nullable=False)
    object_id: Mapped[Integer] = mapped_column(Integer, nullable=False)
    
    content_type = relationship("ContentType")
