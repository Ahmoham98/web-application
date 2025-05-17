from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

if TYPE_CHECKING:
    from models.order import Orders
    from models.product import Products


class OrderItems(SQLModel, table=True):
    
    __tablename__ = "orderitems"
    
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    ))
    order_uid: uuid.UUID = Field(foreign_key="orders.uid")
    product_uid: uuid.UUID = Field(foreign_key="products.uid")
    quantity: int
    unit_price: float
    