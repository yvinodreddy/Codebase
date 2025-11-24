#!/usr/bin/env python3
"""
TARGETED TESTS for monitoring.py - 90%+ Coverage
Targets missing lines to push from 66.67% to 90%+
"""

import pytest
import sys
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "guardrails"))

try:
    from monitoring import GuardrailMonitor, GuardrailEvent, get_monitor
except ImportError as e:
    pytest.skip(f"Cannot import monitoring: {e}", allow_module_level=True)


class TestMonitoring90Percent:
    """Tests targeting lines 168-183, 192-207, 211-217, 247-258, 270-318, 328-330"""

    # ============================================
    # LINES 168-183: log_warning() method
    # ============================================

    def test_lines_168_183_log_warning(self):
        """Lines 168-183: log_warning creates event and updates metrics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Call log_warning to trigger lines 168-183
                monitor.log_warning(
                    layer="layer_1_prompt_shields",
                    message="Potential jailbreak pattern detected",
                    details={"pattern": "ignore previous instructions"}
                )

                # Lines 168-183 should execute:
                # 168: event = GuardrailEvent(...)
                # 177: logger.warning(...)
                # 182: self.metrics["warnings"] += 1
                # 183: self._save_metrics()

                assert monitor.metrics["warnings"] == 1

    def test_lines_168_183_log_warning_with_different_layer(self):
        """Lines 168-183: log_warning with different layer"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Log multiple warnings to different layers
                monitor.log_warning("layer_2_input_content", "Low confidence detection")
                monitor.log_warning("layer_3_phi_detection", "Possible PHI pattern")
                monitor.log_warning("layer_4_terminology", "Non-standard term used")

                # Should have 3 warnings total
                assert monitor.metrics["warnings"] == 3

    # ============================================
    # LINES 192-207: log_error() method
    # ============================================

    def test_lines_192_207_log_error(self):
        """Lines 192-207: log_error creates event and updates metrics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Call log_error to trigger lines 192-207
                monitor.log_error(
                    layer="layer_5_output_content",
                    error="API connection failed",
                    details={"error_code": "CONNECTION_TIMEOUT"}
                )

                # Lines 192-207 should execute:
                # 192: event = GuardrailEvent(...)
                # 201: logger.error(...)
                # 206: self.metrics["errors"] += 1
                # 207: self._save_metrics()

                assert monitor.metrics["errors"] == 1

    def test_lines_192_207_log_error_multiple(self):
        """Lines 192-207: log_error with multiple errors"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Log multiple errors
                monitor.log_error("layer_6_groundedness", "Groundedness check failed")
                monitor.log_error("layer_7_compliance", "HIPAA violation detected")

                # Should have 2 errors total
                assert monitor.metrics["errors"] == 2

    # ============================================
    # LINES 211-217: get_statistics() with data
    # ============================================

    def test_lines_211_217_get_statistics_with_validations(self):
        """Lines 211-217: get_statistics calculates success_rate when total > 0"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Add some validations to trigger calculation
                monitor.log_validation("layer_1_prompt_shields", passed=True, message="Passed")
                monitor.log_validation("layer_1_prompt_shields", passed=True, message="Passed")
                monitor.log_validation("layer_1_prompt_shields", passed=False, message="Failed")

                # Call get_statistics to trigger lines 211-217
                stats = monitor.get_statistics()

                # Lines 211-217 should execute:
                # 211: total = self.metrics["total_validations"]
                # 212-215: success_rate calculation with total > 0
                # 217: return {...}

                assert stats["total_validations"] == 3
                assert stats["successful_validations"] == 2
                assert stats["failed_validations"] == 1
                # 2/3 * 100 = 66.67%
                assert stats["success_rate"] == 66.67

    # ============================================
    # LINES 247-258: reset_metrics() method
    # ============================================

    def test_lines_247_258_reset_metrics(self):
        """Lines 247-258: reset_metrics clears all statistics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Add some data first
                monitor.log_validation("layer_1_prompt_shields", passed=True, message="Test")
                monitor.log_validation("layer_2_input_content", passed=False, message="Test")
                monitor.log_warning("layer_3_phi_detection", "Warning")
                monitor.log_error("layer_4_terminology", "Error")

                # Verify data exists
                assert monitor.metrics["total_validations"] > 0
                assert monitor.metrics["warnings"] > 0
                assert monitor.metrics["errors"] > 0

                # Call reset_metrics to trigger lines 247-258
                monitor.reset_metrics()

                # Lines 247-258 should execute and reset everything
                assert monitor.metrics["total_validations"] == 0
                assert monitor.metrics["successful_validations"] == 0
                assert monitor.metrics["failed_validations"] == 0
                assert monitor.metrics["warnings"] == 0
                assert monitor.metrics["errors"] == 0

                # All layer stats should be reset
                for layer_stats in monitor.metrics["layer_stats"].values():
                    assert layer_stats["passed"] == 0
                    assert layer_stats["failed"] == 0

    # ============================================
    # LINES 270-318: generate_report() method
    # ============================================

    def test_lines_270_318_generate_report_no_file(self):
        """Lines 270-318: generate_report creates report string"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Add some data for the report
                monitor.log_validation("layer_1_prompt_shields", passed=True, message="OK")
                monitor.log_validation("layer_2_input_content", passed=True, message="OK")
                monitor.log_warning("layer_3_phi_detection", "Minor warning")

                # Call generate_report WITHOUT output_file (lines 270-318, excluding 312-316)
                report = monitor.generate_report()

                # Lines 270-318 should execute
                assert isinstance(report, str)
                assert "GUARDRAIL SYSTEM PERFORMANCE REPORT" in report
                assert "OVERALL STATISTICS" in report
                assert "LAYER PERFORMANCE" in report
                assert "Total Validations: 2" in report

    def test_lines_270_318_generate_report_with_file(self):
        """Lines 270-318: generate_report saves to file (hits lines 312-316)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "test_metrics.json"

            with patch('monitoring.LOG_DIR', Path(tmpdir)):
                monitor = GuardrailMonitor(metrics_file=metrics_file.name)

                # Add some data
                monitor.log_validation("layer_1_prompt_shields", passed=True, message="OK")
                monitor.log_validation("layer_1_prompt_shields", passed=False, message="Failed")

                # Call generate_report WITH output_file to trigger lines 312-316
                report_filename = "test_report.txt"
                report = monitor.generate_report(output_file=report_filename)

                # Lines 312-316 should execute (file save path)
                report_path = Path(tmpdir) / report_filename
                assert report_path.exists()

                # Verify file contents
                with open(report_path, 'r') as f:
                    file_content = f.read()
                assert file_content == report
                assert "GUARDRAIL SYSTEM PERFORMANCE REPORT" in file_content

    # ============================================
    # LINES 328-330: get_monitor() initialization
    # ============================================

    def test_lines_328_330_get_monitor_initialization(self):
        """Lines 328-330: get_monitor creates new instance if None"""
        import monitoring

        # Reset global monitor to None
        monitoring._monitor = None

        # Call get_monitor to trigger lines 328-330
        monitor1 = get_monitor()

        # Lines 328-330 should execute:
        # 328: if _monitor is None:
        # 329:     _monitor = GuardrailMonitor()
        # 330: return _monitor

        assert monitor1 is not None
        # Check attributes instead of isinstance (module import differences)
        assert hasattr(monitor1, 'metrics')
        assert hasattr(monitor1, 'log_validation')

        # Second call should return same instance
        monitor2 = get_monitor()
        assert monitor2 is monitor1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=guardrails/monitoring", "--cov-report=term-missing"])
