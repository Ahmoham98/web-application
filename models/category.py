from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

if TYPE_CHECKING:
    from models.product import Products

# Categories table

class Categories(SQLModel, table=True):
    
    __tablename__ = "categories"
    
    uid: uuid.UUID | None = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    ))
    title: str = Field(
        pg.VARCHAR(20),
        index=True,
    )
    description: str | None = Field(sa_column=Column(
        pg.VARCHAR(100),
        default="no description "
    ))
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow
    ))