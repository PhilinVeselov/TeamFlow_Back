from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class UserProjectHistory(Base):
    __tablename__ = "user_project_history"

    id_user_project_history = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id_user"))
    id_project = Column(Integer, ForeignKey("project.id_project"))
    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))
    id_role_project = Column(Integer, ForeignKey("role_project.id_role_project"))
