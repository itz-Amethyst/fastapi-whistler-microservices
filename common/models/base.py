from typing import TYPE_CHECKING
from common.db.session import Base
from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr 

def date_time_sec():
    return datetime.now().replace(microsecond=0)

class BaseModel(DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    # @declared_attr
    # def id(self) -> Mapped[int]:
    #     return mapped_column(primary_key=True)

    # if TYPE_CHECKING:
    #     created_time: Mapped[datetime] = mapped_column(DateTime, default=date_time_sec, nullable=False)
    #     modified: Mapped[datetime] = mapped_column(DateTime, default=date_time_sec, onupdate=date_time_sec, nullable=True)
    @declared_attr
    def created_time(self) -> Mapped[datetime]:
        return mapped_column(DateTime, default=date_time_sec, nullable=False)
    
    @declared_attr
    def modified(self) -> Mapped[datetime]:
        return mapped_column(DateTime, default=date_time_sec, onupdate=date_time_sec, nullable=True)