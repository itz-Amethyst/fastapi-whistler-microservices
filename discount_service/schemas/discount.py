from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator, validator



class DiscountBase(BaseModel):
    # todo objectid
    # id: str
    code: str
    use_count: int
    start_date: datetime
    end_date: datetime
    percentage: float

    class Config:
        orm_mode = True
        
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
        
# Todo
class UpdateDiscount(BaseModel):
    code: Optional[str]
    use_count: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    percentage: Optional[float]

    class Config:
        orm_mode = True