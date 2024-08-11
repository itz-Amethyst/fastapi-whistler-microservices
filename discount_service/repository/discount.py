from typing import List, Optional
from bson import ObjectId
from discount_service.models.discount import Discount
from discount_service.schemas import Discount as DiscountResponse
from common.utils.logger import logger_system

class DiscountRepository:
    async def create(self, discount: Discount) -> Discount:
        try:
            await discount.insert()
        except Exception as e:
            logger_system.error(e)
            return {"id": "", "status": False}
        return {"id": str(discount.id), "status": True}

    async def get(self, discount_id: str) -> Optional[DiscountResponse]:
        try:
            discount = await Discount.get(ObjectId(discount_id))
            if discount:
                discount.id = str(discount.id)
            return discount
        except Exception as e:
            logger_system.error(e)
            return None

    async def get_by_token(self, discount_token: str) -> Optional[DiscountResponse]:
        try:
            discount = await Discount.find_one(Discount.code == discount_token)
            if discount:
                discount.id = str(discount.id)
            return discount
        except Exception as e:
            logger_system.error(e)
            return None

    async def update(self, discount_id: str, update_data: dict) -> Optional[DiscountResponse]:
        try:
            discount = await Discount.get(ObjectId(discount_id))
            if not discount:
                return None
            await discount.update({"$set": update_data})
            return await self.get(discount_id)
        except Exception as e:
            logger_system.error(e)
            return None

    async def decrement_use_count(self, discount_token: str) -> Optional[Discount]:
        try:
            # in get i modified id so it's better to retrieve again here
            discount = await Discount.find_one(Discount.code == discount_token)
            if not discount:
                return None
            
            await discount.update({"$inc": {'use_count': -1}})
            updated_discount = await self.get_by_token(discount_token)
            return updated_discount
        except Exception as e:
            logger_system(f"Error updating use count: {e}")
            return None
        
    async def delete(self, discount_id: str) -> bool:
        try:
            discount = await Discount.find_one(Discount.id == ObjectId(discount_id))
            if not discount:
                return False
            await discount.delete()
            return True
        except Exception as e:
            logger_system.error(e)
            return False

    async def list(self, limit: int = 100, skip: int = 0) -> List[DiscountResponse]:
        try:
            discounts = await Discount.find().skip(skip).limit(limit).to_list()
            for discount in discounts:
                discount.id = str(discount.id)
            return discounts
        except Exception as e:
            logger_system.error(e)
            return []
