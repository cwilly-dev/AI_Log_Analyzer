from typing import List
from pydantic import BaseModel, Field
from app.models.log import RiskLevel

class LogAnalysisResponse(BaseModel):
    summary: str = Field(
        description="Clear summary of what the log indicates",
    )
    root_cause: str = Field(
        description="The root cause inferred from the log",
    )
    has_error: bool = Field(
        description="Whether the log indicates an error or issue",
    )
    risk_level: RiskLevel = Field(
        description="Risk level associated with the issue"
    )
    requires_immediate_attention: bool = Field(
        description="Whether this issue requires immediate attention"
    )
    recommended_next_steps: List[str] = Field(
        description="Concrete steps to investigate or fix the issue"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the analysis (0–1)"
    )