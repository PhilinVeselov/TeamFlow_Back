from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base import Base

class VacancyResponse(Base):
    __tablename__ = "vacancy_responses"

    id_vacancy_responses = Column(Integer, primary_key=True, index=True)
    status = Column(String(50))
    id_vacancy = Column(Integer, ForeignKey("vacancy.id_vacancy"))
    id_user = Column(Integer, ForeignKey("user.id_user"))
