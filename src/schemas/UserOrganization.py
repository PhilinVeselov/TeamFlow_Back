from pydantic import BaseModel
from typing import Optional

class UserOrganizationBase(BaseModel):
    id_user: int
    id_organizations: int
    id_role_organization: int

class UserOrganizationRead(UserOrganizationBase):
    id_user_organization: int

    class Config:
        orm_mode = True