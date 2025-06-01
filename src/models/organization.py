from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.db.base import Base
from sqlalchemy.orm import relationship

class Organization(Base):
    __tablename__ = "organization"

    id_organizations = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    domein = Column(String, nullable=False, unique=True)
    email = Column(String(50))
    projects = relationship("Project", back_populates="organization")

