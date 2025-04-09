from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base import Base

class Vacancy(Base):
    __tablename__ = "vacancy"

    id_vacancy = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    id_role_project = Column(Integer, ForeignKey("role_project.id_role_project"))
    id_project = Column(Integer, ForeignKey("project.id_project"))
