
from sqlalchemy import Column, Integer, ForeignKey
from src.db.base import Base

class UserTechnologyStack(Base):
    __tablename__ = "user_technology_stack"

    id_user = Column(Integer, ForeignKey("user.id_user"), primary_key=True)
    id_technology_stack = Column(Integer, ForeignKey("technology_stack.id_technology_stack"), primary_key=True)
