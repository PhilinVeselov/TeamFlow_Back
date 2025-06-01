from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class Project(Base):
    __tablename__ = "project"

    id_project = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    status = Column(String(50), default="active")

    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))
    id_technology_stack = Column(Integer, ForeignKey("technology_stack.id_technology_stack"))

    organization = relationship("Organization", back_populates="projects")
    technology_stack = relationship("TechnologyStack")
