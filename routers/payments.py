from fastapi import APIRouter ,Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from schema.payment import PaymentCreate, PaymentResponse
from dependencies import get_session, AccessTokenBearer, RoleChecker
from models.order import Orders
import httpx


access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])

payment_router = APIRouter()


ZARINPAL_MERCHANT_ID = "marchant_id"
CALLBACK_URL = "http://localhost:9000/api/v1/payment/verify"  # change in production

@payment_router.post("/{order_uid}")
async def pay_order(
    *,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
    order_uid: str,

):
    user_uid = token_details['user']['user_uid']
    
    order = await session.get(Orders, order_uid)
    if not order :
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_uid != user_uid:
        raise HTTPException(status_code=404, detail="you don't have access to this order")

    amount = order.total_price  # ← total amount in Tomans
    description = "Payment for pharmacy order"

    data = {
        "merchant_id": ZARINPAL_MERCHANT_ID,
        "amount": amount,
        "callback_url": CALLBACK_URL + f"?order_id={order.uid}",
        "description": description,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.zarinpal.com/pg/v4/payment/request.json", json=data)

    res_data = response.json()
    if res_data["data"]["code"] == 100:
        authority = res_data["data"]["authority"]
        order.authority = authority
        order.status = "pending"
        session.add(order)
        session.commit()
        return {"payment_url": f"https://www.zarinpal.com/pg/StartPay/{authority}"}
    else:
        raise HTTPException(status_code=400, detail="Zarinpal payment initiation failed")
    

@payment_router.get("/verify/{order_uid}")
async def verify_order(
    *,
    session: AsyncSession = Depends(get_session),
    order_uid: str,
    Authority: str,
    Status: str
):
    order = await session.get(Orders, order_uid)
    if not order or order.authority != Authority:
        raise HTTPException(status_code=404, detail="Invalid payment authority")

    if Status != "OK":
        order.status = "failed"
        session.commit()
        return {"status": "failed", "message": "Payment was cancelled by user"}

    verify_data = {
        "merchant_id": ZARINPAL_MERCHANT_ID,
        "amount": 10000,  # should match exactly!
        "authority": Authority,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.zarinpal.com/pg/v4/payment/verify.json", json=verify_data)

    res_data = response.json()
    if res_data["data"]["code"] == 100:
        order.status = "paid"
        session.commit()
        return {"status": "success", "ref_id": res_data["data"]["ref_id"]}
    else:
        order.status = "failed"
        session.commit()
        return {"status": "failed", "message": "Verification failed"}
