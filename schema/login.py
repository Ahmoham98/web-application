from pydantic import BaseModel, Field, EmailStr


class UserLoginModel(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=8)