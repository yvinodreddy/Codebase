"""
Comprehensive tests for parallel_instance_orchestrator.py - Track: track1_core
Target coverage: 95%
Tests REAL code execution with mocked external dependencies
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import json
import threading
import time

try:
    from parallel_instance_orchestrator import ParallelInstanceOrchestrator
except ImportError:
    pytest.skip("Cannot import parallel_instance_orchestrator", allow_module_level=True)


class TestParallelInstanceOrchestrator:
    """Test suite for ParallelInstanceOrchestrator class"""

    def test_instantiation(self):
        """Test that orchestrator instantiates correctly"""
        orchestrator = ParallelInstanceOrchestrator()

        assert orchestrator is not None
        assert orchestrator.base_dir == Path("/home/user01/claude-test/ClaudePrompt")
        assert len(orchestrator.tracks) == 5
        assert "track1" in orchestrator.tracks
        assert orchestrator.tracks["track1"]["target_coverage"] == 95
        assert orchestrator.tracks["track1"]["priority"] == "CRITICAL"

    def test_tracks_configuration(self):
        """Test that all 5 tracks are properly configured"""
        orchestrator = ParallelInstanceOrchestrator()

        # Verify all 5 tracks exist
        assert "track1" in orchestrator.tracks
        assert "track2" in orchestrator.tracks
        assert "track3" in orchestrator.tracks
        assert "track4" in orchestrator.tracks
        assert "track5" in orchestrator.tracks

        # Verify track1 (Core System)
        track1 = orchestrator.tracks["track1"]
        assert track1["name"] == "Core System"
        assert "files" in track1
        assert len(track1["files"]) == 6
        assert "ultrathink.py" in track1["files"]

        # Verify track2 (Agent Framework)
        track2 = orchestrator.tracks["track2"]
        assert track2["name"] == "Agent Framework"
        assert "pattern" in track2
        assert track2["pattern"] == "agent_framework/*.py"

    def test_status_initialization(self):
        """Test that status dictionary is initialized correctly"""
        orchestrator = ParallelInstanceOrchestrator()

        assert len(orchestrator.status) == 5
        for track_id, status in orchestrator.status.items():
            assert status["running"] == False
            assert status["coverage"] == 0
            assert status["tests"] == 0

    def test_get_files_for_track_with_explicit_files(self):
        """Test get_files_for_track for tracks with explicit file lists"""
        orchestrator = ParallelInstanceOrchestrator()

        # Test track1 which has explicit files
        files = orchestrator.get_files_for_track("track1")

        assert isinstance(files, list)
        assert len(files) == 6
        assert "ultrathink.py" in files
        assert "master_orchestrator.py" in files
        assert "config.py" in files

    @patch('parallel_instance_orchestrator.Path.glob')
    def test_get_files_for_track_with_pattern(self, mock_glob):
        """Test get_files_for_track for tracks with glob patterns"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock glob to return fake files
        mock_glob.return_value = [
            Path("/home/user01/claude-test/ClaudePrompt/agent_framework/file1.py"),
            Path("/home/user01/claude-test/ClaudePrompt/agent_framework/file2.py")
        ]

        # Test track2 which uses patterns
        files = orchestrator.get_files_for_track("track2")

        assert isinstance(files, list)
        assert len(files) == 2

    def test_get_files_for_track_empty(self):
        """Test get_files_for_track with track that has no files"""
        orchestrator = ParallelInstanceOrchestrator()

        # Add a test track with no files or patterns
        orchestrator.tracks["test_empty"] = {"name": "Empty"}

        files = orchestrator.get_files_for_track("test_empty")

        assert isinstance(files, list)
        assert len(files) == 0

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    def test_generate_tests_for_track_success(self, mock_open, mock_subprocess):
        """Test generate_tests_for_track with successful execution"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess to return success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock measure_track_coverage
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 96.5, "tests": 10}

            result = orchestrator.generate_tests_for_track("track1")

        assert result["track"] == "track1"
        assert result["status"] == "completed"
        assert result["coverage_achieved"] == 96.5
        assert result["tests_created"] == 10
        assert result["files_processed"] == 6  # track1 has 6 files

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    def test_generate_tests_for_track_with_failures(self, mock_open, mock_subprocess):
        """Test generate_tests_for_track with some failures"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess to alternate between success and failure
        mock_results = [Mock(returncode=0), Mock(returncode=1, stderr="Error")]
        mock_subprocess.side_effect = mock_results * 3  # 6 files

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock measure_track_coverage
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 85.0, "tests": 5}

            result = orchestrator.generate_tests_for_track("track1")

        assert result["track"] == "track1"
        assert result["status"] == "completed"
        assert result["files_processed"] == 3  # Only 3 succeeded

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    def test_generate_tests_for_track_timeout(self, mock_open, mock_subprocess):
        """Test generate_tests_for_track with timeout"""
        import subprocess
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess to raise TimeoutExpired
        mock_subprocess.side_effect = subprocess.TimeoutExpired(cmd=[], timeout=600)

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock measure_track_coverage
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 0, "tests": 0}

            result = orchestrator.generate_tests_for_track("track1")

        # Should complete despite timeout
        assert result["track"] == "track1"
        assert result["status"] == "completed"
        assert result["files_processed"] == 0  # All timed out

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    @patch('pathlib.Path.glob')
    def test_measure_track_coverage_success(self, mock_glob, mock_open, mock_subprocess):
        """Test measure_track_coverage with valid coverage data"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess run
        mock_subprocess.return_value = Mock(returncode=0)

        # Mock JSON file with coverage data
        coverage_data = {
            "totals": {
                "percent_covered": 92.5
            }
        }
        mock_file = MagicMock()
        mock_file.read.return_value = json.dumps(coverage_data)
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock glob for test count
        mock_glob.return_value = [Path("test1.py"), Path("test2.py"), Path("test3.py")]

        result = orchestrator.measure_track_coverage("track1")

        assert result["coverage"] == 92.5
        assert result["tests"] == 3

    @patch('parallel_instance_orchestrator.subprocess.run')
    def test_measure_track_coverage_failure(self, mock_subprocess):
        """Test measure_track_coverage when subprocess fails"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess to raise exception
        mock_subprocess.side_effect = Exception("Coverage failed")

        result = orchestrator.measure_track_coverage("track1")

        assert result["coverage"] == 0
        assert result["tests"] == 0

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    def test_run_track_in_thread(self, mock_open, mock_subprocess):
        """Test run_track_in_thread executes correctly"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess
        mock_subprocess.return_value = Mock(returncode=0)

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock measure_track_coverage
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 95.0, "tests": 15}

            # Run in thread
            orchestrator.run_track_in_thread("track1")

        # Verify status was updated
        assert orchestrator.status["track1"]["running"] == False
        assert orchestrator.status["track1"]["coverage"] == 95.0
        assert orchestrator.status["track1"]["tests"] == 15

    def test_print_progress(self, capsys):
        """Test print_progress displays status correctly"""
        orchestrator = ParallelInstanceOrchestrator()

        # Set some status
        orchestrator.status["track1"]["running"] = True
        orchestrator.status["track1"]["coverage"] = 92.5
        orchestrator.status["track1"]["tests"] = 10

        orchestrator.status["track2"]["running"] = False
        orchestrator.status["track2"]["coverage"] = 88.0
        orchestrator.status["track2"]["tests"] = 8

        orchestrator.print_progress()

        captured = capsys.readouterr()
        assert "Elapsed:" in captured.out
        assert "track1" in captured.out
        assert "track2" in captured.out
        assert "RUNNING" in captured.out
        assert "DONE" in captured.out

    def test_print_final_report(self, capsys):
        """Test print_final_report displays completion summary"""
        orchestrator = ParallelInstanceOrchestrator()

        # Set completion status
        orchestrator.status["track1"]["coverage"] = 95.0
        orchestrator.status["track1"]["tests"] = 15
        orchestrator.status["track2"]["coverage"] = 90.0
        orchestrator.status["track2"]["tests"] = 12
        orchestrator.status["track3"]["coverage"] = 88.0
        orchestrator.status["track3"]["tests"] = 10
        orchestrator.status["track4"]["coverage"] = 92.0
        orchestrator.status["track4"]["tests"] = 14
        orchestrator.status["track5"]["coverage"] = 85.0
        orchestrator.status["track5"]["tests"] = 8

        orchestrator.print_final_report()

        captured = capsys.readouterr()
        assert "PARALLEL EXECUTION COMPLETE" in captured.out
        assert "Total Time:" in captured.out
        assert "Total Tests Created: 59" in captured.out
        assert "Average Coverage: 90.0%" in captured.out
        assert "PRODUCTION READY" in captured.out

    @patch('parallel_instance_orchestrator.subprocess.run')
    @patch('builtins.open', create=True)
    @patch('parallel_instance_orchestrator.threading.Thread')
    @patch('time.sleep')
    def test_run_all_tracks_parallel(self, mock_sleep, mock_thread, mock_open, mock_subprocess):
        """Test run_all_tracks_parallel orchestrates all tracks"""
        orchestrator = ParallelInstanceOrchestrator()

        # Mock subprocess
        mock_subprocess.return_value = Mock(returncode=0)

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock threads
        mock_threads = []
        for i in range(5):
            mock_t = Mock()
            # is_alive returns: True (while checking), False (done)
            # Use return_value for repeatable behavior instead of side_effect
            mock_t.is_alive.return_value = False  # All threads immediately done
            mock_threads.append(mock_t)

        mock_thread.side_effect = mock_threads

        # Mock measure_track_coverage
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 90.0, "tests": 10}

            # This should complete quickly due to mocks
            orchestrator.run_all_tracks_parallel()

        # Verify 5 threads were created
        assert mock_thread.call_count == 5

        # Verify all threads were started
        for mock_t in mock_threads:
            mock_t.start.assert_called_once()
            mock_t.join.assert_called_once()


def test_main_function():
    """Test that main() can be called (integration test)"""
    with patch('parallel_instance_orchestrator.ParallelInstanceOrchestrator') as mock_orch:
        mock_instance = Mock()
        mock_orch.return_value = mock_instance

        from parallel_instance_orchestrator import main

        main()

        # Verify orchestrator was created and run
        mock_orch.assert_called_once()
        mock_instance.run_all_tracks_parallel.assert_called_once()


def test_edge_case_empty_track():
    """Test handling of track with no files"""
    orchestrator = ParallelInstanceOrchestrator()

    # Override track1 to have no files
    orchestrator.tracks["track1"]["files"] = []

    with patch('builtins.open', create=True):
        with patch.object(orchestrator, 'measure_track_coverage') as mock_measure:
            mock_measure.return_value = {"coverage": 0, "tests": 0}

            result = orchestrator.generate_tests_for_track("track1")

    assert result["files_processed"] == 0
    assert result["status"] == "completed"


def test_edge_case_invalid_track_id():
    """Test handling of invalid track ID"""
    orchestrator = ParallelInstanceOrchestrator()

    # This should raise KeyError for invalid track
    with pytest.raises(KeyError):
        files = orchestrator.get_files_for_track("invalid_track")


def test_start_time_initialization():
    """Test that start_time is set on instantiation"""
    before = time.time()
    orchestrator = ParallelInstanceOrchestrator()
    after = time.time()

    assert before <= orchestrator.start_time <= after


def test_track_pattern_with_multiple_patterns():
    """Test track with multiple glob patterns (track4)"""
    orchestrator = ParallelInstanceOrchestrator()

    track4 = orchestrator.tracks["track4"]
    assert "pattern" in track4
    assert "," in track4["pattern"]  # Multiple patterns separated by comma

    patterns = track4["pattern"].split(",")
    assert len(patterns) == 2
    assert "security/*.py" in patterns
    assert "database/*.py" in patterns
