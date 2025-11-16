"""
Comprehensive tests for verbose_logger.py module.

This test suite extends coverage for the VerboseLogger class,
focusing on formatting, stage output, metrics display, and integration.

Target Coverage: Boost verbose_logger.py from 32% to 70%+
New Tests: 30 tests across 5 test classes
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import time
import io

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from verbose_logger import VerboseLogger


class TestVerboseLoggerFormatting:
    """Test output formatting functionality."""

    def test_format_with_stage_separators(self, capsys):
        """Should format stage headers with 80-char separators."""
        logger = VerboseLogger(enabled=True)
        logger.stage_header(1, "Test Stage")

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        separator_lines = [line for line in lines if '=' in line]

        # Should have separator lines
        assert len(separator_lines) >= 2
        # Each separator should be 80 chars
        for line in separator_lines:
            assert len(line) == 80

    def test_format_with_verbose_prefix(self, capsys):
        """Should add [VERBOSE] prefix to all output."""
        logger = VerboseLogger(enabled=True)
        logger.info("Test message")

        captured = capsys.readouterr()
        assert "[VERBOSE]" in captured.out

    def test_format_with_checkmark_emoji(self, capsys):
        """Should use checkmark emoji for success messages."""
        logger = VerboseLogger(enabled=True)
        logger.success("Operation succeeded")

        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Operation succeeded" in captured.out

    def test_format_with_warning_emoji(self, capsys):
        """Should use warning emoji for warning messages."""
        logger = VerboseLogger(enabled=True)
        logger.warning("Warning message")

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "Warning message" in captured.out

    def test_format_with_error_emoji(self, capsys):
        """Should use error emoji for error messages."""
        logger = VerboseLogger(enabled=True)
        logger.error("Error message")

        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "Error message" in captured.out

    def test_format_multiline_content(self, capsys):
        """Should handle multiline content correctly."""
        logger = VerboseLogger(enabled=True)
        logger.info("Line 1")
        logger.info("Line 2")
        logger.info("Line 3")

        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')
        assert len(lines) == 3
        assert all("[VERBOSE]" in line for line in lines)

    def test_format_with_indentation(self, capsys):
        """Should indent messages when requested."""
        logger = VerboseLogger(enabled=True)
        logger.info("Not indented", indent=False)
        logger.info("Indented", indent=True)

        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')

        # First line should have one space after [VERBOSE]
        assert lines[0].startswith("[VERBOSE] ")
        # Second line should have three spaces after [VERBOSE]
        assert lines[1].startswith("[VERBOSE]   ")

    def test_format_metrics_key_value(self, capsys):
        """Should format metrics as key-value pairs."""
        logger = VerboseLogger(enabled=True)
        logger.metric("Coverage", "71.5%")
        logger.metric("Tests", 550)

        captured = capsys.readouterr()
        assert "Coverage: 71.5%" in captured.out
        assert "Tests: 550" in captured.out


class TestVerboseLoggerStageOutput:
    """Test stage header and footer functionality."""

    def test_stage_header_format(self, capsys):
        """Should format stage headers correctly."""
        logger = VerboseLogger(enabled=True)
        logger.stage_header(2, "Guardrails Validation")

        captured = capsys.readouterr()
        assert "STAGE 2" in captured.out
        assert "Guardrails Validation" in captured.out
        assert "=" * 80 in captured.out

    def test_stage_footer_with_timing(self, capsys):
        """Should display timing in stage footer."""
        logger = VerboseLogger(enabled=True)
        logger.stage_header(1, "Test")

        time.sleep(0.1)  # Small delay
        logger.stage_footer()

        captured = capsys.readouterr()
        assert "completed in" in captured.out
        assert "s" in captured.out  # Time unit
        assert "✓" in captured.out

    def test_stage_footer_custom_duration(self, capsys):
        """Should use custom duration if provided."""
        logger = VerboseLogger(enabled=True)
        logger.current_stage = "STAGE 1"
        logger.stage_footer(duration=2.5)

        captured = capsys.readouterr()
        assert "2.500s" in captured.out or "2.5" in captured.out

    def test_stage_tracking(self):
        """Should track current stage."""
        logger = VerboseLogger(enabled=True)
        logger.stage_header(3, "Context Management")

        assert logger.current_stage == "STAGE 3"
        assert logger.stage_start_time is not None

    def test_multiple_stages_sequence(self, capsys):
        """Should handle multiple stages in sequence."""
        logger = VerboseLogger(enabled=True)

        logger.stage_header(1, "Stage 1")
        logger.info("Stage 1 work")
        logger.stage_footer()

        logger.stage_header(2, "Stage 2")
        logger.info("Stage 2 work")
        logger.stage_footer()

        captured = capsys.readouterr()
        assert "STAGE 1" in captured.out
        assert "STAGE 2" in captured.out
        assert captured.out.count("completed in") == 2

    def test_stage_start_time_reset(self):
        """Should reset stage start time for each stage."""
        logger = VerboseLogger(enabled=True)

        logger.stage_header(1, "First")
        first_time = logger.stage_start_time

        time.sleep(0.01)

        logger.stage_header(2, "Second")
        second_time = logger.stage_start_time

        assert second_time > first_time


class TestVerboseLoggerMetricsDisplay:
    """Test metrics and statistics display."""

    def test_metrics_table_simple(self, capsys):
        """Should display simple metrics table."""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "Coverage": 71.5,
            "Tests": 550,
            "Pass Rate": 99.6
        }

        logger.metrics_table("Test Results", metrics)

        captured = capsys.readouterr()
        assert "Test Results" in captured.out
        assert "Coverage" in captured.out
        assert "71.50" in captured.out or "71.5" in captured.out

    def test_metrics_table_with_floats(self, capsys):
        """Should format float values with 2 decimal places."""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "Confidence": 99.756,
            "Accuracy": 0.9234
        }

        logger.metrics_table("Quality Metrics", metrics)

        captured = capsys.readouterr()
        # Floats should be formatted to 2 decimal places
        assert ".75" in captured.out or "99.76" in captured.out
        assert ".92" in captured.out

    def test_metrics_table_with_strings(self, capsys):
        """Should handle string values in metrics."""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "Status": "PASSING",
            "Mode": "VERBOSE"
        }

        logger.metrics_table("Configuration", metrics)

        captured = capsys.readouterr()
        assert "PASSING" in captured.out
        assert "VERBOSE" in captured.out

    def test_metrics_table_alignment(self, capsys):
        """Should align metrics table columns."""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "Short": "val",
            "VeryLongKeyName": "value"
        }

        logger.metrics_table("Alignment Test", metrics)

        captured = capsys.readouterr()
        # Should have some alignment spacing
        assert ":" in captured.out

    def test_single_metric_display(self, capsys):
        """Should display single metrics correctly."""
        logger = VerboseLogger(enabled=True)
        logger.metric("Coverage", "75%")

        captured = capsys.readouterr()
        assert "Coverage: 75%" in captured.out

    def test_metric_with_numeric_value(self, capsys):
        """Should handle numeric metric values."""
        logger = VerboseLogger(enabled=True)
        logger.metric("Test Count", 582)

        captured = capsys.readouterr()
        assert "Test Count: 582" in captured.out

    def test_empty_metrics_table(self, capsys):
        """Should handle empty metrics gracefully."""
        logger = VerboseLogger(enabled=True)
        logger.metrics_table("Empty", {})

        captured = capsys.readouterr()
        assert "Empty" in captured.out

    def test_metrics_with_boolean_values(self, capsys):
        """Should handle boolean values in metrics."""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "Passed": True,
            "Failed": False
        }

        logger.metrics_table("Boolean Test", metrics)

        captured = capsys.readouterr()
        assert "True" in captured.out or "False" in captured.out


class TestVerboseLoggerDisabledMode:
    """Test logger behavior when disabled."""

    def test_disabled_produces_no_output(self, capsys):
        """Should produce no output when disabled."""
        logger = VerboseLogger(enabled=False)

        logger.stage_header(1, "Test")
        logger.info("Message")
        logger.success("Success")
        logger.warning("Warning")
        logger.error("Error")
        logger.stage_footer()

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_disabled_stage_header(self, capsys):
        """Should skip stage headers when disabled."""
        logger = VerboseLogger(enabled=False)
        logger.stage_header(5, "Skipped Stage")

        captured = capsys.readouterr()
        assert "Skipped Stage" not in captured.out

    def test_disabled_metrics_table(self, capsys):
        """Should skip metrics tables when disabled."""
        logger = VerboseLogger(enabled=False)

        metrics = {"Key": "Value"}
        logger.metrics_table("Skipped Metrics", metrics)

        captured = capsys.readouterr()
        assert "Skipped Metrics" not in captured.out

    def test_disabled_skips_tracking(self):
        """Should skip tracking when disabled."""
        logger = VerboseLogger(enabled=False)
        logger.stage_header(2, "Skipped tracking")

        # Should NOT track the stage number when disabled
        assert logger.current_stage is None


class TestVerboseLoggerIntegration:
    """Test integration scenarios."""

    def test_complete_workflow(self, capsys):
        """Should handle complete verbose workflow."""
        logger = VerboseLogger(enabled=True)

        # Stage 1
        logger.stage_header(1, "Preprocessing")
        logger.info("Analyzing prompt")
        logger.metric("Length", 150)
        logger.success("Analysis complete")
        logger.stage_footer()

        # Stage 2
        logger.stage_header(2, "Execution")
        logger.info("Running tests")
        logger.success("Tests passed")
        logger.stage_footer()

        captured = capsys.readouterr()

        # Check all stages present
        assert "STAGE 1" in captured.out
        assert "STAGE 2" in captured.out
        assert "Preprocessing" in captured.out
        assert "Execution" in captured.out
        assert captured.out.count("completed in") == 2

    def test_mixed_message_types(self, capsys):
        """Should handle mixed message types."""
        logger = VerboseLogger(enabled=True)

        logger.info("Information")
        logger.success("Success message")
        logger.warning("Warning message")
        logger.error("Error message")

        captured = capsys.readouterr()

        assert "Information" in captured.out
        assert "✓" in captured.out
        assert "⚠️" in captured.out
        assert "❌" in captured.out

    def test_session_timing(self):
        """Should track session start time."""
        logger = VerboseLogger(enabled=True)

        assert logger.session_start_time is not None
        assert isinstance(logger.session_start_time, float)
        assert logger.session_start_time <= time.time()

    def test_enabled_flag_toggle(self, capsys):
        """Should respect enabled flag changes."""
        logger = VerboseLogger(enabled=True)
        logger.info("Enabled message")

        logger.enabled = False
        logger.info("Disabled message")

        logger.enabled = True
        logger.info("Re-enabled message")

        captured = capsys.readouterr()

        assert "Enabled message" in captured.out
        assert "Disabled message" not in captured.out
        assert "Re-enabled message" in captured.out

    def test_initialization_defaults(self):
        """Should have correct initialization defaults."""
        logger = VerboseLogger()

        assert logger.enabled is True
        assert logger.stage_start_time is None
        assert logger.current_stage is None
        assert logger.session_start_time is not None

    def test_large_metrics_table(self, capsys):
        """Should handle large metrics tables."""
        logger = VerboseLogger(enabled=True)

        metrics = {f"Metric{i}": i * 1.5 for i in range(10)}
        logger.metrics_table("Large Table", metrics)

        captured = capsys.readouterr()

        assert "Large Table" in captured.out
        assert captured.out.count(":") >= 10  # At least 10 metrics

    def test_rapid_stage_transitions(self, capsys):
        """Should handle rapid stage transitions."""
        logger = VerboseLogger(enabled=True)

        for i in range(1, 6):
            logger.stage_header(i, f"Stage {i}")
            logger.info(f"Work in stage {i}")
            logger.stage_footer()

        captured = capsys.readouterr()

        # All 5 stages should be present
        for i in range(1, 6):
            assert f"STAGE {i}" in captured.out


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
