import os
from pathlib import Path
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles

from common.utils.recursion import RecursionDepth

BYTES_SIZE: int = 1000000
CHUNK_SIZE: int = 1024 * 1024 # 1MB

class GenericPictureRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_picture(self, product_id:int ,picture: UploadFile, model_name: str):
        try:
            content_type_id = await self.get_content_type_id(model_name)
            # Todo
            base_path = f"uploads/{model_name}"
            Path(base_path).mkdir(parents = True, exist_ok = True)
            picture_filename = f"{uuid.uuid4()}.jpg" 
            picture_path = os.path.join(base_path, picture_filename)

            total_size = 0
            # override the recursion depth level to avoid infinite recursion               
            with RecursionDepth(3000):
                async with aiofiles.open(picture_path, "wb") as file:
                    while True:
                        chunk = await picture.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        file.write(chunk)
                        total_size += len(chunk)
                        if total_size > 4 * BYTES_SIZE:
                            raise HTTPException(400, {"message": "File size must be lower than 4MB"})
                
            picture_url = os.path.relpath(picture_path, start="uploads").replace(os.path.sep, '/')

            sql = text(
                """
                insert into generic_pictures (picture_url, content_type_id , object_id)
                values (:picture_url, :content_type_id ,:object_id)
                """
            )

            await self.session.execute(sql, {"picture_url": picture_url, "content_type_id": content_type_id, "object_id": product_id})
            # await self.session.commit()
        except HTTPException as http_exc:
            if os.path.exists(picture_path):
                os.remove(picture_path)
            raise http_exc 
        except Exception as e:
            await self.session.rollback()
            print(f"Something went wrong while uploading picture: {e}")
            
    async def get_content_type_id(self, model_name: str) -> int:
        try:
            sql_select = text(
                """
                select id from content_types
                where model = :model_name              
                """
            )

            result = await self.session.execute(sql_select, {"model_name": model_name})
            content_type_id = result.scalar()
            
            if content_type_id is None:
                sql_insert = text(
                    """
                    insert into content_types 
                    values (:model_name)
                    returning id
                    """
                )
                
                result = await self.session.execute(sql_insert, {"model_name": model_name})
                content_type_id = result.scalar()
                # await self.session.commit()
                
            return content_type_id
        except Exception as e:
            await self.session.rollback()
            print("Something went wrong: {e}")
        
            return None
        