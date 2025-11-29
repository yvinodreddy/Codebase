#!/usr/bin/env python3
"""
Comprehensive tests for verbose_logger.py - targeting 90%+ coverage.
This test suite covers all remaining uncovered methods and edge cases.

Test Coverage Target: Boost verbose_logger.py from 69% to 90%+
Strategy: Test all display methods with various parameter combinations
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from verbose_logger import VerboseLogger


class TestContextStats:
    """Test context_stats method"""

    def test_context_stats_with_compactions(self, capsys):
        """Should display context stats with compaction info"""
        logger = VerboseLogger(enabled=True)

        stats = {
            'total_messages': 150,
            'total_tokens': 180000,
            'usage_percentage': 90.0,
            'compactions_performed': 3,
            'total_tokens_saved': 25000
        }

        logger.context_stats(stats)

        captured = capsys.readouterr()
        assert "Context Management:" in captured.out
        assert "150" in captured.out
        assert "180,000" in captured.out
        assert "90.0%" in captured.out
        assert "Compactions: 3" in captured.out
        assert "25,000" in captured.out

    def test_context_stats_without_compactions(self, capsys):
        """Should display context stats without compaction info"""
        logger = VerboseLogger(enabled=True)

        stats = {
            'total_messages': 50,
            'total_tokens': 10000,
            'usage_percentage': 5.0,
            'compactions_performed': 0
        }

        logger.context_stats(stats)

        captured = capsys.readouterr()
        assert "Context Management:" in captured.out
        assert "50" in captured.out
        assert "10,000" in captured.out
        assert "Compactions" not in captured.out


class TestSeparatorAndSubsection:
    """Test separator and subsection methods"""

    def test_separator(self, capsys):
        """Should display separator line"""
        logger = VerboseLogger(enabled=True)
        logger.separator()

        captured = capsys.readouterr()
        assert "─" in captured.out

    def test_subsection(self, capsys):
        """Should display subsection header"""
        logger = VerboseLogger(enabled=True)
        logger.subsection("Test Section")

        captured = capsys.readouterr()
        assert "Test Section" in captured.out
        assert "-" in captured.out  # Uses regular hyphens, not em-dash


class TestListItems:
    """Test list_items method"""

    def test_list_items_with_indent(self, capsys):
        """Should display indented list"""
        logger = VerboseLogger(enabled=True)
        logger.list_items(["Item 1", "Item 2", "Item 3"], indent=True)

        captured = capsys.readouterr()
        assert "Item 1" in captured.out
        assert "Item 2" in captured.out
        assert "Item 3" in captured.out
        assert "•" in captured.out

    def test_list_items_without_indent(self, capsys):
        """Should display non-indented list"""
        logger = VerboseLogger(enabled=True)
        logger.list_items(["Item A", "Item B"], indent=False)

        captured = capsys.readouterr()
        assert "Item A" in captured.out
        assert "Item B" in captured.out


class TestProcessingStep:
    """Test processing_step with different statuses"""

    def test_processing_step_in_progress(self, capsys):
        """Should display in-progress step"""
        logger = VerboseLogger(enabled=True)
        logger.processing_step("Loading data", status="in progress")

        captured = capsys.readouterr()
        assert "Loading data" in captured.out
        assert "→" in captured.out

    def test_processing_step_done(self, capsys):
        """Should display completed step"""
        logger = VerboseLogger(enabled=True)
        logger.processing_step("Processing complete", status="done")

        captured = capsys.readouterr()
        assert "Processing complete" in captured.out
        assert "✓" in captured.out

    def test_processing_step_failed(self, capsys):
        """Should display failed step"""
        logger = VerboseLogger(enabled=True)
        logger.processing_step("Operation failed", status="failed")

        captured = capsys.readouterr()
        assert "Operation failed" in captured.out
        assert "❌" in captured.out

    def test_processing_step_warning(self, capsys):
        """Should display warning step"""
        logger = VerboseLogger(enabled=True)
        logger.processing_step("Warning detected", status="warning")

        captured = capsys.readouterr()
        assert "Warning detected" in captured.out
        assert "⚠️" in captured.out


class TestIterationInfo:
    """Test iteration_info method"""

    def test_iteration_info(self, capsys):
        """Should display iteration progress"""
        logger = VerboseLogger(enabled=True)
        logger.iteration_info(current=5, total=20, confidence=92.5)

        captured = capsys.readouterr()
        assert "Iteration 5/20" in captured.out
        assert "92.50%" in captured.out


class TestFinalSummary:
    """Test final_summary method"""

    def test_final_summary_success(self, capsys):
        """Should display successful final summary"""
        logger = VerboseLogger(enabled=True)
        logger.final_summary(success=True, confidence=99.5, iterations=8, duration=12.345)

        captured = capsys.readouterr()
        assert "FINAL SUMMARY" in captured.out
        assert "✅ SUCCESS" in captured.out
        assert "99.50%" in captured.out
        assert "8" in captured.out
        assert "12.345s" in captured.out

    def test_final_summary_failed(self, capsys):
        """Should display failed final summary"""
        logger = VerboseLogger(enabled=True)
        logger.final_summary(success=False, confidence=85.0, iterations=20, duration=45.678)

        captured = capsys.readouterr()
        assert "FINAL SUMMARY" in captured.out
        assert "❌ FAILED" in captured.out
        assert "85.00%" in captured.out
        assert "20" in captured.out


class TestPromptInfo:
    """Test prompt_info method"""

    def test_prompt_info(self, capsys):
        """Should display prompt information"""
        logger = VerboseLogger(enabled=True)
        logger.prompt_info(prompt_length=250, target_confidence=99.0)

        captured = capsys.readouterr()
        assert "ULTRATHINK PROCESSING INITIATED" in captured.out
        assert "250" in captured.out
        assert "99.0%" in captured.out
        assert "Claude Code Max" in captured.out


class TestGuardrailLayer:
    """Test guardrail_layer method"""

    def test_guardrail_layer_with_details(self, capsys):
        """Should display guardrail layer with details"""
        logger = VerboseLogger(enabled=True)

        details = {
            "Check 1": "Passed",
            "Check 2": "Passed",
            "Very long detail that needs truncation because it exceeds the maximum allowed length": "Value"
        }

        logger.guardrail_layer(
            layer_num=1,
            layer_name="Test Layer",
            layer_purpose="Testing purpose",
            passed=True,
            details=details
        )

        captured = capsys.readouterr()
        assert "Layer 1: Test Layer" in captured.out
        assert "✅ PASS" in captured.out
        assert "Testing purpose" in captured.out
        assert "Check 1" in captured.out
        assert "..." in captured.out  # Truncation marker

    def test_guardrail_layer_failed(self, capsys):
        """Should display failed guardrail layer"""
        logger = VerboseLogger(enabled=True)

        logger.guardrail_layer(
            layer_num=3,
            layer_name="Validation Layer",
            layer_purpose="Input validation",
            passed=False,
            details=None
        )

        captured = capsys.readouterr()
        assert "Layer 3" in captured.out
        assert "❌ FAIL" in captured.out


class TestAgentComponent:
    """Test agent_component method"""

    def test_agent_component_with_metrics(self, capsys):
        """Should display agent component with metrics"""
        logger = VerboseLogger(enabled=True)

        metrics = {
            "agents_used": 25,
            "confidence": 98.5,
            "duration": "2.5s"
        }

        logger.agent_component(
            component_name="Code Generator",
            purpose="Generate high-quality code",
            status="Active",
            metrics=metrics
        )

        captured = capsys.readouterr()
        assert "Code Generator" in captured.out
        assert "Generate high-quality code" in captured.out
        assert "Active" in captured.out
        assert "agents_used: 25" in captured.out

    def test_agent_component_without_metrics(self, capsys):
        """Should display agent component without metrics"""
        logger = VerboseLogger(enabled=True)

        logger.agent_component(
            component_name="Verifier",
            purpose="Verify output quality",
            status="Idle",
            metrics=None
        )

        captured = capsys.readouterr()
        assert "Verifier" in captured.out
        assert "Idle" in captured.out


class TestIterationDetail:
    """Test iteration_detail method"""

    def test_iteration_detail_first_iteration(self, capsys):
        """Should display first iteration details"""
        logger = VerboseLogger(enabled=True)

        logger.iteration_detail(
            iteration=1,
            max_iterations=20,
            confidence=95.0,
            target=99.0,
            changes_made="Generated initial response",
            reason=""
        )

        captured = capsys.readouterr()
        assert "Iteration 1/20" in captured.out
        assert "95.00%" in captured.out
        assert "99.00%" in captured.out
        assert "4.00%" in captured.out  # Gap
        assert "Initial Response" in captured.out

    def test_iteration_detail_refinement(self, capsys):
        """Should display refinement iteration"""
        logger = VerboseLogger(enabled=True)

        logger.iteration_detail(
            iteration=5,
            max_iterations=20,
            confidence=97.5,
            target=99.0,
            changes_made="Improved accuracy",
            reason="Confidence below target"
        )

        captured = capsys.readouterr()
        assert "Iteration 5/20" in captured.out
        assert "Changes Made: Improved accuracy" in captured.out
        assert "Reason for Refinement: Confidence below target" in captured.out

    def test_iteration_detail_target_achieved(self, capsys):
        """Should display target achieved"""
        logger = VerboseLogger(enabled=True)

        logger.iteration_detail(
            iteration=8,
            max_iterations=20,
            confidence=99.5,
            target=99.0,
            changes_made="Final refinements",
            reason="Polish output"
        )

        captured = capsys.readouterr()
        assert "✅ TARGET ACHIEVED!" in captured.out


class TestContextManagementDetail:
    """Test context_management_detail method"""

    def test_context_management_with_compactions(self, capsys):
        """Should display detailed context management with compactions"""
        logger = VerboseLogger(enabled=True)

        stats = {
            'total_tokens': 180000,
            'usage_percentage': 90.0,
            'total_messages': 150,
            'compactions_performed': 3,
            'total_tokens_saved': 30000
        }

        savings_info = {
            'cache_read_tokens': 50000,
            'cache_creation_tokens': 20000
        }

        logger.context_management_detail(stats, savings_info)

        captured = capsys.readouterr()
        assert "Context Management - Detailed Breakdown" in captured.out
        assert "200,000 tokens" in captured.out
        assert "180,000" in captured.out
        assert "Compactions Performed: 3" in captured.out
        assert "30,000" in captured.out
        assert "Prompt Caching ACTIVE" in captured.out
        assert "50,000" in captured.out
        assert "⚠️  Near threshold" in captured.out

    def test_context_management_without_compactions(self, capsys):
        """Should display context management without compactions"""
        logger = VerboseLogger(enabled=True)

        stats = {
            'total_tokens': 50000,
            'usage_percentage': 25.0,
            'total_messages': 50,
            'compactions_performed': 0
        }

        logger.context_management_detail(stats, None)

        captured = capsys.readouterr()
        assert "Compactions Performed: 0" in captured.out
        assert "✅ Optimal" in captured.out

    def test_context_management_with_cache_creation_only(self, capsys):
        """Should display cache creation without reads"""
        logger = VerboseLogger(enabled=True)

        stats = {
            'total_tokens': 10000,
            'usage_percentage': 5.0,
            'total_messages': 20,
            'compactions_performed': 0
        }

        savings_info = {
            'cache_read_tokens': 0,
            'cache_creation_tokens': 15000
        }

        logger.context_management_detail(stats, savings_info)

        captured = capsys.readouterr()
        assert "15,000" in captured.out
        assert "Future requests will benefit" in captured.out


class TestFrameworkBenefits:
    """Test framework_benefits method"""

    def test_framework_benefits(self, capsys):
        """Should display framework benefits"""
        logger = VerboseLogger(enabled=True)
        logger.framework_benefits()

        captured = capsys.readouterr()
        # This method likely has content, let's just verify it runs
        assert captured.out != ""


class TestAnswerSectionMarkers:
    """Test answer_section_start and answer_section_end methods"""

    def test_answer_section_start(self, capsys):
        """Should display answer section start marker"""
        logger = VerboseLogger(enabled=True)
        logger.answer_section_start()

        captured = capsys.readouterr()
        assert "🔥" in captured.out
        assert "THE ACTUAL ANSWER STARTS HERE" in captured.out
        assert "⬇️" in captured.out
        assert "system processing" in captured.out

    def test_answer_section_end(self, capsys):
        """Should display answer section end marker"""
        logger = VerboseLogger(enabled=True)
        logger.answer_section_end()

        captured = capsys.readouterr()
        assert "🔥" in captured.out
        assert "THE ACTUAL ANSWER ENDS HERE" in captured.out
        assert "⬆️" in captured.out

    def test_answer_section_disabled(self, capsys):
        """Should not display answer markers when disabled"""
        logger = VerboseLogger(enabled=False)
        logger.answer_section_start()
        logger.answer_section_end()

        captured = capsys.readouterr()
        assert captured.out == ""


class TestDisabledMode:
    """Test all methods in disabled mode"""

    def test_disabled_mode_produces_no_output(self, capsys):
        """All methods should produce no output when disabled"""
        logger = VerboseLogger(enabled=False)

        # Call all methods
        logger.context_stats({'total_messages': 100, 'total_tokens': 1000, 'usage_percentage': 0.5})
        logger.separator()
        logger.subsection("Test")
        logger.list_items(["item1", "item2"])
        logger.processing_step("step", "done")
        logger.iteration_info(1, 10, 50.0)
        logger.final_summary(True, 99.0, 5, 10.0)
        logger.prompt_info(100, 99.0)
        logger.guardrail_layer(1, "test", "purpose", True, {})
        logger.agent_component("comp", "purpose", "active", {})
        logger.iteration_detail(1, 10, 95.0, 99.0, "changes", "reason")
        logger.context_management_detail({}, {})
        logger.framework_benefits()

        captured = capsys.readouterr()
        assert captured.out == ""


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
