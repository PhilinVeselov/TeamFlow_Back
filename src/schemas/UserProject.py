from pydantic import BaseModel
from uuid import UUID
from src.schemas.user import UserRead
from src.schemas.RoleProject import RoleProjectRead

class UserProjectCreate(BaseModel):
    id_user: int
    id_project: int
    id_role_project: int
    

class UserProjectRead(BaseModel):
    id_user_project: int
    id_user: int
    id_project: int
    id_role_project: int

    user: UserRead
    role: RoleProjectRead

    class Config:
        from_attributes = True