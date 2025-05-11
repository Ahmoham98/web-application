from datetime import datetime
from pydantic import BaseModel, Field
import uuid

# Categories model
class CategoriesBase(BaseModel):
    title: str = Field(max_length=20)
    description: str | None = Field(default=None, max_length=100)
    created_at: datetime

# Categories Input model
class CategoriesCreate(CategoriesBase):
    created_at: datetime | None = None

# Categories Output models
class CategoriesPublic(CategoriesBase):
    uid: uuid.UUID
    description: str | None = None

# Categories Update(Patch) model
class CategoriesUpdate(BaseModel):
    title: str | None = Field(max_length=20)
    description: str | None = Field(default=None, max_length=100)
    created_at: datetime | None = None

