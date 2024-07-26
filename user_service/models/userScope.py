from sqlalchemy import ForeignKey, Integer
from common.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class UserScope(BaseModel):
    __tablename__ = "user_scopes"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    scope_id: Mapped[int] = mapped_column(Integer, ForeignKey('scopes.id'), primary_key=True)