#!/usr/bin/env python3
"""
Unit Tests for guardrails/monitoring.py
Tests guardrail monitoring and logging system.

Test Coverage Target: 80%+
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from guardrails.monitoring import GuardrailEvent, GuardrailMonitor


# ==========================================
# GUARDRAIL EVENT TESTS
# ==========================================

class TestGuardrailEvent:
    """Test GuardrailEvent dataclass."""

    def test_event_creation(self):
        """GuardrailEvent should be created with all fields."""
        event = GuardrailEvent(
            timestamp="2025-01-01T12:00:00",
            event_type="validation_success",
            layer="layer_1",
            passed=True,
            message="Test message"
        )
        assert event.timestamp == "2025-01-01T12:00:00"
        assert event.event_type == "validation_success"
        assert event.layer == "layer_1"
        assert event.passed is True
        assert event.message == "Test message"

    def test_event_optional_fields(self):
        """GuardrailEvent optional fields should default to None."""
        event = GuardrailEvent(
            timestamp="2025-01-01T12:00:00",
            event_type="validation_success",
            layer="layer_1",
            passed=True,
            message="Test"
        )
        assert event.severity is None
        assert event.details is None
        assert event.user_id is None
        assert event.session_id is None

    def test_event_with_all_fields(self):
        """GuardrailEvent should accept all optional fields."""
        event = GuardrailEvent(
            timestamp="2025-01-01T12:00:00",
            event_type="validation_failure",
            layer="layer_2",
            passed=False,
            message="Validation failed",
            severity=7,
            details={"reason": "content unsafe"},
            user_id="user123",
            session_id="session456"
        )
        assert event.severity == 7
        assert event.details == {"reason": "content unsafe"}
        assert event.user_id == "user123"
        assert event.session_id == "session456"


# ==========================================
# GUARDRAIL MONITOR INITIALIZATION TESTS
# ==========================================

class TestGuardrailMonitorInit:
    """Test GuardrailMonitor initialization."""

    def test_init_creates_monitor(self):
        """GuardrailMonitor should initialize successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))
            assert monitor is not None

    def test_init_loads_default_metrics(self):
        """GuardrailMonitor should load default metrics if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "new_metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            assert monitor.metrics["total_validations"] == 0
            assert monitor.metrics["successful_validations"] == 0
            assert monitor.metrics["failed_validations"] == 0
            assert "layer_stats" in monitor.metrics

    def test_init_with_existing_metrics(self):
        """GuardrailMonitor should load existing metrics from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "existing_metrics.json"

            # Create existing metrics
            existing_data = {
                "total_validations": 100,
                "successful_validations": 80,
                "failed_validations": 20
            }
            with open(metrics_file, 'w') as f:
                json.dump(existing_data, f)

            monitor = GuardrailMonitor(metrics_file=str(metrics_file))
            assert monitor.metrics["total_validations"] == 100
            assert monitor.metrics["successful_validations"] == 80


# ==========================================
# LOG VALIDATION TESTS
# ==========================================

class TestLogValidation:
    """Test log_validation method."""

    def test_log_validation_success(self):
        """log_validation should record successful validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_1_prompt_shields",
                passed=True,
                message="Validation passed"
            )

            assert monitor.metrics["total_validations"] == 1
            assert monitor.metrics["successful_validations"] == 1
            assert monitor.metrics["failed_validations"] == 0

    def test_log_validation_failure(self):
        """log_validation should record failed validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_2_input_content",
                passed=False,
                message="Validation failed"
            )

            assert monitor.metrics["total_validations"] == 1
            assert monitor.metrics["successful_validations"] == 0
            assert monitor.metrics["failed_validations"] == 1

    def test_log_validation_updates_layer_stats(self):
        """log_validation should update layer-specific stats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_1_prompt_shields",
                passed=True,
                message="Test"
            )

            layer_stats = monitor.metrics["layer_stats"]["layer_1_prompt_shields"]
            assert layer_stats["passed"] == 1
            assert layer_stats["failed"] == 0

    def test_log_validation_with_severity(self):
        """log_validation should accept severity parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_3_phi_detection",
                passed=False,
                message="High severity issue",
                severity=9
            )

            assert monitor.metrics["total_validations"] == 1

    def test_log_validation_with_details(self):
        """log_validation should accept details parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_4_terminology",
                passed=True,
                message="Validation passed",
                details={"reason": "all checks passed"}
            )

            assert monitor.metrics["total_validations"] == 1

    def test_log_validation_with_user_session(self):
        """log_validation should accept user_id and session_id."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_validation(
                layer="layer_5_output_content",
                passed=True,
                message="Test",
                user_id="user123",
                session_id="session456"
            )

            assert monitor.metrics["total_validations"] == 1


# ==========================================
# LOG WARNING/ERROR TESTS
# ==========================================

