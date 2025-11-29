"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_process_prompt():
    response = client.post("/v1/prompt", json={
        "prompt": "test prompt",
        "verbose": False
    })
    assert response.status_code == 200
    assert "response" in response.json()
    assert "confidence" in response.json()
