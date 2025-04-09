from pydantic import BaseModel

class RoleOrganizationCreate(BaseModel):
    id_role_organization: int
    name: str

class RoleOrganizationRead(BaseModel):
    id_role_organization: int
    name: str

    class Config:
        from_attributes = True  # В Pydantic v2 заменяет orm_mode = True
