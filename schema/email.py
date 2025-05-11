from pydantic import BaseModel, EmailStr, Field
from typing import List



class EmailModel(BaseModel):
    addresses: List[EmailStr]

class PasswrodResetRequestModel(BaseModel):
    email: str

class PasswordResetConfirmModel(BaseModel):
    new_password: str = Field(min_length=8)
    confirm_new_password: str = Field(min_length=8)