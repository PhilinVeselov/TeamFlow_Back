from src.schemas.organization import OrganizationRead
from pydantic import BaseModel
from src.schemas.RoleOrganization import RoleOrganizationRead  # добавь такую схему
from typing import Optional



class UserOrganizationBase(BaseModel):
    id_user: int
    id_organizations: int
    id_role_organization: int

class UserOrganizationRead(BaseModel):
    id_user_organization: int
    id_user: int
    id_organizations: int
    id_role_organization: int

    # Вложенные сущности
    role_organization: Optional[RoleOrganizationRead]
    organization: Optional[OrganizationRead]

    class Config:
        from_attributes = True  # или orm_mode = True для Pydantic v1


class AddUserByEmail(BaseModel):
    email: str
    id_role_organization: int

