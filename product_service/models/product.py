from sqlalchemy import Column, Float, String, Text
from common.models.base import BaseModel
from common.models.pictureMixIn import PictureMixin
from slugify import slugify 
from user_service.models.user import User
from sqlalchemy.orm import relationship 

class Product(BaseModel, PictureMixin):
    
    __tablename__ = "products"
    
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    seller = relationship(User) 

    def __init__(self, name , **kwargs):
        self.name = name
        self.slug = self.generate_slug(name)
        super().__init__(**kwargs)
        
    def generate_slug(self, name):
        return slugify(name)

    def __repr__(self):
        return f"Product: name={self.name}, price={self.price}"






# Usage 
# async def create_product_with_image():
#     async with DBSessionManager().session_async() as session:
#         # Create a new product
#         new_product = Product(name="Sample Product", description="This is a sample product.", price=100)
#         session.add(new_product)
#         await session.commit()

#         # Ensure the PictureMixin setup is done
#         Product.setup(session)

#         # Create a generic picture for the product
#         new_image = GenericPicture(
#             picture_url="http://example.com/image.jpg", 
#             content_type_id=Product.content_type_id, 
#             object_id=new_product.id
#         )
#         session.add(new_image)
#         await session.commit()

# # Running the async function
# asyncio.run(create_product_with_image())