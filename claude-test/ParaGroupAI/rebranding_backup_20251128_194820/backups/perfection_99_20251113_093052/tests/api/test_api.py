"""
Comprehensive tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from api.main import app

client = TestClient(app)

@pytest.mark.api
def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "endpoints" in data

@pytest.mark.api
def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

@pytest.mark.api
def test_readiness():
    """Test readiness endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data

@pytest.mark.api
def test_process_prompt():
    """Test prompt processing endpoint"""
    response = client.post("/v1/prompt", json={
        "prompt": "test prompt",
        "verbose": False
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "confidence" in data
    assert "success" in data
    assert data["success"] is True

@pytest.mark.api
def test_process_prompt_with_options():
    """Test prompt processing with custom options"""
    response = client.post("/v1/prompt", json={
        "prompt": "detailed test prompt",
        "verbose": True,
        "max_iterations": 10,
        "confidence_threshold": 95.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["confidence"] >= 0.0

@pytest.mark.api
def test_get_status():
    """Test status endpoint"""
    response = client.get("/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "features" in data
