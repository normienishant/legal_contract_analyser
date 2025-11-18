"""API routes."""
import os
import uuid
import logging
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.analysis import Analysis, Clause
from app.schemas.analysis import (
    AnalysisResponse,
    AnalysisHistoryItem,
    UploadResponse,
    DocumentAnalysis,
)
from app.services.extract import DocumentExtractor
from app.services.analysis import AnalysisService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
extractor = DocumentExtractor()
analysis_service = AnalysisService()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "ml_mode": settings.ml_mode}


@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """
    Upload a document for analysis.
    
    Validates file type and size, saves to uploads directory.
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower().lstrip(".")
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{file_ext} not allowed. Allowed: {settings.allowed_extensions}"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum of {settings.max_upload_size_mb}MB"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.uploads_dir, safe_filename)
    
    # Save file
    os.makedirs(settings.uploads_dir, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    logger.info(f"File uploaded: {safe_filename}")
    
    return UploadResponse(
        file_id=file_id,
        filename=safe_filename,
        message="File uploaded successfully"
    )


@router.post("/api/extract")
async def extract_text(
    file_id: str,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """
    Extract text and segment into clauses from uploaded file.
    
    Returns extracted text and clause segments.
    """
    try:
        # Find file by ID
        uploads_dir = Path(settings.uploads_dir)
        matching_files = list(uploads_dir.glob(f"{file_id}_*"))
        
        if not matching_files:
            logger.error(f"File not found for file_id: {file_id} in {uploads_dir}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found for file_id: {file_id}"
            )
        
        file_path = str(matching_files[0])
        logger.info(f"Extracting text from: {file_path}")
        
        # Extract text
        text = extractor.extract_text(file_path)
        logger.info(f"Extracted {len(text)} characters")
        
        # Segment into clauses
        clauses = extractor.segment_clauses(text)
        logger.info(f"Segmented into {len(clauses)} clauses")
        
        # Validate clauses
        if not clauses:
            logger.warning("No clauses found after segmentation. Text might be empty or format not recognized.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not segment document into clauses. Please ensure the document contains numbered clauses (1., 2., etc.) or clear paragraph breaks."
            )
        
        if len(clauses) == 1 and len(clauses[0]) > 5000:
            logger.warning(f"Only one very long clause found ({len(clauses[0])} chars). Segmentation might have failed.")
            # Log warning but don't fail - user might have a single long clause
        
        # Validate clause quality
        valid_clauses = []
        for idx, clause in enumerate(clauses):
            clause = clause.strip()
            if len(clause) < 10:
                logger.warning(f"Skipping clause {idx+1}: too short ({len(clause)} chars)")
                continue
            if len(clause) > 10000:
                logger.warning(f"Clause {idx+1} is very long ({len(clause)} chars), truncating to 10000 chars")
                clause = clause[:10000] + "..."
            valid_clauses.append(clause)
        
        if not valid_clauses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid clauses found after segmentation. Please check your document format."
            )
        
        return {
            "file_id": file_id,
            "filename": matching_files[0].name,
            "text": text,
            "clauses": valid_clauses,
            "clause_count": len(valid_clauses),
        }
    except HTTPException:
        raise
    except ValueError as e:
        # Handle specific validation errors
        logger.error(f"Validation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format or content: {str(e)}"
        )
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found. Please upload the file again."
        )
    except Exception as e:
        logger.error(f"Error extracting text: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting text: {str(e)}. Please try again or contact support."
        )


@router.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_document(
    file_id: str,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """
    Analyze document for risks.
    
    Extracts text, segments clauses, runs risk analysis, and stores results.
    """
    # Find file
    uploads_dir = Path(settings.uploads_dir)
    matching_files = list(uploads_dir.glob(f"{file_id}_*"))
    
    if not matching_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    file_path = str(matching_files[0])
    original_filename = matching_files[0].name.replace(f"{file_id}_", "", 1)
    
    try:
        # Extract and segment
        text = extractor.extract_text(file_path)
        clauses = extractor.segment_clauses(text)
        
        # Validate clauses
        if not clauses:
            logger.warning("No clauses found after segmentation in analyze endpoint")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not segment document into clauses. Please ensure the document contains numbered clauses (1., 2., etc.) or clear paragraph breaks."
            )
        
        # Validate clause quality
        valid_clauses = []
        for idx, clause in enumerate(clauses):
            clause = clause.strip()
            if len(clause) < 10:
                logger.warning(f"Skipping clause {idx+1} in analysis: too short ({len(clause)} chars)")
                continue
            if len(clause) > 10000:
                logger.warning(f"Clause {idx+1} is very long ({len(clause)} chars), truncating to 10000 chars")
                clause = clause[:10000] + "..."
            valid_clauses.append(clause)
        
        if not valid_clauses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid clauses found after segmentation. Please check your document format."
            )
        
        clauses = valid_clauses  # Use validated clauses
        
        # Analyze - use the analysis service
        # Note: If mode is changed via settings API, it will use the updated service
        analysis_result = analysis_service.analyze_document(clauses)
        
        # Store in database
        db_analysis = Analysis(
            session_id=x_session_id,  # Store session_id for user isolation
            filename=matching_files[0].name,
            original_filename=original_filename,
            file_path=file_path,
            global_risk_score=analysis_result["global_risk_score"],
            total_clauses=analysis_result["total_clauses"],
            high_risk_count=analysis_result["high_risk_count"],
            medium_risk_count=analysis_result["medium_risk_count"],
            low_risk_count=analysis_result["low_risk_count"],
        )
        db.add(db_analysis)
        db.flush()
        
        # Store clauses
        for clause_data in analysis_result["clauses"]:
            db_clause = Clause(
                analysis_id=db_analysis.id,
                clause_text=clause_data["clause_text"],
                clause_index=clause_data["clause_index"],
                risk_label=clause_data["risk_label"],
                risk_score=clause_data["risk_score"],
                explanation=clause_data["explanation"],
                suggested_mitigation=clause_data["suggested_mitigation"],
            )
            db.add(db_clause)
        
        db.commit()
        db.refresh(db_analysis)
        
        # Build response
        clause_analyses = [
            {
                "clause_text": c["clause_text"],
                "clause_index": c["clause_index"],
                "risk_label": c["risk_label"],
                "risk_score": c["risk_score"],
                "explanation": c["explanation"],
                "suggested_mitigation": c["suggested_mitigation"],
            }
            for c in analysis_result["clauses"]
        ]
        
        document_analysis = DocumentAnalysis(
            global_risk_score=analysis_result["global_risk_score"],
            total_clauses=analysis_result["total_clauses"],
            high_risk_count=analysis_result["high_risk_count"],
            medium_risk_count=analysis_result["medium_risk_count"],
            low_risk_count=analysis_result["low_risk_count"],
            clauses=clause_analyses,
        )
        
        return AnalysisResponse(
            analysis_id=db_analysis.id,
            filename=original_filename,
            analysis=document_analysis,
            created_at=db_analysis.created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing document: {str(e)}"
        )


@router.get("/api/history", response_model=List[AnalysisHistoryItem])
async def get_history(
    limit: int = 50,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Get analysis history for current session."""
    query = db.query(Analysis)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        query = query.filter(Analysis.session_id == x_session_id)
    else:
        # If no session_id, return empty (user isolation)
        query = query.filter(Analysis.session_id == None)
    
    analyses = query.order_by(Analysis.created_at.desc()).limit(limit).all()
    return [AnalysisHistoryItem.model_validate(a) for a in analyses]


