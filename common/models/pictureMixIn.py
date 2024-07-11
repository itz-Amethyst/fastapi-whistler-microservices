from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from common.models.contentType import ContentType

class PictureMixin:
    
    content_type_id = Column(Integer, ForeignKey("content_types.id"), nullable=True)
    object_id = Column(Integer, nullable=True)
    images = relationship("GenericPictures", 
                          primaryjoin="and_(GenericPicture.content_type_id==foreign(PictureMixin.content_type_id), foreign(GenericPicture.object_id)==PictureMixin.object_id)",
                          viewonly=True)
    
    
    @classmethod
    def setup(cls, session: Session):
        model_name = cls.__tablename__
        
        
        content_type = session.query(ContentType).filter_by(model = model_name).first()
        if not content_type:
            content_type = ContentType(model = model_name)
            session.add(content_type)
            session.commit()
            
        # to set the contenttype id for next usage
        cls.content_type_id = content_type.id