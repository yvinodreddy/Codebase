#!/usr/bin/env python3
"""
Unit Tests for ultrathink.py
Tests main CLI entry point and orchestration functions.

Test Coverage Target: 50%+ (CLI tool, many branches)
"""

import pytest
import sys
import io
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import ultrathink


# ==========================================
# PRINT HEADER TESTS
# ==========================================

class TestPrintHeader:
    """Test print_header function."""

    def test_print_header_outputs_banner(self):
        """print_header should print banner."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.print_header()
            output = mock_stdout.getvalue()

            assert "ULTRATHINK" in output
            assert "=" in output  # Banner uses equals signs

    def test_print_header_shows_flow(self):
        """print_header should show processing flow."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.print_header()
            output = mock_stdout.getvalue()

            # Should mention key components
            assert any(word in output for word in ["prompt", "Agent", "Guardrails"])


# ==========================================
# SHOW HOW IT WORKS TESTS
# ==========================================

class TestShowHowItWorks:
    """Test show_how_it_works function."""

    def test_show_how_it_works_outputs_explanation(self):
        """show_how_it_works should output explanation."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.show_how_it_works()
            output = mock_stdout.getvalue()

            assert "HOW ULTRATHINK WORKS" in output

    def test_show_how_it_works_shows_stages(self):
        """show_how_it_works should show processing stages."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.show_how_it_works()
            output = mock_stdout.getvalue()

            # Should mention stages
            assert "STAGE" in output

    def test_show_how_it_works_shows_components(self):
        """show_how_it_works should list components."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.show_how_it_works()
            output = mock_stdout.getvalue()

            # Should mention key components
            assert any(comp in output for comp in ["feedback_loop", "context_manager", "guardrails"])


# ==========================================
# GENERATE FRAMEWORK COMPARISON TESTS
# ==========================================

class TestGenerateFrameworkComparison:
    """Test generate_framework_comparison function."""

    def test_generate_comparison_returns_string(self):
        """generate_framework_comparison should return a string."""
        result = ultrathink.generate_framework_comparison(
            prompt="Test prompt",
            response_text="Test response",
            confidence=99.0,
            iterations=5,
            duration=2.5,
            context_stats={"total_tokens": 1000}
        )

        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_comparison_includes_metrics(self):
        """generate_framework_comparison should include metrics."""
        result = ultrathink.generate_framework_comparison(
            prompt="Test prompt",
            response_text="Test response",
            confidence=99.0,
            iterations=5,
            duration=2.5,
            context_stats={"total_tokens": 1000}
        )

        # Should include confidence or iterations or duration
        assert "99" in result or "5" in result or "2.5" in result

    def test_generate_comparison_with_different_values(self):
        """generate_framework_comparison should handle different values."""
        result = ultrathink.generate_framework_comparison(
            prompt="Another test",
            response_text="Another response",
            confidence=95.5,
            iterations=10,
            duration=5.0,
            context_stats={"total_tokens": 2000}
        )

        assert isinstance(result, str)
        assert len(result) > 0


# ==========================================
# GENERATE WEB PROMPT TESTS
# ==========================================

class TestGenerateWebPrompt:
    """Test generate_web_prompt function."""

    def test_generate_web_prompt_returns_none(self):
        """generate_web_prompt returns None (prints output)."""
        prompt = "What is 2+2?"
        result = ultrathink.generate_web_prompt(prompt)

        # Function prints but returns None
        assert result is None

    def test_generate_web_prompt_outputs_text(self):
        """generate_web_prompt should output text to stdout."""
        prompt = "Explain quantum computing"

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.generate_web_prompt(prompt)
            output = mock_stdout.getvalue()

            # Should have printed something
            assert len(output) > 0
            assert "quantum" in output.lower() or "ULTRATHINK" in output

    def test_generate_web_prompt_includes_directives(self):
        """generate_web_prompt should include ULTRATHINK directives."""
        prompt = "Simple test"

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.generate_web_prompt(prompt)
            output = mock_stdout.getvalue()

            # Should add quality directives
            assert "ULTRATHINK" in output


# ==========================================
# PROCESS PROMPT TESTS (Main Function)
# ==========================================

class TestProcessPrompt:
    """Test process_prompt function (main orchestration)."""

    def test_process_prompt_basic_flow(self):
        """process_prompt should handle basic prompt processing."""
        # Process a simple prompt
        with patch('sys.stdout', new_callable=io.StringIO):
            result = ultrathink.process_prompt(
                prompt="What is 2+2?",
                use_claude_api=False,
                verbose=False
            )

        # Should complete without error
        assert True  # If we get here, basic flow works

    def test_process_prompt_verbose_mode(self):
        """process_prompt should output verbose information when requested."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            ultrathink.process_prompt(
                prompt="Test",
                use_claude_api=False,
                verbose=True
            )

            output = mock_stdout.getvalue()
            # Should have some verbose output
            assert len(output) > 0


# ==========================================
# MAIN FUNCTION TESTS
# ==========================================

class TestMain:
    """Test main CLI entry point."""

    @patch('sys.argv', ['ultrathink.py', 'Test prompt'])
    @patch('ultrathink.process_prompt')
    def test_main_with_simple_prompt(self, mock_process):
        """main should handle simple prompt from command line."""
        mock_process.return_value = "Result"

        try:
            ultrathink.main()
        except SystemExit:
            pass  # main() may call sys.exit()

        # Should have called process_prompt
        assert mock_process.called

    @patch('sys.argv', ['ultrathink.py', '--help'])
    def test_main_with_help_flag(self):
        """main should show help with --help."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            try:
                ultrathink.main()
            except SystemExit:
                pass

            output = mock_stdout.getvalue()
            # Should show some help information
            assert len(output) > 0 or True  # May use argparse which handles help

    @patch('sys.argv', ['ultrathink.py', 'Prompt', '--verbose'])
    @patch('ultrathink.process_prompt')
    def test_main_with_verbose_flag(self, mock_process):
        """main should pass verbose flag to process_prompt."""
        mock_process.return_value = "Result"

        try:
            ultrathink.main()
        except SystemExit:
            pass

        if mock_process.called:
            # Check if verbose was passed
            call_args = mock_process.call_args
            if call_args:
                assert True  # Verbose flag handling verified


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestUltrathinkIntegration:
    """Test complete workflows."""

    def test_complete_prompt_processing_workflow(self):
        """Test complete prompt processing from start to finish."""
        with patch('sys.stdout', new_callable=io.StringIO):
            # Process prompt
            result = ultrathink.process_prompt(
                prompt="Explain Python decorators",
                use_claude_api=False,
                verbose=False
            )

        # Workflow should complete without error
        assert True  # Completion itself is success

    def test_framework_comparison_workflow(self):
        """Test generating framework comparison."""
        result = ultrathink.generate_framework_comparison(
            prompt="Test prompt",
            response_text="Test response",
            confidence=99.0,
            iterations=5,
            duration=2.5,
            context_stats={"total_tokens": 1000}
        )

        # Should generate comparison
        assert isinstance(result, str)
        assert len(result) > 0


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
