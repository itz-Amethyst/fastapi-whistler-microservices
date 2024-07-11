from common.models.session import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer

def date_time_sec():
    return datetime.now().replace(microsecond=0)


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_time = Column(DateTime, default=date_time_sec, nullable=False)
    modified = Column(DateTime, default=date_time_sec, onupdate=date_time_sec, nullable=True)