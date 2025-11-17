"""Settings API endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.services.analysis import AnalysisService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Global analysis service instance (will be updated when mode changes)
analysis_service = AnalysisService()


class SettingsUpdate(BaseModel):
    """Settings update request."""
    ml_mode: Literal["ml", "rules"]


@router.get("/api/settings")
async def get_settings():
    """Get current settings."""
    return {
        "ml_mode": settings.ml_mode,
        "model_path": settings.model_path,
        "use_gpu": settings.use_gpu,
    }


@router.post("/api/settings")
async def update_settings(settings_update: SettingsUpdate):
    """
    Update settings dynamically (without restart).
    
    Changes ML mode on the fly.
    """
    # Import here to avoid circular dependency
    
    try:
        old_mode = settings.ml_mode
        new_mode = settings_update.ml_mode
        
        # Update settings object
        settings.ml_mode = new_mode
        
        # Reinitialize analysis service with new mode
        # Update the global service in routes module
        import app.api.routes as routes_module
        routes_module.analysis_service = AnalysisService()
        
        logger.info(f"ML mode changed from {old_mode} to {new_mode}")
        
        return {
            "success": True,
            "message": f"Settings updated. ML mode changed to {new_mode}. Changes take effect immediately!",
            "ml_mode": new_mode,
        }
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update settings: {str(e)}"
        )


