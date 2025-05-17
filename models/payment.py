from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from datetime import datetime
import uuid

from schema.payment import Status

class Payments(SQLModel, table=True):
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    ))
    order_uid: uuid.UUID = Field(foreign_key="orders.uid")
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    amount: float = Field(sa_column=Column(
        pg.FLOAT
    ))
    status: Status = Field(sa_column=Column(
        pg.ENUM(name=Status)
    )) # e.g. "pending", "success", "failed"
    payment_method: Optional[str]  # e.g. "card", "paypal"
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP,
        default=datetime.utcnow
    ))