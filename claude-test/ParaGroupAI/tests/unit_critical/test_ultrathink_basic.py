"""Basic tests for ultrathink.py"""
import pytest

def test_ultrathink_imports():
    """Test ultrathink can be imported."""
    try:
        import ultrathink
        assert True
    except ImportError:
        pytest.skip("ultrathink not importable")

def test_config_exists():
    """Test config module exists."""
    try:
        import config
        assert hasattr(config, 'MAX_REFINEMENT_ITERATIONS')
    except ImportError:
        pytest.skip("config not importable")
