from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class UserProject(Base):
    __tablename__ = "user_project"

    id_user_project = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id_user"))
    id_project = Column(Integer, ForeignKey("project.id_project"))
    id_role_project = Column(Integer, ForeignKey("role_project.id_role_project"))

    user = relationship("User", backref="user_projects")
    project = relationship("Project", backref="user_projects")
    role = relationship("RoleProject")
