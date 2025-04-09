from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base import Base

class UserProject(Base):
    __tablename__ = "user_project"

    id_user_project = Column(Integer, primary_key=True, index=True)
    id_project = Column(Integer, ForeignKey("project.id_project"))
    id_role_project = Column(Integer, ForeignKey("role_project.id_role_project"))
    id_user = Column(Integer, ForeignKey("user.id_user"))