#!/usr/bin/env python3
"""Comprehensive test suite for realtime_log_monitor.py - Target: 90%+ coverage"""
import pytest
import tempfile
import time
import threading
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from realtime_log_monitor import RealtimeLogMonitor

class TestRealtimeLogMonitor:
    def setup_method(self):
        self.temp_file = tempfile.mktemp(suffix='.log')
        self.callback_results = []
        self.callback = lambda line: self.callback_results.append(line)
    
    def teardown_method(self):
        if Path(self.temp_file).exists():
            Path(self.temp_file).unlink()
    
    def test_initialization(self):
        monitor = RealtimeLogMonitor(self.temp_file, self.callback)
        assert monitor.log_file == self.temp_file
        assert monitor.callback == self.callback
        assert monitor.last_position == 0
        assert monitor.running == False
    
    @patch('time.sleep')
    @patch('os.path.exists')
    def test_start_monitoring_file_not_exists(self, mock_exists, mock_sleep):
        mock_exists.side_effect = [False, False, True]
        monitor = RealtimeLogMonitor(self.temp_file, self.callback)
        monitor.running = True
        
        # Simulate stopping after checking twice
        def stop_after_checks(*args):
            if mock_exists.call_count >= 2:
                monitor.running = False
        mock_sleep.side_effect = stop_after_checks
        
        monitor.start_monitoring()
        assert mock_exists.call_count >= 2
    
    def test_start_monitoring_with_new_content(self):
        # Create file with initial content
        with open(self.temp_file, 'w') as f:
            f.write("Line 1\n")
        
        monitor = RealtimeLogMonitor(self.temp_file, self.callback)
        
        # Start monitoring in thread
        thread = threading.Thread(target=monitor.start_monitoring)
        thread.start()
        
        # Give monitor time to start
        time.sleep(0.1)
        
        # Add new content
        with open(self.temp_file, 'a') as f:
            f.write("Line 2\n")
        
        # Give monitor time to read
        time.sleep(0.1)
        
        # Stop monitoring
        monitor.stop_monitoring()
        thread.join(timeout=1)
        
        assert "Line 1" in self.callback_results or "Line 2" in self.callback_results
    
    def test_stop_monitoring(self):
        monitor = RealtimeLogMonitor(self.temp_file, self.callback)
        monitor.running = True
        monitor.stop_monitoring()
        assert monitor.running == False
    
    @patch('builtins.open', side_effect=Exception("File error"))
    @patch('os.path.exists', return_value=True)
    @patch('time.sleep')
    def test_monitoring_with_exception(self, mock_sleep, mock_exists, mock_open):
        monitor = RealtimeLogMonitor(self.temp_file, self.callback)
        monitor.running = True
        
        # Stop after one iteration
        def stop_monitor(*args):
            monitor.running = False
        mock_sleep.side_effect = stop_monitor
        
        monitor.start_monitoring()
        # Should handle exception gracefully

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
