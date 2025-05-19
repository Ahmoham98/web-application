from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.order import Orders
from models.product import Products
from models.user import Users

class AdminController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list_all_users(self):
        statement = select(Users)
        result = await self.session.exec(statement)
        result = result.all()
        
        if not result:
            raise HTTPException(status_code=404, detail="not any user found :O ")
        
        return result
    
    async def list_all_orders(self):
        statement = select(Orders)
        orders = await self.session.exec(statement)
        orders = orders.all()
        
        if not orders:
            raise HTTPException(status_code=404, detail="no order found here ")
        
        return orders

    async def get_order_by_uid(self, order_uid: str):
        statement = select(Orders).where(Orders.uid == order_uid)
        order = await self.session.exec(statement)
        
        if not order:
            raise HTTPException(status_code=404, detail="the order you are trying to find actually doesn't exist! ")
        
        return order
    
    async def get_all_pending_products(self):
        statement = select(Products).where(Products.status == "pending")
        result = await self.session.exec(statement)
        result = result.all()
        
        if not result:
            raise HTTPException(status_code=404, detail="we don't have any product pending here :)")
        
        return result

