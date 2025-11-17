"""Migration script to add session_id column to analyses table."""
import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Add session_id column to analyses table if it doesn't exist."""
    # Find database file
    db_paths = [
        Path(__file__).parent.parent.parent / "contract_analyzer.db",
        Path(__file__).parent.parent.parent.parent / "contract_analyzer.db",
        Path.home() / ".contract_analyzer" / "contract_analyzer.db",
    ]
    
    db_path = None
    for path in db_paths:
        if path.exists():
            db_path = path
            break
    
    if not db_path:
        # Try to get from environment or use default
        db_path = Path(os.getenv("DATABASE_PATH", "contract_analyzer.db"))
        if not db_path.is_absolute():
            db_path = Path(__file__).parent.parent.parent / db_path
    
    print(f"Checking database at: {db_path}")
    
    if not db_path.exists():
        print(f"Database not found at {db_path}. It will be created on first run.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check if session_id column exists
        cursor.execute("PRAGMA table_info(analyses)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'session_id' not in columns:
            print("Adding session_id column to analyses table...")
            cursor.execute("""
                ALTER TABLE analyses 
                ADD COLUMN session_id VARCHAR(255)
            """)
            
            # Create index for better performance
            try:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_analyses_session_id 
                    ON analyses(session_id)
                """)
                print("Created index on session_id")
            except Exception as e:
                print(f"Index might already exist: {e}")
            
            conn.commit()
            print("[SUCCESS] Migration successful! session_id column added.")
        else:
            print("[OK] session_id column already exists. No migration needed.")
        
        # Verify
        cursor.execute("PRAGMA table_info(analyses)")
        columns = cursor.fetchall()
        print("\nCurrent table structure:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
    except Exception as e:
        print(f"[ERROR] Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

