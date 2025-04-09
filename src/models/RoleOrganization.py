from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class RoleOrganization(Base):
    __tablename__ = "role_organization"

    id_role_organization = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))