from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.models.user_technology_stack import UserTechnologyStack

class TechnologyStack(Base):
    __tablename__ = "technology_stack"

    id_technology_stack = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    users = relationship(
        "User",
         secondary=UserTechnologyStack.__table__,
        back_populates="technology_stacks"
    )
    
