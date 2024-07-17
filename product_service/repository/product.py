from typing import Any, Dict, List, Optional
from fastapi import UploadFile
from slugify import slugify
from sqlalchemy import delete, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
from common.schemas.image import Image
from product_service.models.product import Product, Product
from common.repository.genericPicture import GenericPictureRepository

class ProductRepository:
    
    def __init__(self, sess: Session) -> None:
        self.session: Session = sess


    #fix seller_id later to retrieve real data
    async def insert_product(self, seller_id: int, product, picture: UploadFile = None) -> bool:
        try:
            product.slug = slugify(product.name)
            sql = text(
                """
                    insert into products (name, slug, description, price, seller_id)
                    values(:name, :slug, :description, :price, :seller_id)
                    returning id
                """) 
            result = await self.session.execute(sql,{**product , "seller_id": seller_id})
            product_id = result.fetchone()[0]
            
            if picture:
                generic_repo = GenericPictureRepository(session= self.session)
                generic_repo.add_picture(product_id, picture, model_name = Product.__tablename__)

            await self.session.commit()

            data = await self.get_product_with_pictures(product_id)
            return data, True
        except Exception as e :
            await self.session.rollback()
            print(f"Error while creating product: {e}")
            return False
            
    async def get_all_products(self, skip:int = 0 , limit:int = 10) ->List[Product]:
        try:
            sql = text("select * from products order by id offset :skip limit :limit")
            result = await self.session.execute(sql, {"skip": skip, "limit": limit})
            products = result.mappings().all()
            return [Product(**product) for product in products]
        except Exception as e:
            print(f"Error fetching data: {e}")
            return [] 


    async def get_product_with_pictures(self, product_id: int) -> Optional[Product]:
        try:
            sql = text(
                """
                select p.id, p.name, p.slug, p.descriptionSELECT p.id, p.name, p.slug, p.description, p.price, p.seller_id,
                       gp.picture_url, gp.content_type_id, gp.object_id
                from products p
                left join generic_pictures gp on p.id = gp.object_id
                where p.id = :product_id
                """
            )
            
            result = await self.session.execute(sql, {"product_id": product_id})
            rows = result.fetchall()

            if not rows:
                return None
            
            product_data = rows[0]
           
            product_dict = {k: product_data[k] for k in product_data.keys() if k != "picture_url"} 
            
            product_dict['images'] = [] 
            
            for row in rows:
                if row['picture_url']:
                    image = Image(
                        picture_url = row['picture_url'],
                        content_type_id=row["content_type_id"],
                        object_id = row['object_id']
                    )
                    product_dict['images'].append(image)
                    
            return Product(**product_dict)
        except Exception as e:
            await self.session.rollback()
            print("Something went wrong while fetching product with pictures: {e}")
            return None
        