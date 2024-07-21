from typing import List
from fastapi import APIRouter, HTTPException
from discount_service.repository.discount import DiscountRepository
from discount_service.models import Discount as DiscountModel
from discount_service.schemas import CreateDiscount, UpdateDiscount, Discount


router = APIRouter()
repository = DiscountRepository()

@router.post("/discounts/", response_model=dict)
async def create_discount(discount: CreateDiscount):
    discount = DiscountModel(**discount.model_dump())
    print(discount)
    result = await repository.create(discount)
    
    if not result['status']:
        raise HTTPException(status_code=500, detail="Failed to create discount")

@router.get("/discounts/{discount_id}", response_model=Discount)
async def read_discount(discount_id: str):
    discount = await repository.get(discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

@router.put("/discounts/{discount_id}", response_model=Discount)
async def update_discount(discount_id: str, update_data: UpdateDiscount):
    update_dict = update_data.model_dump(exclude_unset=True)
    discount = await repository.update(discount_id, update_dict)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

@router.delete("/discounts/{discount_id}", response_model=dict)
async def delete_discount(discount_id: str):
    success = await repository.delete(discount_id)
    if not success:
        raise HTTPException(status_code=404, detail="Discount not found")
    return {"detail": "Discount deleted"}

@router.get("/discounts/", response_model=List[Discount])
async def list_discounts(limit: int = 100, skip: int = 0):
    return await repository.list(limit, skip)