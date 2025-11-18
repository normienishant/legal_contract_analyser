"""Bookmark database models."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Bookmark(Base):
    """Bookmark model for saving important clauses."""
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_id = Column(Integer, ForeignKey("clauses.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    note = Column(Text)  # Optional note/comment
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    clause = relationship("Clause", foreign_keys=[clause_id])
    analysis = relationship("Analysis", foreign_keys=[analysis_id])

