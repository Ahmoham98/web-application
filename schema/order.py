from typing import List
from datetime import datetime
from pydantic import BaseModel
import uuid

class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int
    
    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    
    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    uid: uuid.UUID
    total_price: float
    status: str
    created_at: datetime
    
    class Config:
        orm_mode = True


class OrderItemRead(BaseModel):
    product_uid: uuid.UUID
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderReadWithItems(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        orm_mode = True