from typing import Any, Dict, List, Optional
from fastapi import UploadFile
from slugify import slugify
from sqlalchemy import delete, update, insert, text
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
from product_service.models.product import Product as ProductModel
from user_service.models.user import User
from user_service.models.token import Token 

class UserRepository:
    
    def __init__(self, sess: Session) -> None:
        self.session: Session = sess
    
    async def get_user_and_token(self, token_value: str):
        sql = select(User, Token).join(User, User.token_id == Token.id).where(Token.token_value == token_value)
        result = await self.session.execute(sql)
        
        user, token = result.first()
        
        return user, token
        