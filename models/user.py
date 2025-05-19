from typing import TYPE_CHECKING, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
from pydantic import EmailStr
import sqlalchemy.dialects.postgresql as pg
import uuid

if TYPE_CHECKING:
    from models.product import Products 
    from models.order import Orders

class Users(SQLModel, table=True):
    
    __tablename__ = "users"
    
    uid: uuid.UUID | None = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
            index=True,
            unique=True
        ))
    username: str | None = Field(sa_column=Column(
        pg.VARCHAR(20),
        unique=True
    ))
    hashed_password: str | None = Field(exclude=True)
    email: EmailStr
    phone: str | None = Field(sa_column=Column(
        pg.VARCHAR(50),
        default="no phone "
    ))
    first_name: str | None = Field(sa_column=Column(
        pg.VARCHAR(20),
        default= "no first_name "
    ))
    last_name: str | None = Field(sa_column=Column(
        pg.VARCHAR(20),
        default= "no last_name "
    ))
    address: str | None = Field(sa_column=Column(
        pg.VARCHAR(50),
        default= "no address "
    ))
    role: str | None = Field(sa_column=Column(
        pg.VARCHAR(20),
        default= "no role "
    ))
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow
    ))
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow
    ))
    is_superuser: bool | None = Field(sa_column=Column(
        pg.BOOLEAN,
        default= False
    ))
    
    is_verified : bool | None = Field(sa_column=Column(
        pg.BOOLEAN,
        default=False
    ))
    
    is_active : bool | None = Field(sa_column=Column(
        pg.BOOLEAN,
        default=True
    ))
    
    orders: List["Orders"] = Relationship(back_populates="user")
    
    def __repr__(self):
        return f"<user's first_name: {self.first_name}>"