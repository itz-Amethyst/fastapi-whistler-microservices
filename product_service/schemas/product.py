from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from pydantic import Field, field_validator, BaseModel as pydantic_model
from slugify import slugify
from common.schemes.base import BaseModel
from common.schemes.image import Image 



class ProductBase_For_Response(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    created_time: datetime
    modified: Optional[datetime] = None
    
class ProductBase(pydantic_model):
    name: str
    description: Optional[str] = None
    price: float
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]

    
class Product(ProductBase_For_Response):
    id: int
    slug: str
    seller_id: Optional[int]
    images: List[Image] = []
    is_deleted: bool 

    class Config:
        orm_mode = True