@router.get("/api/history/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Get specific analysis by ID (only if belongs to current session)."""
    query = db.query(Analysis).filter(Analysis.id == analysis_id)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        query = query.filter(Analysis.session_id == x_session_id)
    else:
        # If no session_id, only return analyses without session_id
        query = query.filter(Analysis.session_id == None)
    
    analysis = query.first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Load clauses
    clauses = db.query(Clause).filter(Clause.analysis_id == analysis_id).order_by(Clause.clause_index).all()
    
    clause_analyses = [
        {
            "clause_id": c.id,
            "clause_text": c.clause_text,
            "clause_index": c.clause_index,
            "risk_label": c.risk_label,
            "risk_score": c.risk_score,
            "explanation": c.explanation or "",
            "suggested_mitigation": c.suggested_mitigation or "",
        }
        for c in clauses
    ]
    
    document_analysis = DocumentAnalysis(
        global_risk_score=analysis.global_risk_score,
        total_clauses=analysis.total_clauses,
        high_risk_count=analysis.high_risk_count,
        medium_risk_count=analysis.medium_risk_count,
        low_risk_count=analysis.low_risk_count,
        clauses=clause_analyses,
    )
    
    return AnalysisResponse(
        analysis_id=analysis.id,
        filename=analysis.original_filename,
        analysis=document_analysis,
        created_at=analysis.created_at,
    )


@router.get("/api/search/clauses")
async def search_clauses(
    query: str,
    analysis_id: int = None,
    limit: int = 50,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Search clauses across all analyses or within a specific analysis (filtered by session)."""
    from sqlalchemy import or_
    
    if not query or len(query.strip()) < 2:
        return {"query": query, "results": [], "count": 0}
    
    clause_query = db.query(Clause).join(Analysis)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        clause_query = clause_query.filter(Analysis.session_id == x_session_id)
    else:
        # If no session_id, only search in analyses without session_id
        clause_query = clause_query.filter(Analysis.session_id == None)
    
    # Filter by analysis_id if provided
    if analysis_id:
        clause_query = clause_query.filter(Clause.analysis_id == analysis_id)
    
    # Search in clause text, explanation, and mitigation
    search_term = f"%{query.strip()}%"
    clause_query = clause_query.filter(
        or_(
            Clause.clause_text.ilike(search_term),
            Clause.explanation.ilike(search_term),
            Clause.suggested_mitigation.ilike(search_term)
        )
    )
    
    clauses = clause_query.limit(limit).all()
    
    # Format response with analysis info
    results = []
    for clause in clauses:
        analysis = db.query(Analysis).filter(Analysis.id == clause.analysis_id).first()
        results.append({
            "clause_id": clause.id,
            "analysis_id": clause.analysis_id,
            "analysis_filename": analysis.original_filename if analysis else "",
            "clause_text": clause.clause_text,
            "clause_index": clause.clause_index,
            "risk_label": clause.risk_label,
            "risk_score": clause.risk_score,
            "explanation": clause.explanation,
            "suggested_mitigation": clause.suggested_mitigation,
        })
    
    return {"query": query, "results": results, "count": len(results)}

