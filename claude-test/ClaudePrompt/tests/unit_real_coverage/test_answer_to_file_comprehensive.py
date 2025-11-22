#!/usr/bin/env python3
"""
Comprehensive tests for answer_to_file.py
Target: 95%+ code coverage with REAL CODE tests (not mocks)
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from answer_to_file import append_answer_section


class TestAppendAnswerSection:
    """Test the append_answer_section function with real code execution"""

    def test_basic_functionality(self, tmp_path):
        """Test basic answer appending to a file"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("ULTRATHINK output here\n")

        answer = "This is Claude Code's answer to the question."

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()

        # Verify answer is present
        assert answer in content
        # Verify visual markers
        assert "🎯 CLAUDE CODE'S ANSWER" in content
        assert "⬇️" in content
        assert "⬆️" in content
        assert "THE ANSWER STARTS HERE" in content
        assert "THE ANSWER ENDS HERE" in content
        assert "✅ You can now read this file from top to bottom!" in content
        # Verify separator lines
        assert "=" * 80 in content

    def test_empty_answer(self, tmp_path):
        """Test appending an empty answer"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("Initial content\n")

        append_answer_section(str(output_file), "")

        content = output_file.read_text()
        assert "🎯 CLAUDE CODE'S ANSWER" in content
        # Verify markers are still present even with empty answer
        assert "THE ANSWER STARTS HERE" in content

    def test_long_multiline_answer(self, tmp_path):
        """Test appending a long multiline answer"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("ULTRATHINK processing...\n")

        answer = """This is a very long answer that spans multiple lines.

It includes:
- Multiple paragraphs
- Bullet points
- Code blocks

All of this should be preserved exactly as provided."""

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()

        # Verify full answer is present
        assert answer in content
        # Verify multiline structure is preserved
        assert "Multiple paragraphs" in content
        assert "Bullet points" in content
        assert "Code blocks" in content

    def test_special_characters_in_answer(self, tmp_path):
        """Test answer with special characters"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("Content\n")

        answer = "Answer with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()
        assert answer in content

    def test_unicode_characters_in_answer(self, tmp_path):
        """Test answer with unicode characters"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("Content\n")

        answer = "Answer with unicode: 你好 世界 🌍 ñ ü ö"

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()
        assert answer in content

    def test_appends_to_existing_content(self, tmp_path):
        """Test that function appends without overwriting existing content"""
        output_file = tmp_path / "output.txt"
        existing = "Existing ULTRATHINK output\nLine 2\nLine 3"
        output_file.write_text(existing)

        answer = "New answer"

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()

        # Verify existing content is preserved
        assert existing in content
        # Verify new answer is added
        assert answer in content

    def test_creates_file_if_not_exists(self, tmp_path):
        """Test that function creates file if it doesn't exist"""
        output_file = tmp_path / "new_file.txt"
        assert not output_file.exists()

        answer = "Answer for new file"

        append_answer_section(str(output_file), answer)

        assert output_file.exists()
        content = output_file.read_text()
        assert answer in content

    def test_visual_markers_format(self, tmp_path):
        """Test that visual markers are properly formatted"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("")

        answer = "Test answer"

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()
        lines = content.split('\n')

        # Find the marker lines
        arrow_down_lines = [line for line in lines if line.startswith("⬇️")]
        arrow_up_lines = [line for line in lines if line.startswith("⬆️")]

        # Verify we have the expected number of arrow lines
        assert len(arrow_down_lines) >= 1
        assert len(arrow_up_lines) >= 1

        # Verify separator lines are 80 characters
        equals_lines = [line for line in lines if line.startswith("=" * 70)]
        assert len(equals_lines) >= 2  # At least opening and closing separators

    def test_file_permissions_error(self, tmp_path):
        """Test handling of file permission errors"""
        output_file = tmp_path / "readonly.txt"
        output_file.write_text("Content")
        output_file.chmod(0o444)  # Read-only

        answer = "Test answer"

        # Should raise PermissionError on Linux/Unix
        with pytest.raises((PermissionError, OSError)):
            append_answer_section(str(output_file), answer)

        # Restore permissions for cleanup
        output_file.chmod(0o644)

    def test_nonexistent_directory(self):
        """Test with a path to a non-existent directory"""
        output_file = "/nonexistent/directory/file.txt"
        answer = "Test answer"

        with pytest.raises((FileNotFoundError, OSError)):
            append_answer_section(output_file, answer)


class TestMainBlock:
    """Test the main block command-line interface via subprocess"""

    def test_main_via_subprocess_success(self, tmp_path):
        """Test main block execution via subprocess with valid arguments"""
        import subprocess

        output_file = tmp_path / "output.txt"
        output_file.write_text("Initial content\n")
        answer = "Test answer from command line"

        result = subprocess.run(
            [sys.executable, 'answer_to_file.py', str(output_file), answer],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "✅ Answer appended to" in result.stdout

        content = output_file.read_text()
        assert answer in content

    def test_main_via_subprocess_insufficient_args(self):
        """Test main block with insufficient arguments"""
        import subprocess

        result = subprocess.run(
            [sys.executable, 'answer_to_file.py'],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1
        assert "Usage:" in result.stdout

    def test_main_via_subprocess_one_arg(self):
        """Test main block with only one argument"""
        import subprocess

        result = subprocess.run(
            [sys.executable, 'answer_to_file.py', '/tmp/test.txt'],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1
        assert "Usage:" in result.stdout


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_large_answer(self, tmp_path):
        """Test with a very large answer (10MB+)"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("")

        # Create a large answer (10MB)
        answer = "A" * (10 * 1024 * 1024)

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()
        assert answer in content

    def test_answer_with_null_bytes(self, tmp_path):
        """Test answer containing null bytes"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("")

        answer = "Answer with\x00null\x00bytes"

        append_answer_section(str(output_file), answer)

        # File should contain the answer (null bytes may be preserved or stripped by OS)
        assert output_file.exists()

    def test_concurrent_appends(self, tmp_path):
        """Test multiple sequential appends to same file"""
        output_file = tmp_path / "output.txt"
        output_file.write_text("Initial\n")

        append_answer_section(str(output_file), "Answer 1")
        append_answer_section(str(output_file), "Answer 2")
        append_answer_section(str(output_file), "Answer 3")

        content = output_file.read_text()

        # All three answers should be present
        assert "Answer 1" in content
        assert "Answer 2" in content
        assert "Answer 3" in content


class TestFilePathTypes:
    """Test different file path types"""

    def test_relative_path(self, tmp_path, monkeypatch):
        """Test with relative file path"""
        monkeypatch.chdir(tmp_path)

        output_file = "relative_output.txt"
        Path(output_file).write_text("")

        answer = "Relative path test"

        append_answer_section(output_file, answer)

        content = Path(output_file).read_text()
        assert answer in content

    def test_absolute_path(self, tmp_path):
        """Test with absolute file path"""
        output_file = tmp_path / "absolute_output.txt"
        output_file.write_text("")

        answer = "Absolute path test"

        append_answer_section(str(output_file.absolute()), answer)

        content = output_file.read_text()
        assert answer in content

    def test_path_with_spaces(self, tmp_path):
        """Test with file path containing spaces"""
        output_file = tmp_path / "file with spaces.txt"
        output_file.write_text("")

        answer = "Spaces in path"

        append_answer_section(str(output_file), answer)

        content = output_file.read_text()
        assert answer in content
