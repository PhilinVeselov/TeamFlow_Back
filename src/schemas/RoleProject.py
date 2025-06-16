from pydantic import BaseModel

class RoleProjectBase(BaseModel):
    name: str

class RoleProjectCreate(RoleProjectBase):
    pass

class RoleProjectRead(BaseModel):
    id_role_project: int
    name: str

    class Config:
        from_attributes = True