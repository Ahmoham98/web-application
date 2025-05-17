#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

#//////////////////// Asyncsession ////////////////////////
from  database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.order import OrderItemCreate, OrderCreate, OrderResponse, OrderReadWithItems
from models.order import Orders
from models.product import Products
from models.orderitem import OrderItems
from models.user import Users

#//////////////////// Controllers class importation ////////////////////////
from controllers.order import OrderController

#//////////////////// dependencies importation ////////////////////////
from dependencies import AccessTokenBearer, RoleChecker


access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])


router = APIRouter(
)

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order = Orders(user_uid=current_user['user']['user_uid'], total_price=0)

    async with session.begin():  # handles commit/rollback automatically
        session.add(order)
        await session.flush()  # ensure order gets a UID before we use it in items
        await session.refresh(order)

        for item in order_data.items:
            product = await session.get(Products, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            price = product.sale_price or product.unit_price
            total += price * item.quantity

            order_item = OrderItems(
                order_uid=order.uid,
                product_uid=item.product_id,
                quantity=item.quantity,
                unit_price=price
            )
            session.add(order_item)

        order.total_price = total
        session.add(order)  # update total_price

    return order


@router.get("/")
async def get_orders(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker),
):
    return await OrderController(session=session).get_orders_controller()


@router.get("/{order_uid}/status")
async def get_order_status():
    pass




@router.get("/me")
async def get_my_orders(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),):
    
    user_uid = token_details['user']['user_uid']
    
    
    statement = select(Orders).where(Orders.user_uid == user_uid)
    result = await session.exec(statement)
    
    return result


@router.get("/{order_id}", response_model=OrderReadWithItems)
async def get_order(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker),
    order_id: str,
):

    order =  await OrderController(session=session).get_order_controller(order_uid=order_id)
    
    if order.user_uid != token_details["user"]["user_uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

@router.delete("/{order_id}")
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker),
    order_id: str,
):
    return await OrderController(session=session).delete_order_controller(order_id=order_id)

"""@router.patch ("/")
async def update_order(
    *,session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker),
    order: OrderUpdate,
):
    return await OrderController(session=session).update_order_controller(order=order)"""


"""@router.put("/{product_id}")
async def update_user_patch(product_id: str):
    pass"""