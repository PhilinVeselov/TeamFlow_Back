from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    description: Optional[str] = None
    img: Optional[str] = None
    id_technology_stack: Optional[int] = None
    is_looking_for_project: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserRead(BaseModel):
    id_user: int
    name: str
    email: str

    class Config:
        from_attributes = True