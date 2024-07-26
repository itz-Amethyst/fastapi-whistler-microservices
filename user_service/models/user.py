import json
import re
from typing import List
from sqlalchemy import Boolean, String 
from common.models.base import BaseModel
from sqlalchemy.orm import validates, mapped_column, Mapped, relationship
from user_service.config import settings

class BaseModelUser(BaseModel):
    __abstract__ = True
    JSON_KEYS = {}

    async def add_fields(self):
        for field, scheme in self.JSON_KEYS.items():
            setattr(self, field, self.get_json_key(field, scheme))

    async def load_data(self):
        await self.add_related()
        await self.add_fields()

    async def _delete(self, *args, **kwargs):
        await self.delete_related()
        return await super().delete(*args, **kwargs)

    @classmethod
    async def create(cls, **kwargs):
        model = await super().create(**kwargs)
        await model.load_data()
        return model

    @classmethod
    def process_kwargs(cls, kwargs):
        return kwargs

    @classmethod
    def prepare_create(cls, kwargs):
        kwargs["id"] = cls.generate_unique_id()
        if "metadata" not in kwargs and getattr(cls, "METADATA", False):
            kwargs["metadata"] = {}
        return kwargs

    def prepare_edit(self, kwargs):
        kwargs.pop("user_id", None) 
        return kwargs

    def get_json_key(self, key, scheme):
        data = getattr(self, key) or {}
        return scheme(**data)

    async def set_json_key(self, key, scheme):
        json_data = json.dumps(getattr(self, key))
        kwargs = {key: json_data}
        await self.update(**kwargs) 



class User(BaseModelUser):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    # totp_code = mapped_column(Text, nullable=False)
    # tfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    scopes: Mapped[List["Scope"]] = relationship("Scope", secondary="user_scopes", back_populates="users")

    @validates("email")
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address: {email}")
        
        return email

    def get_scope_names(self) -> List[str]:
        return [scope.name for scope in self.scopes]
    

    def __repr__(self):
        return f"User: {self.username}, email={self.email}, is_verified: {self.is_verified}"