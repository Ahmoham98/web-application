from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Enum


class Status (BaseModel, Enum):
    pending: str
    success: str
    failed: str


class PaymentCreate(BaseModel):
    order_uid: str
    amount: float
    payment_method: Optional[str] = "card"

class PaymentResponse(BaseModel):
    uid: str
    order_uid: str
    user_uid: str
    amount: float
    status: str
    payment_method: Optional[str]
    created_at: datetime