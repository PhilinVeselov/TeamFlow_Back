from pydantic import BaseModel
from typing import List, Optional
from src.schemas.UserOrganization import UserOrganizationRead

class TechnologyStackItem(BaseModel):
    id_technology_stack: int
    name: str


class ProfileOut(BaseModel):
    id_user: int
    name: str
    email: str
    description: Optional[str] = None
    img: Optional[str] = None
    technology_stack: List[TechnologyStackItem]
    user_organizations: List[UserOrganizationRead]  

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    img: Optional[str] = None
    technology_stack_ids: Optional[List[int]] = None