class TestLogWarningError:
    """Test log_warning and log_error methods."""

    def test_log_warning_increments_counter(self):
        """log_warning should increment warnings counter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_warning("layer_1", "Warning message")

            assert monitor.metrics["warnings"] == 1

    def test_log_error_increments_counter(self):
        """log_error should increment errors counter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_error("layer_2", "Error message")

            assert monitor.metrics["errors"] == 1

    def test_multiple_warnings_errors(self):
        """Multiple warnings and errors should be counted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            monitor.log_warning("layer_1", "Warning 1")
            monitor.log_warning("layer_2", "Warning 2")
            monitor.log_error("layer_3", "Error 1")

            assert monitor.metrics["warnings"] == 2
            assert monitor.metrics["errors"] == 1


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    def test_get_statistics_initial(self):
        """get_statistics should return initial stats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            stats = monitor.get_statistics()

            assert stats["total_validations"] == 0
            assert stats["successful_validations"] == 0
            assert stats["failed_validations"] == 0
            assert stats["success_rate"] == 0.0

    def test_get_statistics_after_validations(self):
        """get_statistics should calculate success rate correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            # Log some validations
            for _ in range(8):
                monitor.log_validation("layer_1_prompt_shields", True, "Pass")
            for _ in range(2):
                monitor.log_validation("layer_2_input_content", False, "Fail")

            stats = monitor.get_statistics()

            assert stats["total_validations"] == 10
            assert stats["successful_validations"] == 8
            assert stats["failed_validations"] == 2
            assert stats["success_rate"] == 80.0


# ==========================================
# GET LAYER PERFORMANCE TESTS
# ==========================================

class TestGetLayerPerformance:
    """Test get_layer_performance method."""

    def test_get_layer_performance_initial(self):
        """get_layer_performance should return initial stats for layer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            perf = monitor.get_layer_performance("layer_1_prompt_shields")

            assert perf["passed"] == 0
            assert perf["failed"] == 0
            assert perf["total_validations"] == 0
            assert perf["pass_rate"] == 0.0

    def test_get_layer_performance_after_validations(self):
        """get_layer_performance should calculate layer success rate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            # Log validations for specific layer
            for _ in range(7):
                monitor.log_validation("layer_1_prompt_shields", True, "Pass")
            for _ in range(3):
                monitor.log_validation("layer_1_prompt_shields", False, "Fail")

            perf = monitor.get_layer_performance("layer_1_prompt_shields")

            assert perf["passed"] == 7
            assert perf["failed"] == 3
            assert perf["total_validations"] == 10
            assert perf["pass_rate"] == 70.0

    def test_get_layer_performance_unknown_layer(self):
        """get_layer_performance should handle unknown layer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            perf = monitor.get_layer_performance("unknown_layer")

            # Should return error for unknown layer
            assert "error" in perf


# ==========================================
# RESET METRICS TESTS
# ==========================================

class TestResetMetrics:
    """Test reset_metrics method."""

    def test_reset_clears_metrics(self):
        """reset_metrics should clear all metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            # Add some data
            monitor.log_validation("layer_1_prompt_shields", True, "Test")
            monitor.log_warning("layer_2", "Warning")
            monitor.log_error("layer_3", "Error")

            # Reset
            monitor.reset_metrics()

            assert monitor.metrics["total_validations"] == 0
            assert monitor.metrics["successful_validations"] == 0
            assert monitor.metrics["failed_validations"] == 0
            assert monitor.metrics["warnings"] == 0
            assert monitor.metrics["errors"] == 0


# ==========================================
# GENERATE REPORT TESTS
# ==========================================

class TestGenerateReport:
    """Test generate_report method."""

    def test_generate_report_returns_string(self):
        """generate_report should return a string report."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            report = monitor.generate_report()

            assert isinstance(report, str)
            assert len(report) > 0

    def test_generate_report_contains_metrics(self):
        """generate_report should contain key metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            # Add some data
            monitor.log_validation("layer_1_prompt_shields", True, "Test")

            report = monitor.generate_report()

            assert "total" in report.lower() or "validation" in report.lower()

    def test_generate_report_to_file(self):
        """generate_report should save to file when output_file provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            output_file = Path(tmpdir) / "report.txt"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            report = monitor.generate_report(output_file=str(output_file))

            assert output_file.exists()


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestGuardrailMonitorIntegration:
    """Test real-world monitoring scenarios."""

    def test_full_validation_workflow(self):
        """Test complete validation workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"
            monitor = GuardrailMonitor(metrics_file=str(metrics_file))

            # Simulate multiple layers of validation
            monitor.log_validation("layer_1_prompt_shields", True, "Layer 1 passed")
            monitor.log_validation("layer_2_input_content", True, "Layer 2 passed")
            monitor.log_validation("layer_3_phi_detection", False, "PHI detected")
            monitor.log_warning("layer_3_phi_detection", "Sensitive data warning")

            stats = monitor.get_statistics()
            assert stats["total_validations"] == 3
            assert stats["successful_validations"] == 2
            assert stats["failed_validations"] == 1
            assert monitor.metrics["warnings"] == 1

    def test_metrics_persistence(self):
        """Test that metrics persist across monitor instances."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.json"

            # Create first monitor and log data
            monitor1 = GuardrailMonitor(metrics_file=str(metrics_file))
            monitor1.log_validation("layer_1_prompt_shields", True, "Test")
            monitor1._save_metrics()

            # Create second monitor and verify data loaded
            monitor2 = GuardrailMonitor(metrics_file=str(metrics_file))
            assert monitor2.metrics["total_validations"] == 1


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
