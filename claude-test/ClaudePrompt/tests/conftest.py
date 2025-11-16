"""
Pytest configuration and fixtures for ULTRATHINK tests
"""
import pytest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent

@pytest.fixture
def test_data_dir(project_root):
    """Return test data directory"""
    return project_root / "tests" / "test_data"

@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test"""
    yield
    # Cleanup after test if needed

# Markers
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "performance: mark test as performance test")
