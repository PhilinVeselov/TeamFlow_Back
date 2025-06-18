# models/project_technology_stack.py
from sqlalchemy import Column, ForeignKey, Table
from src.db.base import Base

class ProjectTechnologyStack(Base):
    __tablename__ = "project_technology_stack"
    id_project = Column(ForeignKey("project.id_project"), primary_key=True)
    id_technology_stack = Column(ForeignKey("technology_stack.id_technology_stack"), primary_key=True)
