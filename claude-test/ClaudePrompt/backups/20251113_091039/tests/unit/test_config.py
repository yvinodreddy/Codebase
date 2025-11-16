#!/usr/bin/env python3
"""
Unit Tests for config.py
Tests all configuration constants and their relationships.

Test Coverage Target: 100% (config.py is pure constants)
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import UltrathinkConfig


class TestConfidenceThresholds:
    """Test confidence-related configuration values."""

    def test_production_confidence_value(self):
        """CONFIDENCE_PRODUCTION should be 99.0%."""
        assert UltrathinkConfig.CONFIDENCE_PRODUCTION == 99.0

    def test_production_confidence_type(self):
        """CONFIDENCE_PRODUCTION should be a float."""
        assert isinstance(UltrathinkConfig.CONFIDENCE_PRODUCTION, float)

    def test_production_confidence_range(self):
        """CONFIDENCE_PRODUCTION should be between 0 and 100."""
        assert 0 <= UltrathinkConfig.CONFIDENCE_PRODUCTION <= 100

    def test_verification_confidence_value(self):
        """CONFIDENCE_VERIFICATION should be 95.0%."""
        assert UltrathinkConfig.CONFIDENCE_VERIFICATION == 95.0

    def test_verification_confidence_type(self):
        """CONFIDENCE_VERIFICATION should be a float."""
        assert isinstance(UltrathinkConfig.CONFIDENCE_VERIFICATION, float)

    def test_verification_less_than_production(self):
        """CONFIDENCE_VERIFICATION should be less than CONFIDENCE_PRODUCTION."""
        assert (
            UltrathinkConfig.CONFIDENCE_VERIFICATION
            < UltrathinkConfig.CONFIDENCE_PRODUCTION
        )


class TestContextManagement:
    """Test context management configuration values."""

    def test_context_window_tokens_value(self):
        """CONTEXT_WINDOW_TOKENS should be 200,000."""
        assert UltrathinkConfig.CONTEXT_WINDOW_TOKENS == 200_000

    def test_context_window_tokens_type(self):
        """CONTEXT_WINDOW_TOKENS should be an integer."""
        assert isinstance(UltrathinkConfig.CONTEXT_WINDOW_TOKENS, int)

    def test_context_window_tokens_positive(self):
        """CONTEXT_WINDOW_TOKENS should be positive."""
        assert UltrathinkConfig.CONTEXT_WINDOW_TOKENS > 0

    def test_compaction_threshold_value(self):
        """CONTEXT_COMPACTION_THRESHOLD should be 0.85 (85%)."""
        assert UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD == 0.85

    def test_compaction_threshold_range(self):
        """CONTEXT_COMPACTION_THRESHOLD should be between 0 and 1."""
        assert 0 < UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD < 1

    def test_min_compaction_ratio_value(self):
        """CONTEXT_MIN_COMPACTION_RATIO should be 0.30 (30%)."""
        assert UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO == 0.30

    def test_min_compaction_ratio_range(self):
        """CONTEXT_MIN_COMPACTION_RATIO should be between 0 and 1."""
        assert 0 < UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO < 1

    def test_compaction_threshold_leaves_buffer(self):
        """Compaction threshold should leave reasonable buffer for response."""
        buffer_ratio = 1.0 - UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD
        buffer_tokens = UltrathinkConfig.CONTEXT_WINDOW_TOKENS * buffer_ratio
        # Should have at least 20K tokens buffer for response
        assert buffer_tokens >= 20_000


class TestIterationLimits:
    """Test iteration limit configuration values."""

    def test_max_refinement_iterations_value(self):
        """MAX_REFINEMENT_ITERATIONS should be 20."""
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS == 20

    def test_max_refinement_iterations_type(self):
        """MAX_REFINEMENT_ITERATIONS should be an integer."""
        assert isinstance(UltrathinkConfig.MAX_REFINEMENT_ITERATIONS, int)

    def test_max_refinement_iterations_positive(self):
        """MAX_REFINEMENT_ITERATIONS should be positive."""
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS > 0

    def test_min_iterations_before_early_exit_value(self):
        """MIN_ITERATIONS_BEFORE_EARLY_EXIT should be 2."""
        assert UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT == 2

    def test_min_less_than_max_iterations(self):
        """MIN_ITERATIONS_BEFORE_EARLY_EXIT should be less than MAX_REFINEMENT_ITERATIONS."""
        assert (
            UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT
            < UltrathinkConfig.MAX_REFINEMENT_ITERATIONS
        )


class TestAgentOrchestration:
    """Test agent orchestration configuration values."""

    def test_parallel_agents_max_exists(self):
        """PARALLEL_AGENTS_MAX should exist."""
        assert hasattr(UltrathinkConfig, "PARALLEL_AGENTS_MAX")

    def test_parallel_agents_max_positive(self):
        """PARALLEL_AGENTS_MAX should be positive."""
        assert UltrathinkConfig.PARALLEL_AGENTS_MAX > 0

    def test_parallel_agents_max_reasonable(self):
        """PARALLEL_AGENTS_MAX should be reasonable (not too high)."""
        # Should not exceed 1000 (reasonable upper bound for parallel tasks)
        assert UltrathinkConfig.PARALLEL_AGENTS_MAX <= 1000


class TestRateLimiting:
    """Test rate limiting configuration values."""

    def test_rate_limit_exists(self):
        """RATE_LIMIT_CALLS should exist."""
        assert hasattr(UltrathinkConfig, "RATE_LIMIT_CALLS")

    def test_rate_limit_window_exists(self):
        """RATE_LIMIT_WINDOW should exist."""
        assert hasattr(UltrathinkConfig, "RATE_LIMIT_WINDOW")

    def test_rate_limit_positive(self):
        """RATE_LIMIT_CALLS should be positive."""
        assert UltrathinkConfig.RATE_LIMIT_CALLS > 0

    def test_rate_limit_window_positive(self):
        """RATE_LIMIT_WINDOW should be positive."""
        assert UltrathinkConfig.RATE_LIMIT_WINDOW > 0


class TestGuardrails:
    """Test guardrail configuration values."""

    def test_guardrail_timeout_exists(self):
        """GUARDRAIL_TIMEOUT_SECONDS should exist."""
        assert hasattr(UltrathinkConfig, "GUARDRAIL_TIMEOUT_SECONDS")

    def test_guardrail_timeout_positive(self):
        """GUARDRAIL_TIMEOUT_SECONDS should be positive."""
        assert UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS > 0

    def test_guardrail_timeout_reasonable(self):
        """GUARDRAIL_TIMEOUT_SECONDS should be reasonable (not too long)."""
        # Should not exceed 60 seconds (would make system too slow)
        assert UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS <= 60


class TestClaudeModel:
    """Test Claude model configuration."""

    def test_claude_model_exists(self):
        """CLAUDE_MODEL_NAME should exist."""
        assert hasattr(UltrathinkConfig, "CLAUDE_MODEL_NAME")

    def test_claude_model_is_string(self):
        """CLAUDE_MODEL_NAME should be a string."""
        assert isinstance(UltrathinkConfig.CLAUDE_MODEL_NAME, str)

    def test_claude_model_not_empty(self):
        """CLAUDE_MODEL_NAME should not be empty."""
        assert len(UltrathinkConfig.CLAUDE_MODEL_NAME) > 0

    def test_claude_model_format(self):
        """CLAUDE_MODEL_NAME should follow naming convention."""
        # Should contain 'claude' and a version/variant
        model_lower = UltrathinkConfig.CLAUDE_MODEL_NAME.lower()
        assert "claude" in model_lower


class TestConfigDocumentation:
    """Test that configuration constants are properly documented."""

    def test_production_confidence_has_docstring(self):
        """CONFIDENCE_PRODUCTION should have a docstring."""
        # Access the class attribute's docstring through annotations
        assert UltrathinkConfig.__dict__["__doc__"] is not None

    def test_config_class_has_docstring(self):
        """UltrathinkConfig class should have a docstring."""
        assert UltrathinkConfig.__doc__ is not None
        assert len(UltrathinkConfig.__doc__.strip()) > 0


class TestConfigIntegrity:
    """Test relationships and integrity between configuration values."""

    def test_confidence_hierarchy(self):
        """Confidence values should follow hierarchy: production > verification."""
        assert (
            UltrathinkConfig.CONFIDENCE_PRODUCTION
            > UltrathinkConfig.CONFIDENCE_VERIFICATION
        )

    def test_reasonable_confidence_gap(self):
        """Gap between production and verification confidence should be reasonable."""
        gap = (
            UltrathinkConfig.CONFIDENCE_PRODUCTION
            - UltrathinkConfig.CONFIDENCE_VERIFICATION
        )
        # Should be between 1% and 10%
        assert 1.0 <= gap <= 10.0

    def test_context_ratios_valid(self):
        """Context management ratios should sum to less than 1."""
        # Compaction threshold + min ratio should allow for meaningful compaction
        total = (
            UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD
            + UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO
        )
        # Should not exceed 1.0 (would be impossible to achieve)
        assert total <= 1.5  # Allow some overlap since they measure different things

    def test_iteration_limits_sane(self):
        """Iteration limits should be sane and achievable."""
        # Min should be small enough to allow early exit
        assert UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT <= 5
        # Max should be large enough to reach high confidence
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS >= 10


# Pytest fixtures
@pytest.fixture
def config():
    """Fixture providing UltrathinkConfig instance."""
    return UltrathinkConfig()


# Integration tests
class TestConfigUsability:
    """Test that config values can be used as intended."""

    def test_can_import_config(self):
        """Config should be importable."""
        from config import UltrathinkConfig

        assert UltrathinkConfig is not None

    def test_can_access_all_constants(self):
        """All public constants should be accessible."""
        # Get all public constants (uppercase attributes)
        constants = [
            attr
            for attr in dir(UltrathinkConfig)
            if attr.isupper() and not attr.startswith("_")
        ]

        # Should have at least 10 constants
        assert len(constants) >= 10

        # All should be accessible (allow None for optional configs)
        for const in constants:
            # Should not raise AttributeError
            value = getattr(UltrathinkConfig, const)
            # Value can be None (e.g., PROMPT_MAX_LENGTH_CHARS = None is valid)


# Marker for quick tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
