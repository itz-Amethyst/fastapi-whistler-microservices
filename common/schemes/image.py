from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    
    picture_url: str
    object_id:int
    content_type_id: int