from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

from common.models.base import BaseModel


class GenericPictures(BaseModel):
    
    __tablename__ = 'generic_pictures'
    
    picture_url = Column(String, nullable=False)
    content_type_id = Column(Integer, ForeignKey('content_types.id'), nullable=False)
    object_id = Column(Integer, nullable=False)
    
    content_type = relationship("ContentType")
