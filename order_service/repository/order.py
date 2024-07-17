from typing import Optional
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from order_service.repository.orderItems import OrderItemsRepository
from order_service.schemas import OrderCreate, Order, OrderUpdate


class OrderRepository:
    
    def __init__(self, sess: AsyncSession) -> None:
        self.session = sess
        self.orderItemsRepo = OrderItemsRepository(sess)
    
    
    async def create_order(self, order: OrderCreate) -> Optional[Order]:
        try:
            order_data = jsonable_encoder(order, exclude={"order_items"})
            sql = text(
                """
                insert into orders (reference_id, total_amount, status, user_id)
                values (:reference_id, :total_amount, :status, :user_id)
                returning id ,reference_id, total_amount, status, user_id
                """
            )
            result = await self.session.execute(sql, order_data)
            db_order = result.fetchone()
            if not db_order:
                return None
            
            await self.orderItemsRepo.create_order_items(db_order.id, order.order_items)
            await self.session.commit()

            return await self.get_order_by_id(db_order.id)
        except Exception as e:
            await self.session.rollback()
            print(f"Something went worng while creating order: {e}")
    
    async def update_order(self, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
        try:
            order_data = jsonable_encoder(order_update, exclude={"order_items"})
            sql = text(
                """
                update orders
                set reference_id = :reference_id,
                    total_amount = :total_amount,
                    status = :status
                where id = :order_id
                returning id, reference_id, total_amount, status, user_id
                """
            )
            result = await self.session.execute(sql, order_data)
            db_order = result.fetchone()
            if not db_order:
                None
            
            await self.orderItemsRepo.delete_order_items(order_id)
            await self.orderItemsRepo.create_order_items(order_id, order_update.order_items)
            await self.session.commit()

            return await self.get_order_by_id(order_id)

        except Exception as e:
            await self.session.rollback()
            print(f"Something went worng while updating order: {e}")
    
    async def delete_order(self, order_id: int) -> bool:
        try:
            await self.orderItemsRepo.delete_order_items(order_id)
            sql = text(
                """
                delete from orders where id = :order_id 
                """
            )

            await self.session.execute(sql, {"order_id": order_id})
            await self.session.commit()
            return True
        
        except Exception as e:
            await self.session.rollback()
            print(f"Something went worng while deleting order: {e}")
            return False
    
    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        try:
            sql = text(
                """
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                where o.id = :order_id
                """
            )
            result = await self.session.execute(sql, {"order_id": order_id})
            rows = result.fetchall()
            
            if not rows:
                return None
            
            order_data = self._extract_order_data(rows)
            return Order(**order_data)            

        except Exception as e:
            print(f"Error fetching order by id: {e}")
            return None 
    
    async def get_order_by_reference_id(self, reference_id: uuid.UUID) -> Optional[Order]:
        try:
            sql = text(
                """
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                where o.reference_id = :reference_id
                """
            )
            result = await self.session.execute(sql, {"reference_id": reference_id})
            rows = result.fetchall()
            
            if not rows:
                return None
            
            order_data = self._extract_order_data(rows)
            return Order(**order_data)            

        except Exception as e:
            print(f"Error fetching order by reference_id: {e}")
            return None 
        
    
    async def get_all_orders(self, skip: int = 0, limit: int = 10) -> list[Order]:
        try:
            sql = text(
                """
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                order by o.id
                offset :skip limit :limit
                """
            )
            result = await self.session.execute(sql, {"skip": skip, "limit": limit})
            rows = result.fetchall()
            
            orders = []
            current_order_id = None
            current_order_rows = [] 
            
            for row in rows:
                if row['id'] != current_order_id:
                    if current_order_rows:
                        order_data = self._extract_order_data(current_order_rows)
                        orders.append(Order(**order_data))

                    current_order_id = row['id']
                    current_order_rows = []
                current_order_rows.append(row)

            if current_order_rows:
                order_data = self._extract_order_data(current_order_rows)
                orders.append(Order(**order_data))

            return orders
        except Exception as e:
            print(f"Error fetching all orders: {e}")
            return []

    def _extract_order_data(self, rows) -> dict:
        order_data = dict(rows[0])
        order_items = [
            {
                "id": row["order_item_id"],
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "product_price": row["product_price"]
                
            } for row in rows if row['order_item_id']
        ] 
        order_data['order_items'] = order_items
        return order_data
