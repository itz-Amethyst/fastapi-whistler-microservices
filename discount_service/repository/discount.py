from typing import List, Optional
from bson import ObjectId
from discount_service.models.discount import Discount
from discount_service.schemas import Discount as DiscountResponse

class DiscountRepository:
    async def create(self, discount: Discount) -> Discount:
        try:
            await discount.insert()
        except Exception as e:
            print(e)
            return False 
        return True

    async def get(self, discount_id: str) -> Optional[DiscountResponse]:
        try:
            return await Discount.get(ObjectId(discount_id))
        except Exception as e:
            # Handle or log the error as needed
            return None

    async def update(self, discount_id: str, update_data: dict) -> Optional[DiscountResponse]:
        try:
            discount = await self.get(discount_id)
            if not discount:
                return None

            await discount.update({"$set": update_data})
            return await self.get(discount_id)
        except Exception as e:
            # Handle or log the error as needed
            return None

    async def delete(self, discount_id: str) -> bool:
        try:
            result = await Discount.delete_one(Discount.id == ObjectId(discount_id))
            return result.deleted_count > 0
        except Exception as e:
            # Handle or log the error as needed
            return False

    async def list(self, limit: int = 100, skip: int = 0) -> List[DiscountResponse]:
        try:
            return await Discount.find().skip(skip).limit(limit).to_list()
        except Exception as e:
            # Handle or log the error as needed
            return []
