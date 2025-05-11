from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime

# Users model
class UsersBase(BaseModel):
    username: str = Field(max_length=10)
    email: EmailStr = Field(max_length=40)
    phone: str = Field(max_length=20)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    address: str = Field(max_length=60)
    created_at: datetime

# User password with hashed data
class UserInDB(UsersBase):
    hashed_password: str

#User Input model
class UsersCreate(UsersBase):
    password: str = Field(min_length=8)
    email: EmailStr = Field(max_length=40)
    phone: str | None = Field(default=None ,max_length=20)
    address: str | None = Field(default=None ,max_length=60)
    created_at: datetime | None = None
    updated_at: datetime | None = None

# User Output model
class UsersPublic(UsersBase):
    uid: uuid.UUID
    email: EmailStr | None = None
    phone: str | None = None

# User Update(Patch) model
class UsersUpdate(BaseModel):
    username: str = Field(max_length=10)
    password: str | None = Field(default=None, min_length=8)
    email: EmailStr | None = Field(default=None ,max_length=40)
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    created_at: datetime | None = None
    is_superuser: bool | None = False


class UsersUpdatePut(BaseModel):
    username: str 
    email: EmailStr | None = None
    phone: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    role: str | None = None
    created_at: datetime | None = None
    is_superuser: bool | None = False