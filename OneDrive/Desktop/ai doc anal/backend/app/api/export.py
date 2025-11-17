"""Export functionality for analysis reports."""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.analysis import Analysis
import json
from typing import Optional

router = APIRouter()


@router.get("/api/export/{analysis_id}/json")
async def export_json(
    analysis_id: int,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Export analysis as JSON (only if belongs to current session)."""
    query = db.query(Analysis).filter(Analysis.id == analysis_id)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        query = query.filter(Analysis.session_id == x_session_id)
    else:
        query = query.filter(Analysis.session_id == None)
    
    analysis = query.first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found or does not belong to your session")
    
    report = {
        "filename": analysis.filename,
        "analyzed_at": analysis.created_at.isoformat(),
        "global_risk_score": analysis.global_risk_score,
        "summary": {
            "total_clauses": analysis.total_clauses,
            "high_risk": analysis.high_risk_count,
            "medium_risk": analysis.medium_risk_count,
            "low_risk": analysis.low_risk_count,
        },
        "clauses": [
            {
                "clause_index": clause.clause_index,
                "clause_text": clause.clause_text,
                "risk_label": clause.risk_label,
                "risk_score": clause.risk_score,
                "explanation": clause.explanation,
                "suggested_mitigation": clause.suggested_mitigation,
            }
            for clause in analysis.clauses
        ],
    }
    
    return Response(
        content=json.dumps(report, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="contract-analysis-{analysis_id}.json"'
        }
    )


@router.get("/api/export/{analysis_id}/txt")
async def export_txt(
    analysis_id: int,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),  # Session ID from header
    db: Session = Depends(get_db)
):
    """Export analysis as plain text (only if belongs to current session)."""
    query = db.query(Analysis).filter(Analysis.id == analysis_id)
    
    # Filter by session_id if provided (user isolation)
    if x_session_id:
        query = query.filter(Analysis.session_id == x_session_id)
    else:
        query = query.filter(Analysis.session_id == None)
    
    analysis = query.first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found or does not belong to your session")
    
    text = f"CONTRACT ANALYSIS REPORT\n"
    text += f"{'=' * 50}\n\n"
    text += f"Document: {analysis.filename}\n"
    text += f"Analyzed: {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += f"EXECUTIVE SUMMARY\n"
    text += f"{'-' * 50}\n"
    text += f"Global Risk Score: {analysis.global_risk_score:.1f}/100\n"
    text += f"Total Clauses: {analysis.total_clauses}\n"
    text += f"High Risk: {analysis.high_risk_count}\n"
    text += f"Medium Risk: {analysis.medium_risk_count}\n"
    text += f"Low Risk: {analysis.low_risk_count}\n\n"
    text += f"DETAILED CLAUSE ANALYSIS\n"
    text += f"{'-' * 50}\n\n"
    
    for clause in analysis.clauses:
        text += f"Clause {clause.clause_index + 1}: {clause.risk_label} Risk ({clause.risk_score:.1f})\n"
        text += f"Text: {clause.clause_text}\n"
        text += f"Explanation: {clause.explanation}\n"
        text += f"Mitigation: {clause.suggested_mitigation}\n\n"
    
    return Response(
        content=text,
        media_type="text/plain",
        headers={
            "Content-Disposition": f'attachment; filename="contract-analysis-{analysis_id}.txt"'
        }
    )

