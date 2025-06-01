from pydantic import BaseModel

class RoleProjectBase(BaseModel):
    name: str

class RoleProjectCreate(RoleProjectBase):
    pass

class RoleProjectRead(RoleProjectBase):
    id_role_project: int

    class Config:
        from_attributes = True
