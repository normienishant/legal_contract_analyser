"""Batch processing endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.config import settings
from app.services.extract import DocumentExtractor
from app.services.analysis import AnalysisService
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

extractor = DocumentExtractor()
analysis_service = AnalysisService()


@router.post("/api/batch/upload")
async def batch_upload(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload multiple files for batch processing."""
    if len(files) > 10:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed per batch"
        )
    
    results = []
    for file in files:
        try:
            # Validate file
            file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
            if file_ext not in settings.allowed_extensions_list:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": f"File type .{file_ext} not allowed"
                })
                continue
            
            # Read and save file
            content = await file.read()
            if len(content) > settings.max_upload_size_bytes:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": f"File size exceeds {settings.max_upload_size_mb}MB"
                })
                continue
            
            # Save file (simplified - in production, use proper file handling)
            results.append({
                "filename": file.filename,
                "status": "success",
                "message": "File uploaded successfully"
            })
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
    
    return {"results": results, "total": len(files), "successful": sum(1 for r in results if r["status"] == "success")}

