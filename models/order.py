from typing import TYPE_CHECKING, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

if TYPE_CHECKING:
    from models.orderitem import OrderItems
    from models.user import Users
    from models.order import Orders

class Orders(SQLModel, table=True):
    
    __tablename__ = "orders"
    
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    ))
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP,
        default=datetime.utcnow
    ))
    total_price: float = Field(sa_column=Column(
        pg.FLOAT
    ))
    status: str = Field(sa_column=Column(
        pg.VARCHAR(20),
        default="pending"
    ))
    