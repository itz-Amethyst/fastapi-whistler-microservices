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
            return {"id": "", "status": False}
        return {"id": str(discount.id), "status": True}

    async def get(self, discount_id: str) -> Optional[DiscountResponse]:
        try:
            discount = await Discount.get(ObjectId(discount_id))
            if discount:
                discount.id = str(discount.id)
            return discount
        except Exception as e:
            # Handle or log the error as needed
            return None

    async def update(self, discount_id: str, update_data: dict) -> Optional[DiscountResponse]:
        try:
            discount = await Discount.get(ObjectId(discount_id))
            if not discount:
                return None
            await discount.update({"$set": update_data})
            return await self.get(discount_id)
        except Exception as e:
            # Handle or log the error as needed
            return None

    async def delete(self, discount_id: str) -> bool:
        try:
            discount = await Discount.find_one(Discount.id == ObjectId(discount_id))
            if not discount:
                return False
            await discount.delete()
            return True
        except Exception as e:
            # Handle or log the error as needed
            return False

    async def list(self, limit: int = 100, skip: int = 0) -> List[DiscountResponse]:
        try:
            discounts = await Discount.find().skip(skip).limit(limit).to_list()
            for discount in discounts:
                discount.id = str(discount.id)
            return discounts
        except Exception as e:
            # Handle or log the error as needed
            return []
