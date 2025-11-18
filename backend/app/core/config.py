"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Literal
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = int(os.getenv("PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./contract_analyzer.db")
    
    # ML Configuration
    ml_mode: Literal["ml", "rules"] = "ml"
    model_path: str = "./models/risk_classifier"
    use_gpu: bool = False
    
    # Security
    api_key: str = "your_api_key_here"
    max_upload_size_mb: int = 10
    allowed_extensions: str = "pdf,docx,txt"
    
    # Hugging Face
    hf_token: str | None = None
    
    # Logging
    log_level: str = "INFO"
    
    # Paths
    uploads_dir: str = "./uploads"
    models_dir: str = "./models"
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_upload_size_mb * 1024 * 1024
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Get list of allowed extensions."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8-sig"  # Handle BOM
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields


settings = Settings()

# Ensure directories exist
try:
    os.makedirs(settings.uploads_dir, exist_ok=True)
    os.makedirs(settings.models_dir, exist_ok=True)
except Exception as e:
    # Log but don't fail if directory creation fails
    import logging
    logging.getLogger(__name__).warning(f"Could not create directories: {e}")

