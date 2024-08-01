from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declared_attr 

from common.models.contentType import ContentType

class PictureMixin:
    # decide later to remove this fields or not
    # Note: without declared's it's gonna throw and error due to abstract rule
    @declared_attr
    def content_type_id(cls):
        return Column(Integer, ForeignKey("content_types.id"), nullable=True)
    
    @declared_attr
    def object_id(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def images(cls):
        return relationship("GenericPicture",
                            primaryjoin=(
                                "and_(GenericPicture.content_type_id==foreign(PictureMixin.content_type_id), "
                                "foreign(GenericPicture.object_id)==PictureMixin.object_id)"
                            ),
                            viewonly=True)
    
    
    @classmethod
    def setup(cls, session: Session):
        if hasattr(cls, '__tablename__'):
            model_name = cls.__tablename__
            
            
            content_type = session.query(ContentType).filter_by(model = model_name).first()
            if not content_type:
                content_type = ContentType(model = model_name)
                session.add(content_type)
                session.commit()
                
            # to set the contenttype id for next usage
            cls.content_type_id = content_type.id
        else:
            pass