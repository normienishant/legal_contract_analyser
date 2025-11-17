"""Tests for API endpoints."""
import pytest
import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_file():
    """Create a test file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test contract clause. The party agrees to the terms.")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_upload_file(test_file):
    """Test file upload endpoint."""
    with open(test_file, 'rb') as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert "filename" in data
    assert data["message"] == "File uploaded successfully"


def test_upload_invalid_file_type():
    """Test upload with invalid file type."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.exe', delete=False) as f:
        f.write("test")
        temp_path = f.name
    
    try:
        with open(temp_path, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test.exe", f, "application/x-msdownload")}
            )
        
        assert response.status_code == 400
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_extract_text(test_file):
    """Test text extraction endpoint."""
    # First upload
    with open(test_file, 'rb') as f:
        upload_response = client.post(
            "/api/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    
    file_id = upload_response.json()["file_id"]
    
    # Then extract
    response = client.post(f"/api/extract?file_id={file_id}")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "clauses" in data
    assert "clause_count" in data


def test_analyze_document(test_file):
    """Test document analysis endpoint."""
    # First upload
    with open(test_file, 'rb') as f:
        upload_response = client.post(
            "/api/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    
    file_id = upload_response.json()["file_id"]
    
    # Then analyze
    response = client.post(f"/api/analyze?file_id={file_id}")
    assert response.status_code == 200
    data = response.json()
    assert "analysis_id" in data
    assert "analysis" in data
    assert "global_risk_score" in data["analysis"]
    assert "clauses" in data["analysis"]


def test_get_history():
    """Test history endpoint."""
    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_analysis_by_id(test_file):
    """Test getting analysis by ID."""
    # Upload and analyze
    with open(test_file, 'rb') as f:
        upload_response = client.post(
            "/api/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    
    file_id = upload_response.json()["file_id"]
    analyze_response = client.post(f"/api/analyze?file_id={file_id}")
    analysis_id = analyze_response.json()["analysis_id"]
    
    # Get analysis
    response = client.get(f"/api/history/{analysis_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["analysis_id"] == analysis_id
    assert "analysis" in data

