from datetime import datetime
from pydantic import BaseModel as BaseModelPydantic, Field, PrivateAttr



class BaseModel(BaseModelPydantic):
    _id: int = PrivateAttr() 
    modified: datetime = Field(description="Modified date")
    created_time: datetime = Field(description="Created datetime")

    
    class Config:
        underscore_attrs_are_private = True

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value