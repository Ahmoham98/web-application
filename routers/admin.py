from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from database import get_session
from dependencies import AccessTokenBearer, RoleChecker
from controllers.admin import AdminController
from models.order import Orders
from models.product import Products
from models.user import Users
from schema.user import UsersPublic

admin_router = APIRouter()

access_token_bearer = AccessTokenBearer()
admin_checker = RoleChecker(["admin"])


@admin_router.get("/orders")
async def list_orders(
    *,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker),
):
    return await AdminController(session=session).list_all_orders()


@admin_router.put("/orders/{order_uid}/status")
async def update_order_status(
    *,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker),
    order_uid: str,
    status: str,
):
    
    if status not in ("processing", "shipped", "delivered", "cancelled"):
        raise HTTPException(status_code=404, detail="The order state is not clear! error occurred...")
    
    order = await session.get(Orders, order_uid)
    
    if not order:
        raise HTTPException(status_code=404, detail="the order you are trying to find actually doesn't exist! ")
    
    order.status = status
    session.add(order)
    await session.commit()
    return {"message": "Order status updated"}


@admin_router.get("/products/pending")
async def show_pending_products(
    *,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker)
):
    result = await AdminController(session=session).get_all_pending_products()
    return result


@admin_router.put("/products/{product_id}/status")
async def update_product_status(
    *,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker),
    product_uid: str,
    status: str,
):
    if status not in ("approved", "rejected"):
        raise HTTPException(status_code=404, detail="we don't have such status among our products. wrong status input... ")
    
    product = await session.get(Products, product_uid)
    
    if not product:
        raise HTTPException(status_code=404, detail="the is no such product for approve or reject... ")
    
    product.status = status
    session.add(product)
    await session.commit()
    return {"message": f"Product {status}"}


@admin_router.get("/users", response_model=list[UsersPublic])
async def list_users(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _:bool = Depends(admin_checker),
):
    """ 
        Handles get_all user requests and hand it over to the backend to get all the users 
            ** you need admin access for this operation **
    """

    result = await AdminController(session=session).list_all_users()
    return result


@admin_router.put("/users/{user_uid}/role")
async def update_role(
    *,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker),
    user_uid: str,
    role: str
):
    if role not in ("user", "pharmacist", "admin"):
        raise HTTPException(status_code=404, detail="we don't have such role among our wep-application. wrong role input... ")
    
    user = await session.get(Users, user_uid)
    
    if not user:
        raise HTTPException(status_code=404, detail="the is no such user for changing the role ")
    
    user.role = role
    session.add(user)
    await session.commit()
    return {"message": "Role updated"}


# Ban/unban user
@admin_router.put("/users/{user_uid}/status")
async def toggle_user_status(
    *,
    session: AsyncSession = Depends(get_session),
    user_uid: str,
    is_active: bool,
):
    user = await session.get(Users, user_uid)
    
    if not user:
        raise HTTPException(status_code=404, detail="the is no such user for banning operation ")
    
    user.is_active = is_active
    session.add(user)
    await session.commit()
    return {"message": "User status updated"}


