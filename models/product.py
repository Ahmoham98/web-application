from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

if TYPE_CHECKING:
    from models.user import Users
    from models.category import Categories
    #from models.order_item import OrderItems

# Products table

class Products(SQLModel, table=True):
    
    __tablename__ = "products"
    
    uid: uuid.UUID= Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    ))
    category_uid: uuid.UUID = Field(foreign_key="categories.uid")
    users_uid: uuid.UUID = Field(foreign_key="users.uid")
    title: str | None = Field(sa_column=Column(
        pg.VARCHAR(50),
        index=True
    ))
    description: str | None = Field(sa_column=Column(
        pg.VARCHAR(100),
        default="no description "
    ))
    image_url: str | None = Field(sa_column=Column(
        pg.VARCHAR(100),
        default="update image_url "
    ))
    unit_price: int | None = Field(
        sa_column=Column(
            pg.INTEGER,
            default=-1,
    ))
    sale_price: int | None = Field(
        sa_column=Column(
            pg.INTEGER,
            default=-1,
        ))
    is_active: bool = Field(
        sa_column=Column(
            pg.BOOLEAN, 
            default= False
        )
    )
    status: str | None = Field(
        sa_column=Column(
            pg.VARCHAR(20),
            default="Assign status",
        ))
    created_at: datetime | None = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default = datetime.utcnow,
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default = datetime.utcnow,
        ))
