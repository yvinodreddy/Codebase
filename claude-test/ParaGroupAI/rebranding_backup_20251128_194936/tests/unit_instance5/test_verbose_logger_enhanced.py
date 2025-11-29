#!/usr/bin/env python3
"""
Enhanced comprehensive tests for verbose_logger.py
Target: 90% coverage with real code execution
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock, call
from io import StringIO
import contextlib

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import verbose_logger
from verbose_logger import VerboseLogger

class TestVerboseLoggerComprehensive:
    """Achieve 90% coverage for verbose_logger"""

    def setup_method(self):
        """Setup test instance"""
        self.logger = VerboseLogger()

    def test_initialization(self):
        """Test logger initialization"""
        assert self.logger is not None
        assert hasattr(self.logger, 'verbose')
        assert hasattr(self.logger, 'log')

    def test_set_verbose(self):
        """Test verbose setting"""
        self.logger.set_verbose(True)
        assert self.logger.verbose == True

        self.logger.set_verbose(False)
        assert self.logger.verbose == False

    def test_log_with_verbose_on(self, capsys):
        """Test logging with verbose mode on"""
        self.logger.set_verbose(True)
        self.logger.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_log_with_verbose_off(self, capsys):
        """Test logging with verbose mode off"""
        self.logger.set_verbose(False)
        self.logger.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.out

    def test_log_levels(self, capsys):
        """Test different log levels"""
        self.logger.set_verbose(True)

        self.logger.log("Info message", level="INFO")
        self.logger.log("Warning message", level="WARNING")
        self.logger.log("Error message", level="ERROR")

        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "WARNING" in captured.out
        assert "ERROR" in captured.out

    def test_log_with_timestamp(self, capsys):
        """Test logging with timestamps"""
        self.logger.set_verbose(True)
        self.logger.log_with_timestamp("Message")

        captured = capsys.readouterr()
        assert "Message" in captured.out

    def test_log_stage(self, capsys):
        """Test stage logging"""
        self.logger.set_verbose(True)
        self.logger.log_stage("STAGE 1", "Processing")

        captured = capsys.readouterr()
        assert "STAGE 1" in captured.out
        assert "Processing" in captured.out

    def test_log_separator(self, capsys):
        """Test separator logging"""
        self.logger.set_verbose(True)
        self.logger.log_separator()

        captured = capsys.readouterr()
        assert "=" in captured.out

    def test_edge_cases(self):
        """Test edge cases"""
        # Test with None
        self.logger.log(None)

        # Test with empty string
        self.logger.log("")

        # Test with very long string
        self.logger.log("x" * 10000)

    def test_format_output(self):
        """Test output formatting"""
        if hasattr(self.logger, 'format_output'):
            result = self.logger.format_output("test", prefix="[TEST]")
            assert "[TEST]" in result
