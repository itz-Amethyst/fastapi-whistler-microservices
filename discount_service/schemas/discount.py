from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from bson import ObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from pydantic import AfterValidator, BaseModel, Field, field_validator, model_validator, validator

def objectid_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Unserializable object {obj} of type {type(obj)}")

ENCODERS_BY_TYPE[ObjectId] = objectid_encoder

class DiscountBase(BaseModel):
    # todo objectid
    id: Optional[str]
    code: str
    use_count: int
    start_date: datetime
    end_date: datetime
    percentage: float

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: objectid_encoder
        }

class DiscountBaseWValidation(BaseModel):
    _id: int
    code: str
    use_count: int 
    start_date: datetime
    end_date: datetime
    percentage: float
    
    @validator("end_date")
    def end_date_validate(cls, v, values):
        start_date = values.get("start_date")
        if start_date:
            if start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=timezone.utc)
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= start_date:
                raise ValueError("end_date must be after start_date")
        return v

    @validator("start_date")
    def start_date_validate(cls, v):
        now = datetime.now(timezone.utc)
        if v.tzinfo is None:
            v = v.replace(tzinfo = timezone.utc)
        if v < now - timedelta(seconds = 5): 
            raise ValueError("start_date must be in the future")
        return v
    

    class Config:
        underscore_attrs_are_private = True
        
class CreateDiscount(DiscountBaseWValidation):
    pass

class Discount(DiscountBase):
    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: objectid_encoder
        } 

class UpdateDiscount(BaseModel):
    code: Optional[str] = None
    use_count: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    percentage: Optional[float] = None

    @validator("end_date", pre=True, always=True)
    def end_date_validate(cls, v, values):
        start_date = values.get("start_date")
        if start_date and v:
            if isinstance(start_date, datetime) and isinstance(v, datetime):
                if start_date.tzinfo is None:
                    start_date = start_date.replace(tzinfo=timezone.utc)
                if v.tzinfo is None:
                    v = v.replace(tzinfo=timezone.utc)
                if v <= start_date:
                    raise ValueError("end_date must be after start_date")
        return v

    @validator("start_date", pre=True, always=True)
    def start_date_validate(cls, v):
        if v:
            now = datetime.now(timezone.utc)
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v < now - timedelta(seconds=5):
                raise ValueError("start_date must be in the future")
        return v

    class Config:
        orm_mode = True