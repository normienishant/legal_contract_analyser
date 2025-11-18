"""Bookmarks API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.bookmark import Bookmark
from app.models.analysis import Clause, Analysis
from pydantic import BaseModel

router = APIRouter()


class BookmarkCreate(BaseModel):
    clause_id: int
    analysis_id: int
    note: str = None


class BookmarkResponse(BaseModel):
    id: int
    clause_id: int
    analysis_id: int
    analysis_filename: str
    clause_text: str
    clause_index: int
    risk_label: str
    risk_score: float
    note: str = None
    created_at: str


@router.post("/api/bookmarks", response_model=BookmarkResponse)
async def create_bookmark(
    bookmark: BookmarkCreate,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Create a new bookmark (only for analyses in current session)."""
    # Check if analysis exists and belongs to current session
    analysis_query = db.query(Analysis).filter(Analysis.id == bookmark.analysis_id)
    if x_session_id:
        analysis_query = analysis_query.filter(Analysis.session_id == x_session_id)
    else:
        analysis_query = analysis_query.filter(Analysis.session_id == None)
    
    analysis = analysis_query.first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found or does not belong to your session"
        )
    
    # Check if clause exists and belongs to this analysis
    clause = db.query(Clause).filter(
        Clause.id == bookmark.clause_id,
        Clause.analysis_id == bookmark.analysis_id
    ).first()
    if not clause:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clause not found"
        )
    
    # Check if already bookmarked
    existing = db.query(Bookmark).filter(
        Bookmark.clause_id == bookmark.clause_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Clause already bookmarked"
        )
    
    # Create bookmark
    db_bookmark = Bookmark(
        clause_id=bookmark.clause_id,
        analysis_id=bookmark.analysis_id,
        note=bookmark.note
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    
    return BookmarkResponse(
        id=db_bookmark.id,
        clause_id=db_bookmark.clause_id,
        analysis_id=db_bookmark.analysis_id,
        analysis_filename=analysis.original_filename if analysis else "",
        clause_text=clause.clause_text,
        clause_index=clause.clause_index,
        risk_label=clause.risk_label,
        risk_score=clause.risk_score,
        note=db_bookmark.note,
        created_at=db_bookmark.created_at.isoformat()
    )


@router.get("/api/bookmarks", response_model=List[BookmarkResponse])
async def get_bookmarks(
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Get all bookmarks for current session."""
    # Join with Analysis to filter by session_id
    bookmark_query = db.query(Bookmark).join(Analysis)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        bookmark_query = bookmark_query.filter(Analysis.session_id == x_session_id)
    else:
        # If no session_id, only return bookmarks for analyses without session_id
        bookmark_query = bookmark_query.filter(Analysis.session_id == None)
    
    bookmarks = bookmark_query.order_by(Bookmark.created_at.desc()).all()
    
    results = []
    for bookmark in bookmarks:
        clause = db.query(Clause).filter(Clause.id == bookmark.clause_id).first()
        analysis = db.query(Analysis).filter(Analysis.id == bookmark.analysis_id).first()
        
        if clause and analysis:
            results.append(BookmarkResponse(
                id=bookmark.id,
                clause_id=bookmark.clause_id,
                analysis_id=bookmark.analysis_id,
                analysis_filename=analysis.original_filename,
                clause_text=clause.clause_text,
                clause_index=clause.clause_index,
                risk_label=clause.risk_label,
                risk_score=clause.risk_score,
                note=bookmark.note,
                created_at=bookmark.created_at.isoformat()
            ))
    
    return results


@router.delete("/api/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: int,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Delete a bookmark (only if belongs to current session)."""
    # Join with Analysis to check session_id
    bookmark_query = db.query(Bookmark).join(Analysis).filter(Bookmark.id == bookmark_id)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        bookmark_query = bookmark_query.filter(Analysis.session_id == x_session_id)
    else:
        bookmark_query = bookmark_query.filter(Analysis.session_id == None)
    
    bookmark = bookmark_query.first()
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found or does not belong to your session"
        )
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark deleted successfully"}

