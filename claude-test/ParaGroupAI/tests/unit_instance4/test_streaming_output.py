#!/usr/bin/env python3
"""Comprehensive test suite for streaming_output.py - Target: 90%+ coverage"""
import pytest
import tempfile
import os
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from streaming_output import StreamingOutput, stream_ultrathinkc_command, display_large_output

class TestStreamingOutput:
    def setup_method(self):
        self.temp_file = tempfile.mktemp(suffix='_test_output.txt')

    def teardown_method(self):
        if Path(self.temp_file).exists():
            Path(self.temp_file).unlink()

    def test_initialization_with_file(self):
        stream = StreamingOutput(self.temp_file)
        assert stream.output_file == Path(self.temp_file)
        assert stream.line_count == 0
        assert stream.byte_count == 0

    def test_initialization_without_file(self):
        stream = StreamingOutput()
        assert stream.output_file.suffix == '_cppultrathink_output.txt'
        stream.cleanup()

    @patch('subprocess.Popen')
    def test_stream_command_output_success(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = ["Line 1\n", "Line 2\n", "Line 3\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        stream = StreamingOutput(self.temp_file)
        return_code, line_count, duration = stream.stream_command_output(
            ["echo", "test"], display_realtime=False
        )

        assert return_code == 0
        assert line_count == 3
        assert duration > 0

    @patch('subprocess.Popen', side_effect=Exception("Process error"))
    def test_stream_command_output_error(self, mock_popen):
        stream = StreamingOutput(self.temp_file)

        with pytest.raises(IOError):
            stream.stream_command_output(["invalid_command"])

    def test_read_output_file_not_exists(self):
        stream = StreamingOutput(self.temp_file)

        with pytest.raises(FileNotFoundError):
            list(stream.read_output())

    def test_read_output_with_content(self):
        # Write test content
        with open(self.temp_file, 'w') as f:
            for i in range(10):
                f.write(f"Line {i}\n")

        stream = StreamingOutput(self.temp_file)
        chunks = list(stream.read_output(chunk_size=3))

        assert len(chunks) == 4  # 10 lines / 3 per chunk = 4 chunks

    def test_get_line_count(self):
        with open(self.temp_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\n")

        stream = StreamingOutput(self.temp_file)
        count = stream.get_line_count()
        assert count == 3

    def test_get_line_count_no_file(self):
        stream = StreamingOutput(self.temp_file)
        count = stream.get_line_count()
        assert count == 0

    def test_get_stats(self):
        stream = StreamingOutput(self.temp_file)
        stream.line_count = 100
        stream.byte_count = 1024
        stream.start_time = time.time() - 5
        stream.end_time = time.time()

        stats = stream.get_stats()
        assert stats['line_count'] == 100
        assert stats['byte_count'] == 1024
        assert stats['duration_seconds'] > 4
        assert stats['lines_per_second'] > 0

    def test_cleanup(self):
        # Create file
        Path(self.temp_file).touch()

        stream = StreamingOutput(self.temp_file)
        stream.cleanup()

        assert not Path(self.temp_file).exists()

@patch('streaming_output.StreamingOutput')
def test_stream_ultrathinkc_command(mock_stream_class):
    mock_stream = MagicMock()
    mock_stream.line_count = 10
    mock_stream_class.return_value = mock_stream
    mock_stream.stream_command_output.return_value = (0, 10, 1.5)

    stream, code = stream_ultrathinkc_command("test prompt", verbose=True)

    assert code == 0
    mock_stream.stream_command_output.assert_called_once()

@patch('builtins.print')
def test_display_large_output_small(mock_print):
    temp_file = tempfile.mktemp()
    with open(temp_file, 'w') as f:
        f.write("Line 1\nLine 2\n")

    display_large_output(temp_file, max_lines_inline=10)

    # Should display inline
    assert any("FULL OUTPUT" in str(call) for call in mock_print.call_args_list)

    Path(temp_file).unlink()

@patch('builtins.print')
def test_display_large_output_large(mock_print):
    temp_file = tempfile.mktemp()
    with open(temp_file, 'w') as f:
        for i in range(600):
            f.write(f"Line {i}\n")

    display_large_output(temp_file, max_lines_inline=500)

    # Should show summary
    assert any("LARGE OUTPUT SUMMARY" in str(call) for call in mock_print.call_args_list)

    Path(temp_file).unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])