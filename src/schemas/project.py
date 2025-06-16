from pydantic import BaseModel
from typing import Optional
from src.schemas.organization import OrganizationRead

class ProjectBase(BaseModel):
    name: str
    description: str
    status: str
    id_organizations: int
    id_technology_stack: int
    is_paid: Optional[bool] = False       
    is_remote: Optional[bool] = True  

class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]
    id_organizations: Optional[int]
    id_technology_stack: Optional[int]
    is_paid: Optional[bool]
    is_remote: Optional[bool]


class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id_project: int
    organization: OrganizationRead

    class Config:
        from_attributes = True
