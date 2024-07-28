from common.db.session import Base
from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

def date_time_sec():
    return datetime.now().replace(microsecond=0)


class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    created_time: Mapped[datetime] = mapped_column(DateTime, default=date_time_sec, nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime, default=date_time_sec, onupdate=date_time_sec, nullable=True)