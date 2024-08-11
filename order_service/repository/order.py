from datetime import datetime
from typing import Optional, Union
import uuid
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from common.config import settings
from discount_service.schemas.discount import Discount
from order_service.repository.orderItems import OrderItemsRepository
from order_service.schemas import OrderCreate, Order, OrderUpdate
from common.utils.logger import logger_system
from product_service.schemas.product import Product


class OrderRepository:
    
    def __init__(self, sess: AsyncSession) -> None:
        self.session = sess
        self.orderItemsRepo = OrderItemsRepository(sess)
        self.http_client = httpx.AsyncClient()
    
    async def _make_request(self, method: str, endpoint: str, json: Optional[dict] = None) -> Optional[dict]:
        try:
            url = f"{settings.BASE_URL}/{endpoint}"
            if method in ["GET", "POST", "PUT", "DELETE"]:
                response = await self.http_client.request(method, url, json=json)
            else:
                raise ValueError(f"Unsupported value {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request to {url} failed with status code {response.status_code}")
                raise HTTPException(status_code=response.status_code, detail="Resource not found")
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while making the request")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred")

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        endpoint = f"product_service/products/{product_id}"
        response_data = await self._make_request("GET", endpoint)
        return Product(**response_data) if response_data else None

    async def get_discount_by_id(self, discount_id: str) -> Optional[Discount]:
        endpoint = f"discount_service/discounts/{discount_id}"
        response_data = await self._make_request("GET", endpoint)
        return Discount(**response_data) if response_data else None

    async def decrement_discount_use_count(self, discount_id: str) -> bool:
        endpoint = f"discount_service/discounts/use_count/{discount_id}"
        response_data = await self._make_request("PUT", endpoint)
        return response_data is not None


    async def check_pending_order(self, user_id: int) -> bool:
        sql = text(
            """
            select 1 from orders where user_id = :user_id AND status = 'PENDING' limit 1
            """
        )
        result = await self.session.execute(sql, {'user_id': user_id})
        return result.scalar() is not None
    
    async def create_order(self, user_id:int, order: OrderCreate) -> Union[bool,Optional[Order]]:
        try:
            if await self.check_pending_order(user_id):
                return True, None
            
            total_amount = 0.0
            updated_order_items = []
            for item in order.order_items:
                product = await self.get_product_by_id(item.product_id)
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
                
                total_amount += product.price * item.quantity
                product_price = product.price
                updated_order_items.append({
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'product_price': product_price
                })
                
                
            # Apply discount if provided
            is_discount_used = False
            discount_amount = 0.0
            if order.discount_token:
                discount = await self.get_discount_by_id(order.discount_token)
                if not discount or discount.use_count <= 0:
                    raise HTTPException(status_code=404, detail=f"Discount with token {order.discount_token} not found")

                if discount.start_date <= datetime.utcnow() <= discount.end_date:
                    discount_amount = total_amount * (discount.percentage / 100)
                    is_discount_used = True
                    if not await self.decrement_discount_use_count(order.discount_token):
                        raise HTTPException(status_code=500, detail="Failed to update discount use count")
                else:
                    raise HTTPException(status_code=400, detail="Discount token is expired")
            else:
                discount_amount = 0.0
            
            total_amount_with_discount = total_amount - discount_amount
            
            
            order_data = {
                'reference_id': str(uuid.uuid4()),
                'total_amount': total_amount,
                'status': 'PENDING',
                'user_id': user_id,
                'is_discount_used': is_discount_used,
                'total_amount_with_discount': total_amount_with_discount if is_discount_used else total_amount
            }
            sql = text(
                """
                insert into orders (reference_id, total_amount, status, user_id, is_discount_used, total_amount_with_discount)
                values (:reference_id, :total_amount, :status, :user_id, :is_discount_used, :total_amount_with_discount)
                returning id ,reference_id, total_amount, status, user_id
                """
            )
            result = await self.session.execute(sql, order_data)
            # mapping
            db_order = result.fetchone()
            if not db_order:
                return False, None
            
            await self.orderItemsRepo.create_order_items(db_order.id, updated_order_items)
            await self.session.commit()

            return False, await self.get_order_by_id(db_order.id)
        except Exception as e:
            await self.session.rollback()
            logger_system.error(f"Something went worng while creating order: {e}")
    
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
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id, o.modified, o.created_time, o.is_discount_used, o.total_amount_with_discount,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                where o.id = :order_id
                """
            )
            result = await self.session.execute(sql, {"order_id": order_id})
            rows = result.mappings().all()
            
            if not rows:
                return None
            
            order_data = self._extract_order_data(rows)
            logger_system.info(**order_data)
            return Order(**order_data)            

        except Exception as e:
            print(f"Error fetching order by id: {e}")
            return None 
    
    async def get_order_by_reference_id(self, reference_id: uuid.UUID) -> Optional[Order]:
        try:
            sql = text(
                """
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id, o.modified, o.created_time, o.is_discount_used, o.total_amount_with_discount,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                where o.reference_id = :reference_id
                """
            )
            result = await self.session.execute(sql, {"reference_id": reference_id})
            rows = result.mappings().all()
            
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
                select o.id, o.reference_id, o.total_amount, o.status, o.user_id, o.modified, o.created_time, o.is_discount_used, o.total_amount_with_discount,
                   oi.id as order_item_id, oi.product_id, oi.quantity, oi.product_price 
                from orders o
                left join order_items oi on o.id = oi.order_id
                order by o.id
                offset :skip limit :limit
                """
            )
            result = await self.session.execute(sql, {"skip": skip, "limit": limit})
            rows = result.mappings().all()
            
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
        try:
            if not rows:
                raise ValueError("No rows provided to extract order data.")

            first_row = rows[0]

            order_data = {
                "id": first_row["id"],
                "reference_id": first_row["reference_id"],
                "total_amount": first_row["total_amount"],
                "status": first_row["status"],
                "user_id": first_row["user_id"],
                "created_time": first_row["created_time"],
                "modified": first_row["modified"],
                "is_discount_used": first_row['is_discount_used'],
                "total_amount_with_discount": first_row['total_amount_with_discount']
            }

            order_items = [
                {
                    "id": row["order_item_id"],
                    "product_id": row["product_id"],
                    "quantity": row["quantity"],
                    "product_price": row["product_price"],
                }
                for row in rows
                if row.get("order_item_id")
            ]

            order_data['order_items'] = order_items
            return order_data

        except Exception as e:
            logger_system.error(f"Error extracting order data: {e}")
            return {}