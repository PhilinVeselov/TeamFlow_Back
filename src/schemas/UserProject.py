from pydantic import BaseModel
from uuid import UUID

class UserProjectCreate(BaseModel):
    id_user: UUID
    id_project: UUID
    id_role_project: int

class UserProjectRead(UserProjectCreate):
    id_user_project: int
