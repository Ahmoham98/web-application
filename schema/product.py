from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# Product model
class Productsbase(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None
    unit_price: int
    sale_price: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

# Product input model
class ProductsCreate(Productsbase):
    pass

# Products Output model
class ProductsPublic(Productsbase):
    uid: uuid.UUID
    category_uid: uuid.UUID
    users_uid: uuid.UUID

#Products Update(Patch) model
class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    unit_price: int | None = None
    sale_price: int | None = None
    is_active: bool | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


