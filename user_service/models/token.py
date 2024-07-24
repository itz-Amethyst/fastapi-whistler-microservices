from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Integer, String
from common.models.base import BaseModel


class Token(BaseModel):
    __tablename__ = "tokens"

    token_value = mapped_column(String, nullable=False) 