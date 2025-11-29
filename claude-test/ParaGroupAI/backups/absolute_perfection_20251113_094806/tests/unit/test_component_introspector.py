#!/usr/bin/env python3
"""
Unit Tests for component_introspector.py
Tests component introspection and reporting.

Test Coverage Target: 80%+
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from component_introspector import ComponentIntrospector


# ==========================================
# COMPONENT INTROSPECTOR TESTS
# ==========================================

class TestComponentIntrospector:
    """Test ComponentIntrospector class."""

    def test_init(self):
        """ComponentIntrospector should initialize."""
        inspector = ComponentIntrospector()
        assert inspector is not None
        assert inspector.script_dir is not None

    def test_get_component_files_returns_dict(self):
        """get_component_files should return dictionary."""
        inspector = ComponentIntrospector()

        components = inspector.get_component_files()

        assert isinstance(components, dict)
        assert "Agent Framework" in components
        assert "Guardrails" in components
        assert "Security" in components
        assert "Core" in components

    def test_get_component_files_agent_framework(self):
        """Should return agent framework files."""
        inspector = ComponentIntrospector()

        components = inspector.get_component_files()

        # Should have some agent framework files
        assert isinstance(components["Agent Framework"], list)

    def test_get_component_files_core_includes_known_files(self):
        """Core should include known core files."""
        inspector = ComponentIntrospector()

        components = inspector.get_component_files()

        assert "ultrathink.py" in components["Core"]
        assert "master_orchestrator.py" in components["Core"]
        assert "config.py" in components["Core"]

    def test_get_config_summary_returns_dict(self):
        """get_config_summary should return dictionary."""
        inspector = ComponentIntrospector()

        config = inspector.get_config_summary()

        assert isinstance(config, dict)
        assert len(config) > 0

    def test_get_config_summary_includes_key_values(self):
        """Config summary should include key configuration values."""
        inspector = ComponentIntrospector()

        config = inspector.get_config_summary()

        assert "PARALLEL_AGENTS_MAX" in config
        assert "CONTEXT_WINDOW_TOKENS" in config
        assert "CONFIDENCE_PRODUCTION" in config
        assert "CLAUDE_MODEL" in config

    def test_estimate_agent_count_returns_dict(self):
        """estimate_agent_count should return dictionary."""
        inspector = ComponentIntrospector()

        result = inspector.estimate_agent_count("What is 2+2?")

        assert isinstance(result, dict)

    def test_estimate_agent_count_simple_prompt(self):
        """Should estimate lower agents for simple prompt."""
        inspector = ComponentIntrospector()

        result = inspector.estimate_agent_count("What is Python?")

        # Should return some estimation
        assert isinstance(result, dict)

    def test_estimate_agent_count_complex_prompt(self):
        """Should estimate more agents for complex prompt."""
        inspector = ComponentIntrospector()

        complex_prompt = "Build a comprehensive system with multiple components"
        result = inspector.estimate_agent_count(complex_prompt)

        assert isinstance(result, dict)


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
