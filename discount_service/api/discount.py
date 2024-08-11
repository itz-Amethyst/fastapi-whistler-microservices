from typing import List, Optional, Tuple, Union
from fastapi import APIRouter, HTTPException, Security
from discount_service.repository.discount import DiscountRepository
from discount_service.models import Discount as DiscountModel
from discount_service.schemas import CreateDiscount, UpdateDiscount, Discount
from user_service.models.user import User
from user_service.utils.security.auth import AuthDependency


router = APIRouter()
repository = DiscountRepository()

@router.post("/discounts/", response_model=dict)
async def create_discount(discount: CreateDiscount, auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"])):

    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    discount = DiscountModel(**discount.model_dump())
    print(discount)
    result = await repository.create(discount)
    
    if not result['status']:
        raise HTTPException(status_code=500, detail="Failed to create discount")
    return result

@router.get("/discounts/{discount_id}", response_model=Discount)
async def read_discount(discount_id: str):
    discount = await repository.get(discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

@router.put("/discounts/use_count/{discount_id}", response_model=Discount)
async def update_use_count(discount_id: str):
    discount = await repository.decrement_use_count(discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

@router.put("/discounts/{discount_id}", response_model=Discount)
async def update_discount(discount_id: str, update_data: UpdateDiscount, auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"])):

    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = update_data.model_dump(exclude_unset=True)
    discount = await repository.update(discount_id, update_dict)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

@router.delete("/discounts/{discount_id}", response_model=dict)
async def delete_discount(discount_id: str, auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"])):

    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    success = await repository.delete(discount_id)
    if not success:
        raise HTTPException(status_code=404, detail="Discount not found")
    return {"detail": "Discount deleted"}

@router.get("/discounts/", response_model=List[Discount])
async def list_discounts(limit: int = 100, skip: int = 0, auth_data: Union[None, Tuple[Optional[User], str]] = Security(
        AuthDependency(token_required=True, return_token=False), scopes=["full_control"])):

    if not auth_data:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await repository.list(limit, skip)