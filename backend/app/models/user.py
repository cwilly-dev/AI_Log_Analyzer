from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    logs = relationship("Log", back_populates="owner")