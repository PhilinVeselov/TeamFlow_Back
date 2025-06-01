from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base

class InviteOrganization(Base):
    __tablename__ = "invite_organization"

    id_invite = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)
    token = Column(String(100), unique=True, index=True)
    id_organizations = Column(Integer, ForeignKey("organization.id_organizations"))
    id_role_organization = Column(Integer, ForeignKey("role_organization.id_role_organization"))
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
