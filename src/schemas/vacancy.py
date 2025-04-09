from pydantic import BaseModel
from typing import Optional

class VacancyBase(BaseModel):
    is_active: bool
    id_role_project: int
    id_project: int

class VacancyRead(VacancyBase):
    id_vacancy: int

    class Config:
        orm_mode = True