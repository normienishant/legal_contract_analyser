"""FastAPI application entry point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.export import router as export_router
from app.api.settings import router as settings_router
from app.api import bookmarks
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Contract Analyzer & Risk Detector",
    description="API for analyzing contract documents and detecting risks",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(export_router)
app.include_router(settings_router)
app.include_router(bookmarks.router)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    from app.db import init_db
    init_db()
    
    # Run migration to add session_id column if needed
    try:
        from app.db.migrate_add_session_id import migrate_database
        migrate_database()
        logger.info("Database migration check completed")
    except Exception as e:
        logger.warning(f"Migration check failed (this is OK if column already exists): {e}")
    
    logger.info(f"Starting application in {settings.environment} mode")
    logger.info(f"ML Mode: {settings.ml_mode}")
    logger.info(f"Upload directory: {settings.uploads_dir}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Contract Analyzer & Risk Detector API",
        "version": "1.0.0",
        "docs": "/docs"
    }

