from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.base import Base

class Vacancy(Base):
    __tablename__ = "vacancy"
    id_vacancy = Column(Integer, primary_key=True)
    id_project = Column(Integer, ForeignKey("project.id_project"))
    id_role_project = Column(Integer, ForeignKey("role_project.id_role_project"))
    is_active = Column(Boolean, default=True)

    role = relationship("RoleProject", back_populates="vacancies")
    project = relationship("Project", back_populates="vacancies")
