"""Migration script to add session_id column to analyses table."""
import logging
from sqlalchemy import inspect, text
from app.db import engine
from app.core.config import settings

logger = logging.getLogger(__name__)

def migrate_database():
    """Add session_id column to analyses table if it doesn't exist."""
    try:
        # Check if table exists
        inspector = inspect(engine)
        if 'analyses' not in inspector.get_table_names():
            logger.info("analyses table does not exist yet. It will be created by SQLAlchemy.")
            return
        
        # Get existing columns
        columns = [col['name'] for col in inspector.get_columns('analyses')]
        
        # Check if session_id column exists
        if 'session_id' not in columns:
            logger.info("Adding session_id column to analyses table...")
            
            # Use raw SQL to add column (works for both SQLite and PostgreSQL)
            with engine.begin() as conn:
                # Check database type
                db_url = settings.database_url.lower()
                
                if 'postgresql' in db_url or 'postgres' in db_url:
                    # PostgreSQL syntax
                    conn.execute(text("""
                        ALTER TABLE analyses 
                        ADD COLUMN IF NOT EXISTS session_id VARCHAR(255)
                    """))
                    
                    # Create index
                    conn.execute(text("""
                        CREATE INDEX IF NOT EXISTS idx_analyses_session_id 
                        ON analyses(session_id)
                    """))
                else:
                    # SQLite syntax
                    conn.execute(text("""
                        ALTER TABLE analyses 
                        ADD COLUMN session_id VARCHAR(255)
                    """))
                    
                    # Create index
                    try:
                        conn.execute(text("""
                            CREATE INDEX IF NOT EXISTS idx_analyses_session_id 
                            ON analyses(session_id)
                        """))
                    except Exception as e:
                        logger.debug(f"Index might already exist: {e}")
                
                logger.info("[SUCCESS] Migration successful! session_id column added.")
        else:
            logger.info("[OK] session_id column already exists. No migration needed.")
            
    except Exception as e:
        logger.warning(f"Migration check failed (this is OK if column already exists): {e}")
        # Don't raise - let the app continue

if __name__ == "__main__":
    migrate_database()

