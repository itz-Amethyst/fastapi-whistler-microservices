from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator 

class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, schema_field):
        return schema_field.update(type="string")


class Discount(BaseModel):
    
    id: Optional[PyObjectId] = Field(alias='_id')
    code: str
    use_count: int
    start_date: datetime
    end_date: datetime
    percentage: float
    # user id
    created_by: int


    # Todo UTC support
    @field_validator("end_date")
    def end_date_validate(cls, v, values):
        start_date = values.get("start_date")
        if start_date and v <= start_date:
            raise ValueError("end_date must be after start_date")
        return v


    @field_validator("start_date")
    def start_date_validate(cls, v):
        if v < datetime.now(): 
            raise ValueError("start_date must be in the future")
        return v

    class Config:
        arbitray_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v : v.isoformat()
        }
        
        schema_extra = {
            "example":{
                "code": "NEW YEAR",
                "use_count": 10,
                "start_date": "2024-06-01T00:00:00",
                "end_date": "2024-08-31T22:22:22",
                "percentage": 20.0,
                "created_by": 1
            }
        }
    