from pydantic import BaseModel
from typing import Optional

class UserProjectBase(BaseModel):
    id_project: int
    id_role_project: int
    id_user: int

class UserProjectRead(UserProjectBase):
    id_user_project: int

    class Config:
        orm_mode = True