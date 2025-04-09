from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class Organization(Base):
    __tablename__ = "organization"

    id_organizations = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    domein = Column(String(50))
    email = Column(String(50))