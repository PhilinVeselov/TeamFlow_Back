from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class UserOrganization(Base):
    __tablename__ = "user_organization"

    id_user_organization = Column(Integer, primary_key=True, index=True)
    id_role_organization = Column(Integer, ForeignKey("role_organization.id_role_organization"))
    id_user = Column(Integer, ForeignKey("user.id_user"))
    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))