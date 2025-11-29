#!/usr/bin/env python3
"""Comprehensive test suite for realtime_verbose_logger.py - Target: 90%+ coverage"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from realtime_verbose_logger import RealtimeVerboseLogger, create_realtime_logger

class TestRealtimeVerboseLogger:
    def setup_method(self):
        self.temp_file = tempfile.mktemp(suffix='.log')
        self.logger = RealtimeVerboseLogger(self.temp_file, enabled=True)
    
    def teardown_method(self):
        if hasattr(self, 'logger'):
            self.logger.close()
        if Path(self.temp_file).exists():
            Path(self.temp_file).unlink()
    
    def test_initialization(self):
        assert self.logger.output_file == self.temp_file
        assert self.logger.enabled == True
        assert self.logger.file_handle is not None
    
    @patch('sys.stdout')
    def test_write(self, mock_stdout):
        self.logger._write("Test message")
        mock_stdout.flush.assert_called()
        
        # Check file content
        with open(self.temp_file) as f:
            content = f.read()
        assert "Test message" in content
    
    def test_stage_header(self):
        self.logger.stage_header(1, "Test Stage")
        with open(self.temp_file) as f:
            content = f.read()
        assert "STAGE 1: Test Stage" in content
    
    def test_stage_footer(self):
        self.logger.stage_header(1, "Test")
        self.logger.stage_footer()
        with open(self.temp_file) as f:
            content = f.read()
        assert "STAGE 1 completed" in content
    
    def test_info(self):
        self.logger.info("Info message", indent=False)
        with open(self.temp_file) as f:
            content = f.read()
        assert "Info message" in content
    
    def test_success(self):
        self.logger.success("Success message")
        with open(self.temp_file) as f:
            content = f.read()
        assert "✓ Success message" in content
    
    def test_warning(self):
        self.logger.warning("Warning message")
        with open(self.temp_file) as f:
            content = f.read()
        assert "⚠️  Warning message" in content
    
    def test_error(self):
        self.logger.error("Error message")
        with open(self.temp_file) as f:
            content = f.read()
        assert "❌ Error message" in content
    
    def test_metric(self):
        self.logger.metric("Key", "Value")
        with open(self.temp_file) as f:
            content = f.read()
        assert "Key: Value" in content
    
    def test_processing_step(self):
        self.logger.processing_step("Step 1", "in progress")
        self.logger.processing_step("Step 2", "done")
        self.logger.processing_step("Step 3", "failed")
        with open(self.temp_file) as f:
            content = f.read()
        assert "→ Step 1" in content
        assert "✓ Step 2" in content
        assert "❌ Step 3" in content
    
    def test_guardrail_layer(self):
        self.logger.guardrail_layer(
            1, "Test Layer", "Test Purpose", 
            True, {"key": "value"}
        )
        with open(self.temp_file) as f:
            content = f.read()
        assert "Layer 1: Test Layer" in content
        assert "✅ PASS" in content
    
    def test_disabled_logger(self):
        logger = RealtimeVerboseLogger(self.temp_file, enabled=False)
        logger.info("Should not appear")
        logger.close()
        
        with open(self.temp_file) as f:
            content = f.read()
        assert "Should not appear" not in content
    
    def test_close(self):
        self.logger.close()
        assert self.logger.file_handle.closed if hasattr(self.logger.file_handle, 'closed') else True

def test_create_realtime_logger():
    temp_file = tempfile.mktemp(suffix='.log')
    logger = create_realtime_logger(temp_file, enabled=True)
    assert isinstance(logger, RealtimeVerboseLogger)
    logger.close()
    if Path(temp_file).exists():
        Path(temp_file).unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
