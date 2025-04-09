from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base import Base

class RoleProject(Base):
    __tablename__ = "role_project"

    id_role_project = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))