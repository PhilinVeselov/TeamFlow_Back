from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str
    status: str
    id_organizations: int
    id_technology_stack: int

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id_project: int

    class Config:
        from_attributes = True
