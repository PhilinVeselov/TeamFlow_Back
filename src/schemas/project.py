from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    id_organizations: int
    id_technology_stack: int
    status: Optional[str]

class ProjectRead(ProjectBase):
    id_project: int

    class Config:
        orm_mode = True