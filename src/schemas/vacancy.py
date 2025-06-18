from pydantic import BaseModel
from src.schemas.RoleProject import RoleProjectRead

class VacancyCreate(BaseModel):
    id_project: int
    id_role_project: int

class VacancyOut(BaseModel):
    role: RoleProjectRead  # будет доступно как vacancy.role.name

    class Config:
        from_attributes = True
