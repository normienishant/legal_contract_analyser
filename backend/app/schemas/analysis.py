"""Analysis schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ClauseAnalysis(BaseModel):
    """Clause-level analysis result."""
    clause_text: str
    clause_index: int
    risk_label: str = Field(..., pattern="^(LOW|MEDIUM|HIGH)$")
    risk_score: float = Field(..., ge=0, le=100)
    explanation: str
    suggested_mitigation: str


class DocumentAnalysis(BaseModel):
    """Document-level analysis result."""
    global_risk_score: float = Field(..., ge=0, le=100)
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    clauses: List[ClauseAnalysis]


class AnalysisResponse(BaseModel):
    """Full analysis response."""
    analysis_id: int
    filename: str
    analysis: DocumentAnalysis
    created_at: datetime


class AnalysisHistoryItem(BaseModel):
    """Analysis history item."""
    id: int
    filename: str
    original_filename: str
    global_risk_score: float
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    """File upload response."""
    file_id: str
    filename: str
    message: str

