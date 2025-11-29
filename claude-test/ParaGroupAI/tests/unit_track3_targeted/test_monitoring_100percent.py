#!/usr/bin/env python3
"""
TARGETED TESTS for monitoring.py - Push to 100% Coverage
Targets the remaining 9 uncovered lines
"""

import pytest
import sys
import tempfile
import os
import logging
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "guardrails"))

try:
    from monitoring import GuardrailMonitor, GuardrailEvent, get_monitor
except ImportError as e:
    pytest.skip(f"Cannot import monitoring: {e}", allow_module_level=True)


class TestMonitoring100Percent:
    """Tests to achieve 100% coverage"""

    def test_logging_basicConfig_execution(self):
        """Test line 27: logging.basicConfig() is called"""
        # This tests the module-level logging setup
        # The code checks: if not logging.getLogger().handlers:

        # Clear existing handlers to trigger basicConfig
        logger = logging.getLogger()
        original_handlers = logger.handlers.copy()

        try:
            # Clear handlers
            logger.handlers.clear()

            # Re-import module to trigger logging setup
            import importlib
            import monitoring
            importlib.reload(monitoring)

            # Verify logging was configured
            assert len(logging.getLogger().handlers) > 0

        finally:
            # Restore original handlers
            logger.handlers.clear()
            for handler in original_handlers:
                logger.addHandler(handler)

    def test_log_validation_failed_with_known_layer(self):
        """Test lines 153-157: Failed validation with known layer in layer_stats"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Log a FAILED validation for a known layer (layer_1_prompt_shields)
                # This should trigger lines 153-157
                monitor.log_validation(
                    layer="layer_1_prompt_shields",
                    passed=False,  # Failed validation
                    message="Test failed validation"
                )

                # Verify metrics updated correctly
                assert monitor.metrics["failed_validations"] >= 1
                assert monitor.metrics["layer_stats"]["layer_1_prompt_shields"]["failed"] >= 1

    def test_log_validation_passed_with_known_layer(self):
        """Test line 153: Passed validation increments layer stats"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Log a PASSED validation for known layer
                monitor.log_validation(
                    layer="layer_2_input_content",
                    passed=True,  # Passed validation
                    message="Test passed validation"
                )

                # Verify line 153 was executed
                assert monitor.metrics["successful_validations"] >= 1
                assert monitor.metrics["layer_stats"]["layer_2_input_content"]["passed"] >= 1

    def test_get_layer_performance_with_actual_stats(self):
        """Test lines 233-237: get_layer_performance with layer that has stats"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Add some actual stats to a layer
                monitor.log_validation("layer_3_phi_detection", passed=True, message="test1")
                monitor.log_validation("layer_3_phi_detection", passed=True, message="test2")
                monitor.log_validation("layer_3_phi_detection", passed=False, message="test3")

                # This should execute lines 233-237 (the success path)
                result = monitor.get_layer_performance("layer_3_phi_detection")

                # Verify the calculation
                assert "layer" in result
                assert result["layer"] == "layer_3_phi_detection"
                assert "total_validations" in result
                assert result["total_validations"] == 3
                assert "passed" in result
                assert result["passed"] == 2
                assert "failed" in result
                assert result["failed"] == 1
                assert "pass_rate" in result
                assert result["pass_rate"] == pytest.approx(66.67, abs=0.1)

    def test_get_layer_performance_with_zero_total(self):
        """Test line 235: pass_rate calculation when total is 0"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Get performance for layer with zero validations
                # This tests the "if total > 0 else 0" part of line 235
                result = monitor.get_layer_performance("layer_4_terminology")

                assert result["total_validations"] == 0
                assert result["pass_rate"] == 0

    def test_log_validation_all_layers_coverage(self):
        """Test validation logging for all predefined layers"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Test all layers to ensure full coverage
                layers = [
                    "layer_1_prompt_shields",
                    "layer_2_input_content",
                    "layer_3_phi_detection",
                    "layer_4_terminology",
                    "layer_5_output_content",
                    "layer_6_groundedness",
                    "layer_7_compliance"
                ]

                for layer in layers:
                    # Test both passed and failed for each layer
                    monitor.log_validation(layer, passed=True, message=f"{layer} pass")
                    monitor.log_validation(layer, passed=False, message=f"{layer} fail")

                # Verify all layers have stats
                for layer in layers:
                    stats = monitor.metrics["layer_stats"][layer]
                    assert stats["passed"] >= 1
                    assert stats["failed"] >= 1

    def test_log_validation_with_all_optional_params(self):
        """Test log_validation with all optional parameters"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor()

                # Call with all parameters to maximize coverage
                monitor.log_validation(
                    layer="layer_5_output_content",
                    passed=False,
                    message="Comprehensive test",
                    severity=7,
                    details={"reason": "test", "score": 0.5},
                    user_id="user_123",
                    session_id="session_456"
                )

                assert monitor.metrics["failed_validations"] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=monitoring", "--cov-report=term-missing"])
