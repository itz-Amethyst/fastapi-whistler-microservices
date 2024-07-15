from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator
from slugify import slugify

from common.schemas.image import Image 



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
    
    class Config:
        orm_mode = True