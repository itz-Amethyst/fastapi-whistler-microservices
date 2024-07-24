from datetime import datetime
from pydantic import BaseModel as BaseModelPydantic, Field



class BaseModel(BaseModelPydantic):
    _id: int = Field(description="Unique id")
    modified: datetime = Field(description="Modified date")
    created_time: datetime = Field(description="Created datetime")

    
    class Config:
        underscore_attrs_are_private = True