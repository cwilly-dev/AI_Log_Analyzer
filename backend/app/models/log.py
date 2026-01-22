import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.db import Base

class RiskLevel(str, enum.Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="logs")
    analyses = relationship("LogAnalysis", back_populates="log", cascade="all, delete-orphan")

class LogAnalysis(Base):
    __tablename__ = "log_analyses"

    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey("logs.id"), nullable=False)

    summary = Column(String, nullable=False)
    root_cause = Column(String, nullable=False)

    has_error = Column(Boolean, nullable=False)
    risk_level = Column(String, nullable=False)
    requires_immediate_attention = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)

    recommended_next_steps = Column(JSON, nullable=False)
    raw_response = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    log = relationship("Log", back_populates="analyses")