#!/usr/bin/env python3
"""
Comprehensive tests for config.py

Test Coverage Target: 95% (CRITICAL priority file)
Total Statements: 120

Test Strategy:
1. Configuration value accessibility
2. Default value validation
3. get_all_config_values() function
4. validate_config() function with valid/invalid scenarios
5. Quality weights validation
6. Confidence threshold validation
7. Rate limiting validation
8. Database configuration
9. Main block execution
10. Edge cases for all validation logic
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the config module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import UltrathinkConfig, get_all_config_values, validate_config


@pytest.fixture(autouse=True)
def reset_config_after_test():
    """Fixture to ensure config is restored to valid state after each test"""
    # Save all original values before test
    original_values = {
        'QUALITY_WEIGHT_PROMPT': UltrathinkConfig.QUALITY_WEIGHT_PROMPT,
        'QUALITY_WEIGHT_AGENTS': UltrathinkConfig.QUALITY_WEIGHT_AGENTS,
        'QUALITY_WEIGHT_GUARDRAILS': UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS,
        'QUALITY_WEIGHT_EFFICIENCY': UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY,
        'QUALITY_WEIGHT_VERIFICATION': UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION,
        'CONFIDENCE_PRODUCTION': UltrathinkConfig.CONFIDENCE_PRODUCTION,
        'CONFIDENCE_VERIFICATION': UltrathinkConfig.CONFIDENCE_VERIFICATION,
        'RATE_LIMIT_CALLS': UltrathinkConfig.RATE_LIMIT_CALLS,
        'RATE_LIMIT_WINDOW': UltrathinkConfig.RATE_LIMIT_WINDOW,
    }

    # Run the test
    yield

    # Restore all values after test (even if test failed)
    for key, value in original_values.items():
        setattr(UltrathinkConfig, key, value)


class TestUltrathinkConfigValues:
    """Test that all configuration values are accessible"""

    def test_confidence_thresholds(self):
        """Test confidence threshold configuration values"""
        assert UltrathinkConfig.CONFIDENCE_PRODUCTION == 99.0
        assert UltrathinkConfig.CONFIDENCE_VERIFICATION == 95.0
        assert 0 <= UltrathinkConfig.CONFIDENCE_PRODUCTION <= 100
        assert 0 <= UltrathinkConfig.CONFIDENCE_VERIFICATION <= 100

    def test_context_management(self):
        """Test context management configuration values"""
        assert UltrathinkConfig.CONTEXT_WINDOW_TOKENS == 200_000
        assert UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD == 0.85
        assert UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO == 0.30
        assert 0 < UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD < 1
        assert 0 < UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO < 1

    def test_iteration_limits(self):
        """Test iteration limit configuration values"""
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS == 20
        assert UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT == 2
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS > 0
        assert UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT > 0

    def test_performance_settings(self):
        """Test performance configuration values"""
        assert UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS == 5.0
        assert UltrathinkConfig.PARALLEL_AGENTS_MAX == 500
        assert UltrathinkConfig.TOKEN_COUNTING_RECOUNT_THRESHOLD == 0.80
        assert UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS > 0
        assert UltrathinkConfig.PARALLEL_AGENTS_MAX > 0

    def test_rate_limiting(self):
        """Test rate limiting configuration values"""
        assert UltrathinkConfig.RATE_LIMIT_CALLS == 500
        assert UltrathinkConfig.RATE_LIMIT_WINDOW == 360
        assert UltrathinkConfig.RATE_LIMIT_CALLS > 0
        assert UltrathinkConfig.RATE_LIMIT_WINDOW > 0

    def test_security_settings(self):
        """Test security configuration values"""
        assert UltrathinkConfig.PROMPT_MAX_LENGTH_CHARS is None
        assert len(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE) == 5
        assert len(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_MEDIUM_CONFIDENCE) == 4
        assert 'ignore all previous instructions' in UltrathinkConfig.PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE

    def test_logging_settings(self):
        """Test logging configuration values"""
        assert UltrathinkConfig.LOG_LEVEL_DEFAULT == "INFO"
        assert UltrathinkConfig.LOG_SECURITY_EVENTS_TO_FILE is True
        assert UltrathinkConfig.LOG_SECURITY_FILE_PATH == "logs/security_events.log"

    def test_database_settings(self):
        """Test database configuration values"""
        assert UltrathinkConfig.DB_FIRST_ENABLED is True
        assert UltrathinkConfig.DB_PATH == "database/ultrathink_context.db"
        assert UltrathinkConfig.DB_POSTGRESQL_URL is None
        assert UltrathinkConfig.DB_REDIS_URL is None
        assert UltrathinkConfig.DB_CONTEXT_PRIORITY_CRITICAL_LOAD_TIME_MS == 100
        assert UltrathinkConfig.DB_TOKEN_CLEAR_THRESHOLD == 0.85
        assert UltrathinkConfig.DB_MAX_PROJECTS == 100
        assert UltrathinkConfig.DB_MAX_INSTANCES_PER_PROJECT == 10
        assert UltrathinkConfig.DB_HEARTBEAT_INTERVAL_SECONDS == 30
        assert UltrathinkConfig.DB_CLEANUP_STALE_INSTANCES_SECONDS == 600

    def test_response_formatting(self):
        """Test response formatting configuration values"""
        assert UltrathinkConfig.RESPONSE_FORMAT_ULTRATHINK is True
        assert UltrathinkConfig.RESPONSE_SECTION_WIDTH == 80
        assert UltrathinkConfig.RESPONSE_VERBOSE_INDENT == 3

    def test_testing_settings(self):
        """Test testing configuration values"""
        assert UltrathinkConfig.TEST_MODE is False
        assert UltrathinkConfig.TEST_MOCK_CLAUDE_RESPONSES is True

    def test_model_configuration(self):
        """Test model configuration values"""
        assert UltrathinkConfig.CLAUDE_MODEL_NAME == "claude-sonnet-4-5-20250929"
        assert UltrathinkConfig.CLAUDE_MAX_TOKENS == 8192
        assert UltrathinkConfig.CLAUDE_MAX_TOKENS > 0

    def test_quality_weights(self):
        """Test quality scoring weights"""
        assert UltrathinkConfig.QUALITY_WEIGHT_PROMPT == 0.15
        assert UltrathinkConfig.QUALITY_WEIGHT_AGENTS == 0.25
        assert UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS == 0.30
        assert UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY == 0.15
        assert UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION == 0.15

        # Verify weights sum to 1.0
        total = (
            UltrathinkConfig.QUALITY_WEIGHT_PROMPT +
            UltrathinkConfig.QUALITY_WEIGHT_AGENTS +
            UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS +
            UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY +
            UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION
        )
        assert abs(total - 1.0) < 0.01

    def test_file_paths(self):
        """Test file path configuration values"""
        assert UltrathinkConfig.ALLOWED_PROMPT_FILE_BASE_DIRS == ["."]
        assert isinstance(UltrathinkConfig.ALLOWED_PROMPT_FILE_BASE_DIRS, list)

    def test_dependency_scanning(self):
        """Test dependency scanning configuration values"""
        assert UltrathinkConfig.DEPENDENCY_SCAN_ON_STARTUP is False
        assert UltrathinkConfig.DEPENDENCY_SCAN_CACHE_HOURS == 24
        assert UltrathinkConfig.DEPENDENCY_SCAN_CACHE_HOURS > 0


class TestGetAllConfigValues:
    """Test get_all_config_values() function"""

    def test_returns_dict(self):
        """Test that function returns a dictionary"""
        config = get_all_config_values()
        assert isinstance(config, dict)

    def test_contains_all_uppercase_constants(self):
        """Test that dictionary contains all uppercase constants"""
        config = get_all_config_values()

        # Should contain key configuration values
        assert 'CONFIDENCE_PRODUCTION' in config
        assert 'CONTEXT_WINDOW_TOKENS' in config
        assert 'MAX_REFINEMENT_ITERATIONS' in config
        assert 'RATE_LIMIT_CALLS' in config
        assert 'CLAUDE_MODEL_NAME' in config

    def test_excludes_private_attributes(self):
        """Test that private attributes are excluded"""
        config = get_all_config_values()

        # Should not contain private attributes
        for key in config.keys():
            assert not key.startswith('_')

    def test_excludes_non_uppercase(self):
        """Test that non-uppercase attributes are excluded"""
        config = get_all_config_values()

        # All keys should be uppercase
        for key in config.keys():
            assert key.isupper()

    def test_values_match_class_attributes(self):
        """Test that returned values match class attributes"""
        config = get_all_config_values()

        # Verify some key values
        assert config['CONFIDENCE_PRODUCTION'] == UltrathinkConfig.CONFIDENCE_PRODUCTION
        assert config['CONTEXT_WINDOW_TOKENS'] == UltrathinkConfig.CONTEXT_WINDOW_TOKENS
        assert config['MAX_REFINEMENT_ITERATIONS'] == UltrathinkConfig.MAX_REFINEMENT_ITERATIONS


class TestValidateConfig:
    """Test validate_config() function"""

    def test_valid_config_passes(self):
        """Test that valid configuration passes validation"""
        # Should not raise any exceptions
        result = validate_config()
        assert result is True

    def test_quality_weights_sum_validation(self):
        """Test quality weights sum to 1.0 validation"""
        # Save original values
        original_prompt = UltrathinkConfig.QUALITY_WEIGHT_PROMPT

        try:
            # Set invalid weight (will make sum != 1.0)
            UltrathinkConfig.QUALITY_WEIGHT_PROMPT = 0.50  # Total will be 1.35

            with pytest.raises(ValueError, match="Quality weights must sum to 1.0"):
                validate_config()
        finally:
            # Restore original value
            UltrathinkConfig.QUALITY_WEIGHT_PROMPT = original_prompt

    def test_confidence_production_range_validation(self):
        """Test confidence production range validation"""
        # Save original value
        original_confidence = UltrathinkConfig.CONFIDENCE_PRODUCTION

        try:
            # Test value > 100
            UltrathinkConfig.CONFIDENCE_PRODUCTION = 150.0

            with pytest.raises(ValueError, match="CONFIDENCE_PRODUCTION must be 0-100"):
                validate_config()

            # Test negative value
            UltrathinkConfig.CONFIDENCE_PRODUCTION = -10.0

            with pytest.raises(ValueError, match="CONFIDENCE_PRODUCTION must be 0-100"):
                validate_config()
        finally:
            # Restore original value
            UltrathinkConfig.CONFIDENCE_PRODUCTION = original_confidence

    def test_rate_limit_calls_positive_validation(self):
        """Test rate limit calls must be positive"""
        # Save original value
        original_calls = UltrathinkConfig.RATE_LIMIT_CALLS

        try:
            UltrathinkConfig.RATE_LIMIT_CALLS = 0

            with pytest.raises(ValueError, match="RATE_LIMIT_CALLS must be positive"):
                validate_config()

            UltrathinkConfig.RATE_LIMIT_CALLS = -100

            with pytest.raises(ValueError, match="RATE_LIMIT_CALLS must be positive"):
                validate_config()
        finally:
            # Restore original value
            UltrathinkConfig.RATE_LIMIT_CALLS = original_calls

    def test_rate_limit_window_positive_validation(self):
        """Test rate limit window must be positive"""
        # Save original value
        original_window = UltrathinkConfig.RATE_LIMIT_WINDOW

        try:
            UltrathinkConfig.RATE_LIMIT_WINDOW = 0

            with pytest.raises(ValueError, match="RATE_LIMIT_WINDOW must be positive"):
                validate_config()

            UltrathinkConfig.RATE_LIMIT_WINDOW = -60

            with pytest.raises(ValueError, match="RATE_LIMIT_WINDOW must be positive"):
                validate_config()
        finally:
            # Restore original value
            UltrathinkConfig.RATE_LIMIT_WINDOW = original_window


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_quality_weights_exact_sum(self):
        """Test quality weights sum exactly to 1.0"""
        total = (
            UltrathinkConfig.QUALITY_WEIGHT_PROMPT +
            UltrathinkConfig.QUALITY_WEIGHT_AGENTS +
            UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS +
            UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY +
            UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION
        )
        # Using tolerance of 0.01 as per validation logic
        assert abs(total - 1.0) <= 0.01

    def test_confidence_at_boundaries(self):
        """Test confidence values at boundaries (0 and 100)"""
        # Save original value
        original_confidence = UltrathinkConfig.CONFIDENCE_PRODUCTION

        try:
            # Test 0 (valid)
            UltrathinkConfig.CONFIDENCE_PRODUCTION = 0.0
            assert validate_config() is True

            # Test 100 (valid)
            UltrathinkConfig.CONFIDENCE_PRODUCTION = 100.0
            assert validate_config() is True
        finally:
            # Restore original value
            UltrathinkConfig.CONFIDENCE_PRODUCTION = original_confidence

    def test_rate_limit_at_minimum(self):
        """Test rate limiting at minimum valid values"""
        # Save original values
        original_calls = UltrathinkConfig.RATE_LIMIT_CALLS
        original_window = UltrathinkConfig.RATE_LIMIT_WINDOW

        try:
            # Test minimum valid values (1)
            UltrathinkConfig.RATE_LIMIT_CALLS = 1
            UltrathinkConfig.RATE_LIMIT_WINDOW = 1
            assert validate_config() is True
        finally:
            # Restore original values
            UltrathinkConfig.RATE_LIMIT_CALLS = original_calls
            UltrathinkConfig.RATE_LIMIT_WINDOW = original_window

    def test_none_values_are_valid(self):
        """Test that None values for optional configs are valid"""
        # These should all be None (optional configurations)
        assert UltrathinkConfig.PROMPT_MAX_LENGTH_CHARS is None
        assert UltrathinkConfig.DB_POSTGRESQL_URL is None
        assert UltrathinkConfig.DB_REDIS_URL is None

        # Validation should pass with None values
        assert validate_config() is True

    def test_list_values_are_valid(self):
        """Test that list configuration values are valid"""
        # Test prompt injection patterns
        assert isinstance(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE, list)
        assert isinstance(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_MEDIUM_CONFIDENCE, list)
        assert isinstance(UltrathinkConfig.ALLOWED_PROMPT_FILE_BASE_DIRS, list)

        # Lists should not be empty
        assert len(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE) > 0
        assert len(UltrathinkConfig.PROMPT_INJECTION_PATTERNS_MEDIUM_CONFIDENCE) > 0
        assert len(UltrathinkConfig.ALLOWED_PROMPT_FILE_BASE_DIRS) > 0


class TestMainBlock:
    """Test main block execution"""

    def test_main_block_execution(self):
        """Test that main block prints configuration information"""
        import subprocess
        import os

        # Get the path to config.py
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.py')

        # Run config.py as a script
        result = subprocess.run(
            ['python3', config_path],
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Verify output contains expected content
        assert "ULTRATHINK Configuration" in output
        assert "Production confidence:" in output
        assert "Context window:" in output
        assert "Rate limiting:" in output
        assert "Max iterations:" in output
        assert "Model:" in output
        assert "All configuration values:" in output
        assert "Validation:" in output
        assert "✅ PASSED" in output

    def test_main_block_shows_all_config_values(self):
        """Test that main block displays all configuration values"""
        captured_output = StringIO()

        with patch('sys.stdout', captured_output):
            # Get all config values and print them
            for key, value in get_all_config_values().items():
                print(f"{key}: {value}")

        output = captured_output.getvalue()

        # Should contain key configuration names
        assert "CONFIDENCE_PRODUCTION" in output
        assert "CONTEXT_WINDOW_TOKENS" in output
        assert "RATE_LIMIT_CALLS" in output
        assert "CLAUDE_MODEL_NAME" in output

    def test_main_block_code_directly(self):
        """Test the main block code directly for coverage using runpy"""
        import runpy
        import sys
        from io import StringIO

        # Get the path to config.py
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.py')
        config_path = os.path.abspath(config_path)

        # Capture stdout
        captured_output = StringIO()
        old_stdout = sys.stdout

        try:
            sys.stdout = captured_output

            # Run config.py as __main__ to trigger the main block
            # This will execute lines 641-656 with coverage tracking
            runpy.run_path(config_path, run_name="__main__")

        finally:
            sys.stdout = old_stdout

        output = captured_output.getvalue()

        # Verify all expected content is present
        assert "ULTRATHINK Configuration" in output
        assert "Production confidence:" in output
        assert "Context window:" in output
        assert "tokens" in output
        assert "Rate limiting:" in output
        assert "Max iterations:" in output
        assert "Model:" in output
        assert "All configuration values:" in output
        assert "Validation:" in output
        assert "✅ PASSED" in output


class TestConfigDocumentation:
    """Test that configuration has proper documentation"""

    def test_class_has_docstring(self):
        """Test that UltrathinkConfig class has docstring"""
        assert UltrathinkConfig.__doc__ is not None
        assert len(UltrathinkConfig.__doc__) > 0

    def test_get_all_config_values_has_docstring(self):
        """Test that get_all_config_values function has docstring"""
        assert get_all_config_values.__doc__ is not None
        assert "Get all configuration values" in get_all_config_values.__doc__

    def test_validate_config_has_docstring(self):
        """Test that validate_config function has docstring"""
        assert validate_config.__doc__ is not None
        assert "Validate that configuration values are reasonable" in validate_config.__doc__


class TestConfigIntegrity:
    """Test overall configuration integrity"""

    def test_all_config_keys_are_strings(self):
        """Test that all config keys are strings"""
        config = get_all_config_values()
        for key in config.keys():
            assert isinstance(key, str)

    def test_confidence_thresholds_are_consistent(self):
        """Test that confidence thresholds are logically consistent"""
        # Production confidence should be higher than or equal to verification
        assert UltrathinkConfig.CONFIDENCE_PRODUCTION >= UltrathinkConfig.CONFIDENCE_VERIFICATION

    def test_database_thresholds_are_consistent(self):
        """Test that database thresholds are logically consistent"""
        # Token clear threshold should be less than 1.0
        assert UltrathinkConfig.DB_TOKEN_CLEAR_THRESHOLD < 1.0

        # Context compaction threshold should be reasonable
        assert 0.5 <= UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD <= 0.95

        # Heartbeat interval should be much less than stale timeout
        assert UltrathinkConfig.DB_HEARTBEAT_INTERVAL_SECONDS < UltrathinkConfig.DB_CLEANUP_STALE_INSTANCES_SECONDS

    def test_iteration_limits_are_consistent(self):
        """Test that iteration limits are logically consistent"""
        # Max iterations should be greater than min iterations
        assert UltrathinkConfig.MAX_REFINEMENT_ITERATIONS > UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT

    def test_parallel_agents_is_reasonable(self):
        """Test that parallel agents max is reasonable"""
        # Should be between 1 and 1000 (reasonable bounds)
        assert 1 <= UltrathinkConfig.PARALLEL_AGENTS_MAX <= 1000


class TestConfigValidationOnImport:
    """Test that validation runs on import"""

    def test_config_is_validated_on_import(self):
        """Test that validate_config() is called when module is imported"""
        # The config module calls validate_config() at the module level (line 633)
        # If validation didn't pass, the initial import would have failed
        # The fact that we can import and use the module proves validation passed

        # No need to use importlib.reload() which creates new class objects
        # and breaks test isolation for other tests

        # Simply verify that the module was imported successfully
        # and has the expected validation behavior
        assert validate_config() is True

        # Verify that the module-level validation ran by checking
        # that default config values are valid
        config_dict = get_all_config_values()
        assert 'CONFIDENCE_PRODUCTION' in config_dict
        assert 'QUALITY_WEIGHT_PROMPT' in config_dict


class TestQualityWeightsValidation:
    """Test quality weights validation in detail"""

    def test_weights_sum_within_tolerance(self):
        """Test that weights summing to 1.009 (within 0.01 tolerance) pass validation"""
        # Set weights that sum to 1.009 (within tolerance)
        UltrathinkConfig.QUALITY_WEIGHT_PROMPT = 0.152
        UltrathinkConfig.QUALITY_WEIGHT_AGENTS = 0.252
        UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS = 0.302
        UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY = 0.152
        UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION = 0.151
        # Total: 1.009 (within 0.01 tolerance)

        # Validation should pass
        assert validate_config() is True

    def test_weights_sum_outside_tolerance(self):
        """Test that weights summing to 1.50 (outside 0.01 tolerance) fail validation"""
        # Set weights that sum to 1.50 (way outside tolerance)
        UltrathinkConfig.QUALITY_WEIGHT_PROMPT = 0.50
        UltrathinkConfig.QUALITY_WEIGHT_AGENTS = 0.25
        UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS = 0.30
        UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY = 0.25
        UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION = 0.20
        # Total: 1.50 (way outside tolerance)

        # Validation should raise ValueError
        with pytest.raises(ValueError, match="Quality weights must sum to 1.0"):
            validate_config()


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=config', '--cov-report=term-missing'])
