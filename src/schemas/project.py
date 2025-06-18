from pydantic import BaseModel
from typing import Optional
from src.schemas.organization import OrganizationRead
from src.schemas.TechnologyStack import TechnologyStackOut
from src.schemas.vacancy import VacancyOut 
from pydantic import ConfigDict

class ProjectBase(BaseModel):
    name: str
    description: str
    status: str
    id_organizations: int
    is_paid: Optional[bool] = False       
    is_remote: Optional[bool] = True  

class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]
    id_organizations: Optional[int]
    is_paid: Optional[bool]
    is_remote: Optional[bool]
    technology_stack_ids: Optional[list[int]] = None

class ProjectCreate(BaseModel):
    name: str
    description: str
    status: str
    id_organizations: int
    technology_stack_ids: list[int]
    is_paid: Optional[bool] = False
    is_remote: Optional[bool] = True


class ProjectRead(BaseModel):
    id_project: int
    name: str
    description: str
    status: str
    vacancies: Optional[list[VacancyOut]] = None 
    is_paid: Optional[bool]
    is_remote: Optional[bool]
    organization: OrganizationRead
    technology_stacks: list[TechnologyStackOut]
    model_config = ConfigDict(from_attributes=True)

