from fastapi import APIRouter ,Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from schema.payment import PaymentCreate, PaymentResponse
from dependencies import get_session, AccessTokenBearer, RoleChecker
from models.order import Orders
from models.payment import Payments

access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])

payment_router = APIRouter()


@payment_router.post("/initialize")
async def start_payment():
    pass


@payment_router.post("/callback", response_model=PaymentResponse)
async def make_payment(
    payment_data: PaymentCreate,
    session: AsyncSession = Depends(get_session),
    token = Depends(access_token_bearer),
):
    user_uid = token["user"]["user_uid"]

    # Get order and validate ownership
    order = await session.get(Orders, payment_data.order_uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_uid != user_uid:
        raise HTTPException(status_code=403, detail="Not allowed to pay for this order")

    if payment_data.amount < order.total_price:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")

    payment = Payments(
        order_uid=order.uid,
        user_uid=user_uid,
        amount=payment_data.amount,
        status="success",  # this would be "pending" if integrating with a real gateway
        payment_method=payment_data.payment_method
    )

    # Update order status
    order.status = "paid"

    async with session.begin():
        session.add(payment)
        session.add(order)

    return payment