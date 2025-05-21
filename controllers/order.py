from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.order import Orders
from models.orderitem import OrderItems
from schema.order import OrderCreate, OrderItemCreate, OrderResponse, OrderReadWithItems #OrderUpdate

class OrderController:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def post_order_controller(self, order:OrderCreate):
        db_order = Orders.model_validate(order)
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)
        return db_order
    
    async def get_order_by_useruid(self, user_uid: str):
        statement = select(Orders).where(Orders.user_uid == user_uid)
        orders = await self.session.exec(statement)
        
        if not orders: 
            raise HTTPException(status_code=404, detail="you don't have any orders yet!")
        
        orders = orders.all()
        return orders

    
    async def get_order_controller(self, order_uid: str) -> OrderReadWithItems:
        statement = (
            select(Orders)
            .where(Orders.uid == order_uid)
            .options(selectinload(Orders.items))  # Eagerly load the 'items' relationship
        )

        result = await self.session.exec(statement)
        order = result.first()

        if not order:
            raise HTTPException(status_code=404, detail="order with given id is not found!")

        return order
    
    async def get_order_status(self, order_uid: str):
        statement = select(Orders).where(Orders.uid == order_uid)
        order = await self.session.exec(statement)
        order = order.first()
        
        if not order:
            raise HTTPException(status_code=404, detail="order with given id not found!")
        
        current_status = order.status
        
        return {"your current order status is: ": current_status}
    
    
    async def delete_order_controller(self, order_uid: str):
        statement = select(Orders).where(Orders.uid == order_uid)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="order with given id not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "order deleted successfully!"}  # return a message to the client
    
    async def update_order_put(self, order_uid: str, data: dict):
        
        order = await self.session.get(Orders)
        
        if not order:
            raise HTTPException(status_code=404, detail="order with given id not found! ")
        
        for k, v in data.items():
            setattr(order, k, v)
            
        self.session.add(order)
        await self.session.commit()
        return {"message": "your requested operation forwarded successfully... "}
            
    
    
"""    async def update_order_controller(self, order: OrderUpdate):
        statement = select(Orders).where(order.uid == Orders.uid)
        db_order = await self.session.exec(statement)
        db_order = db_order.one()
        if order.total_price is None:
            raise HTTPException(status_code=405, detail="total_price field required")
        elif order.total_price == 0:
            raise HTTPException(status_code=405, detail="total_price field required")
        else:
            db_order.total_price = order.total_price
        
        if order.card_number is not None:
            db_order.card_number = order.card_number
        
        if order.card_expiration_date is not None:
            db_order.card_expiration_date = order.card_expiration_date
        
        if order.email is not None:
            db_order.email = order.email
        
        if order.phone is not None:
            db_order.phone = order.phone
        
        if order.address is not None:
            db_order.address = order.address
        
        if order.coupon is not None:
            db_order.coupon = order.coupon
        
        if order.discount is not None:
            db_order.discount = order.discount
        
        if order.status is not None:
            db_order.status = order.status
        
        if order.created_at is not None:
            db_order.created_at = order.created_at
        
        self.session.add(db_order)
        await self.session.commit()
        return {"massage": "success!"}"""


