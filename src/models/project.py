from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.models.project_technology_stack import ProjectTechnologyStack

class Project(Base):
    __tablename__ = "project"

    id_project = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    status = Column(String(50), default="active")
    vacancies = relationship("Vacancy", back_populates="project")

    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))
    is_paid = Column(Boolean, default=False)        
    is_remote = Column(Boolean, default=True)  
    organization = relationship("Organization", back_populates="projects")
    technology_stacks = relationship(
        "TechnologyStack",
        secondary="project_technology_stack",
        back_populates="projects"
    )