from pydantic import BaseModel
from typing import Optional

class UserProjectHistoryBase(BaseModel):
    id_user: int
    id_project: int
    id_organizations: int
    id_role_project: int

class UserProjectHistoryRead(UserProjectHistoryBase):
    id_user_project_history: int

    class Config:
        orm_mode = True