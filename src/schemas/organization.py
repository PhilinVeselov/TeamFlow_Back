from pydantic import BaseModel
from typing import Optional

class OrganizationBase(BaseModel):
    name: str
    domein: Optional[str]
    email: Optional[str]

class OrganizationUp(BaseModel):
    name: str
    email: Optional[str]

class OrganizationRead(OrganizationBase):
    id_organizations: int

    class Config:
        from_attributes = True
