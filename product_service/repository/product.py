from typing import List
from fastapi import UploadFile
from slugify import slugify
from sqlalchemy import delete, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
from product_service.models.product import Product

class ProductRepository:
    
    def __init__(self, sess: Session) -> None:
        self.session: Session = sess


    async def get_all_products(self, skip:int = 0 , limit:int = 10) ->List[Product]:
        try:
            sql = text("select * from products order by id offset :skip limit :limit")
            result = await self.session.execute(sql, {"skip": skip, "limit": limit})
            products = result.mappings().all()
            return [Product(**product) for product in products]
        except Exception as e:
            print(f"Error fetching data: {e}")
            return 