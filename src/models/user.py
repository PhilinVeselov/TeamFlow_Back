from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.models.user_technology_stack import UserTechnologyStack

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(400))
    description = Column(String(3000))
    img = Column(String(3000))
    is_looking_for_project = Column(Boolean, default=False)

    technology_stacks = relationship(
        "TechnologyStack",
        secondary=UserTechnologyStack.__table__,
        back_populates="users"
    )
