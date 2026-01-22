from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LogCreate(BaseModel):
    content: str

class LogOut(BaseModel):
    id: int
    owner_id: int
    content: Optional[str] = None
    created_at: Optional[datetime] = None

class LogAnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    summary: str
    root_cause: str
    has_error: bool
    risk_level: str
    requires_immediate_attention: bool
    recommended_next_steps: list[str]
    confidence: float