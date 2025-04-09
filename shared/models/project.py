from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base import Base

class Project(Base):
    __tablename__ = "project"

    id_project = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(50))
    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))
    id_technology_stack = Column(Integer, ForeignKey("technology_stack.id_technology_stack"))
    status = Column(String(50))