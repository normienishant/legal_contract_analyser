"""Analysis database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Analysis(Base):
    """Analysis record model."""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=True, index=True)  # Browser session for user isolation
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    global_risk_score = Column(Float, nullable=False)
    total_clauses = Column(Integer, default=0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    clauses = relationship("Clause", back_populates="analysis", cascade="all, delete-orphan")


class Clause(Base):
    """Clause model for storing individual clause analysis."""
    __tablename__ = "clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    clause_text = Column(Text, nullable=False)
    clause_index = Column(Integer, nullable=False)
    risk_label = Column(String, nullable=False)  # LOW, MEDIUM, HIGH
    risk_score = Column(Float, nullable=False)
    explanation = Column(Text)
    suggested_mitigation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    analysis = relationship("Analysis", back_populates="clauses")

