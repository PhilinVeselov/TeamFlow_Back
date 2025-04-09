from pydantic import BaseModel
from typing import Optional

class VacancyResponseBase(BaseModel):
    status: str
    id_vacancy: int
    id_user: int

class VacancyResponseRead(VacancyResponseBase):
    id_vacancy_responses: int

    class Config:
        orm_mode = True
