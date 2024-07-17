from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.schemas import OrderItemCreate


class OrderItemsRepository:
    
    def __init__(self, sess: AsyncSession) -> None:
        self.session = sess

        
    async def create_order_items(self, order_id: int, order_items: List[OrderItemCreate]) -> None:
        try:
            for item in order_items:
                item_data = jsonable_encoder(item)
                item_data['order_id'] = order_id
                sql_order = text(
                    """
                    insert into order_items (order_id, product_id, quantity, product_price)
                    values (:order_id, :product_id, :quantity, :product_price)
                    """
                )

                await self.session.execute(sql_order, item_data)
                await self.session.commit()

        except Exception as e:
            await self.session.rollback()
            print(f"Something went worng while creating order_items: {e}")

    async def delete_order_items(self, order_id: int) -> None:
        sql = text(
            """
            delete from order_items where order_id = :order_id
            """
        )
        
        await self.session.execute(sql, {"order_id": order_id})
        await self.session.commit()