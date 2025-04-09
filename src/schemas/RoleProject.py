from pydantic import BaseModel
from typing import Optional

class RoleProjectBase(BaseModel):
    name: str

class RoleProjectRead(RoleProjectBase):
    id_role_project: int

    class Config:
        orm_mode = True