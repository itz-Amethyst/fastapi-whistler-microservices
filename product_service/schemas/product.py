from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from pydantic import Field, field_validator
from slugify import slugify
from common.schemes.base import BaseModel
from common.schemes.image import Image 



class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    
    
class ProductCreate(ProductBase):
    picture: Optional[UploadFile] = None

    # todo : requried checking (slugify applied on repo layer)
    # @field_validator('name')
    # def generate_slug(cls, v):
    #     return slugify(v)


class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    picture: Optional[UploadFile] = None

    
class Product(ProductBase):
    id: int
    slug: str
    seller: Optional[int]
    images: List[Image] = []
    is_deleted: bool 

    class Config:
        orm_mode = True