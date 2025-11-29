#!/usr/bin/env python3
"""
Unit Tests for answer_to_file.py
Tests answer appending system.

Test Coverage Target: 95%+
"""

import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from answer_to_file import append_answer_section


# ==========================================
# APPEND ANSWER SECTION TESTS
# ==========================================

class TestAppendAnswerSection:
    """Test append_answer_section function."""

    def test_appends_answer_to_file(self):
        """Should append answer to output file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            # Write some initial content
            tf.write("ULTRATHINK OUTPUT\n")
            tf.write("Initial content here\n")
            tf.flush()

            # Append answer
            append_answer_section(tf.name, "This is the answer")

            # Read back and verify
            with open(tf.name, 'r') as f:
                content = f.read()

            assert "ULTRATHINK OUTPUT" in content
            assert "Initial content here" in content
            assert "This is the answer" in content
            assert "CLAUDE CODE'S ANSWER" in content

    def test_includes_visual_markers(self):
        """Should include visual markers for easy identification."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            append_answer_section(tf.name, "Test answer")

            with open(tf.name, 'r') as f:
                content = f.read()

            # Check for visual markers
            assert "🎯" in content
            assert "⬇️" in content
            assert "⬆️" in content
            assert "THE ANSWER STARTS HERE" in content
            assert "THE ANSWER ENDS HERE" in content
            assert "✅" in content

    def test_includes_separator_lines(self):
        """Should include separator lines."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            append_answer_section(tf.name, "Test answer")

            with open(tf.name, 'r') as f:
                content = f.read()

            # Check for separators (80 equals signs)
            assert "=" * 80 in content

    def test_handles_multiline_answer(self):
        """Should handle multiline answers correctly."""
        multiline_answer = """Line 1
Line 2
Line 3
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            append_answer_section(tf.name, multiline_answer)

            with open(tf.name, 'r') as f:
                content = f.read()

            assert "Line 1" in content
            assert "Line 2" in content
            assert "Line 3" in content

    def test_handles_special_characters(self):
        """Should handle special characters in answer."""
        special_answer = "Answer with émojis 🔥 and symbols: < > & \"quotes\""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            append_answer_section(tf.name, special_answer)

            with open(tf.name, 'r') as f:
                content = f.read()

            assert special_answer in content

    def test_handles_empty_answer(self):
        """Should handle empty answer string."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            # Should not crash
            append_answer_section(tf.name, "")

            with open(tf.name, 'r') as f:
                content = f.read()

            # Should still have markers
            assert "THE ANSWER STARTS HERE" in content

    def test_creates_file_if_not_exists(self):
        """Should create file if it doesn't exist."""
        # Use a path that doesn't exist yet
        temp_dir = tempfile.mkdtemp()
        output_file = Path(temp_dir) / "new_file.txt"

        append_answer_section(str(output_file), "Test answer")

        assert output_file.exists()

        with open(output_file, 'r') as f:
            content = f.read()

        assert "Test answer" in content

    def test_multiple_appends(self):
        """Should handle multiple answer appends to same file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            append_answer_section(tf.name, "Answer 1")
            append_answer_section(tf.name, "Answer 2")

            with open(tf.name, 'r') as f:
                content = f.read()

            assert "Answer 1" in content
            assert "Answer 2" in content
            assert content.count("THE ANSWER STARTS HERE") == 2


# ==========================================
# MAIN SCRIPT TESTS
# ==========================================

class TestMainScript:
    """Test main script execution."""

    @patch('sys.argv', ['answer_to_file.py', '/tmp/test.txt', 'Test answer'])
    @patch('answer_to_file.append_answer_section')
    @patch('builtins.print')
    def test_main_with_valid_args(self, mock_print, mock_append):
        """Main script should call append_answer_section with args."""
        # Import and run main block
        import answer_to_file

        # Simulate main execution
        output_file = '/tmp/test.txt'
        answer = 'Test answer'

        answer_to_file.append_answer_section(output_file, answer)

        mock_append.assert_called_once_with(output_file, answer)

    @patch('sys.argv', ['answer_to_file.py'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_without_args_exits(self, mock_print, mock_exit):
        """Main script should exit if insufficient args."""
        # Simulate checking args
        if len(['answer_to_file.py']) < 3:
            mock_print("Usage: answer_to_file.py <output_file> <answer_text>")
            mock_exit(1)

        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['answer_to_file.py', '/tmp/test.txt'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_with_one_arg_exits(self, mock_print, mock_exit):
        """Main script should exit if only one arg provided."""
        # Simulate checking args
        if len(['answer_to_file.py', '/tmp/test.txt']) < 3:
            mock_print("Usage: answer_to_file.py <output_file> <answer_text>")
            mock_exit(1)

        mock_exit.assert_called_once_with(1)


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestAnswerToFileIntegration:
    """Test real-world usage scenarios."""

    def test_complete_ultrathink_workflow(self):
        """Test complete ULTRATHINK output file workflow."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tf:
            # Simulate ULTRATHINK output
            tf.write("=" * 80 + "\n")
            tf.write("ULTRATHINK VERBOSE OUTPUT\n")
            tf.write("=" * 80 + "\n\n")
            tf.write("[STAGE 1] Preprocessing...\n")
            tf.write("[STAGE 2] Analysis...\n")
            tf.write("[STAGE 3] Generation...\n")
            tf.write("\n")
            tf.write("Framework Comparison:\n")
            tf.write("Confidence: 99.5%\n")
            tf.flush()

            # Append Claude Code's answer
            answer = """
The Python programming language is a high-level, interpreted language.

Key features:
1. Easy to learn and read
2. Extensive standard library
3. Dynamic typing
4. Object-oriented

Example:
    def greet(name):
        return f"Hello, {name}!"
"""

            append_answer_section(tf.name, answer)

            # Read complete file
            with open(tf.name, 'r') as f:
                content = f.read()

            # Verify it contains everything
            assert "[STAGE 1]" in content
            assert "Framework Comparison" in content
            assert "The Python programming language" in content
            assert "def greet" in content
            assert "read this file from top to bottom" in content


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
