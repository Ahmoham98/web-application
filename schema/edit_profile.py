from pydantic import BaseModel
from typing import Optional

class ChangePasswordModel(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

class UpdateProfileModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]