#!/usr/bin/env python3
"""
Comprehensive test suite for prompt_history.py
Target: 90%+ coverage with real code testing
"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
from datetime import datetime

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from prompt_history import PromptHistoryManager, format_history_entry


class TestPromptHistoryManager:
    """Test the PromptHistoryManager class"""

    def setup_method(self):
        """Setup test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.history_file = Path(self.temp_dir) / "test_history.json"

    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization_default(self):
        """Test default initialization"""
        manager = PromptHistoryManager()
        assert manager.history_file.name == "prompt_history.json"
        assert manager.history_file.parent.name == "logs"

    def test_initialization_custom_file(self):
        """Test initialization with custom file"""
        manager = PromptHistoryManager(str(self.history_file))
        assert manager.history_file == self.history_file
        assert self.history_file.exists()

    def test_ensure_history_file_creates_new(self):
        """Test that ensure_history_file creates new file if not exists"""
        manager = PromptHistoryManager(str(self.history_file))
        assert self.history_file.exists()
        with open(self.history_file) as f:
            data = json.load(f)
        assert data == []

    def test_ensure_history_file_validates_json(self):
        """Test that ensure_history_file validates existing JSON"""
        # Write valid JSON
        with open(self.history_file, 'w') as f:
            json.dump([{"id": 1, "prompt": "test"}], f)

        manager = PromptHistoryManager(str(self.history_file))

        # File should still exist with same content
        with open(self.history_file) as f:
            data = json.load(f)
        assert data == [{"id": 1, "prompt": "test"}]

    def test_ensure_history_file_backs_up_corrupted(self):
        """Test that corrupted file is backed up"""
        # Write corrupted JSON
        with open(self.history_file, 'w') as f:
            f.write("not valid json {]")

        manager = PromptHistoryManager(str(self.history_file))

        # Should create new empty file
        with open(self.history_file) as f:
            data = json.load(f)
        assert data == []

        # Backup should exist
        backup_files = list(Path(self.temp_dir).glob("test_history.json.backup"))
        assert len(backup_files) == 1

    def test_load_history_empty_file(self):
        """Test loading from empty/new file"""
        manager = PromptHistoryManager(str(self.history_file))
        history = manager._load_history()
        assert history == []

    def test_load_history_with_data(self):
        """Test loading existing history"""
        test_data = [
            {"id": 1, "prompt": "test1"},
            {"id": 2, "prompt": "test2"}
        ]
        with open(self.history_file, 'w') as f:
            json.dump(test_data, f)

        manager = PromptHistoryManager(str(self.history_file))
        history = manager._load_history()
        assert history == test_data

    def test_save_history(self):
        """Test saving history to file"""
        manager = PromptHistoryManager(str(self.history_file))
        test_data = [{"id": 1, "prompt": "test"}]
        manager._save_history(test_data)

        with open(self.history_file) as f:
            saved_data = json.load(f)
        assert saved_data == test_data

    def test_add_prompt_basic(self):
        """Test adding a basic prompt"""
        manager = PromptHistoryManager(str(self.history_file))

        prompt_id = manager.add_prompt(
            prompt="What is 2+2?",
            complexity="SIMPLE",
            agents_allocated=8,
            mode="claude_code",
            duration_seconds=1.234,
            success=True,
            verbose=True
        )

        assert prompt_id == 1

        history = manager._load_history()
        assert len(history) == 1
        assert history[0]["id"] == 1
        assert history[0]["prompt"] == "What is 2+2?"
        assert history[0]["complexity"] == "SIMPLE"
        assert history[0]["agents_allocated"] == 8
        assert history[0]["mode"] == "claude_code"
        assert history[0]["duration_seconds"] == 1.234
        assert history[0]["success"] == True
        assert history[0]["flags"]["verbose"] == True
        assert history[0]["flags"]["quiet"] == False

    def test_add_prompt_with_metadata(self):
        """Test adding prompt with additional metadata"""
        manager = PromptHistoryManager(str(self.history_file))

        metadata = {"extra_field": "value", "count": 42}
        prompt_id = manager.add_prompt(
            prompt="Test prompt",
            complexity="MODERATE",
            agents_allocated=15,
            mode="api",
            additional_metadata=metadata
        )

        history = manager._load_history()
        assert history[0]["metadata"] == metadata

    def test_add_prompt_multiple(self):
        """Test adding multiple prompts gets correct IDs"""
        manager = PromptHistoryManager(str(self.history_file))

        id1 = manager.add_prompt("prompt1", "SIMPLE", 5, "claude_code")
        id2 = manager.add_prompt("prompt2", "COMPLEX", 20, "api")
        id3 = manager.add_prompt("prompt3", "MODERATE", 10, "claude_code")

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3

    def test_get_all_no_limit(self):
        """Test getting all prompts without limit"""
        manager = PromptHistoryManager(str(self.history_file))

        # Add 3 prompts
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")
        manager.add_prompt("p2", "COMPLEX", 10, "api")
        manager.add_prompt("p3", "MODERATE", 8, "claude_code")

        all_prompts = manager.get_all()

        # Should be reversed (newest first)
        assert len(all_prompts) == 3
        assert all_prompts[0]["prompt"] == "p3"
        assert all_prompts[1]["prompt"] == "p2"
        assert all_prompts[2]["prompt"] == "p1"

    def test_get_all_with_limit(self):
        """Test getting prompts with limit"""
        manager = PromptHistoryManager(str(self.history_file))

        for i in range(5):
            manager.add_prompt(f"p{i}", "SIMPLE", 5, "claude_code")

        limited = manager.get_all(limit=2)
        assert len(limited) == 2
        assert limited[0]["prompt"] == "p4"
        assert limited[1]["prompt"] == "p3"

    def test_get_all_with_offset(self):
        """Test getting prompts with offset"""
        manager = PromptHistoryManager(str(self.history_file))

        for i in range(5):
            manager.add_prompt(f"p{i}", "SIMPLE", 5, "claude_code")

        offset_prompts = manager.get_all(offset=2)
        assert len(offset_prompts) == 3
        assert offset_prompts[0]["prompt"] == "p2"

    def test_get_all_with_limit_and_offset(self):
        """Test getting prompts with both limit and offset"""
        manager = PromptHistoryManager(str(self.history_file))

        for i in range(10):
            manager.add_prompt(f"p{i}", "SIMPLE", 5, "claude_code")

        prompts = manager.get_all(limit=3, offset=2)
        assert len(prompts) == 3
        assert prompts[0]["prompt"] == "p7"
        assert prompts[1]["prompt"] == "p6"
        assert prompts[2]["prompt"] == "p5"

    def test_get_by_id_exists(self):
        """Test getting prompt by ID that exists"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")
        id2 = manager.add_prompt("p2", "COMPLEX", 10, "api")
        manager.add_prompt("p3", "MODERATE", 8, "claude_code")

        prompt = manager.get_by_id(id2)
        assert prompt is not None
        assert prompt["id"] == 2
        assert prompt["prompt"] == "p2"
        assert prompt["complexity"] == "COMPLEX"

    def test_get_by_id_not_exists(self):
        """Test getting prompt by ID that doesn't exist"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")

        prompt = manager.get_by_id(999)
        assert prompt is None

    def test_search_in_prompt(self):
        """Test searching in prompt field"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("What is Python?", "SIMPLE", 5, "claude_code")
        manager.add_prompt("Explain JavaScript", "MODERATE", 10, "api")
        manager.add_prompt("Python vs Java", "COMPLEX", 15, "claude_code")

        results = manager.search("Python", search_in="prompt")
        assert len(results) == 2
        assert results[0]["prompt"] == "Python vs Java"
        assert results[1]["prompt"] == "What is Python?"

    def test_search_case_insensitive(self):
        """Test case-insensitive search"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("PYTHON code", "SIMPLE", 5, "claude_code")
        manager.add_prompt("python script", "MODERATE", 10, "api")

        results = manager.search("python", search_in="prompt", case_sensitive=False)
        assert len(results) == 2

    def test_search_case_sensitive(self):
        """Test case-sensitive search"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("PYTHON code", "SIMPLE", 5, "claude_code")
        manager.add_prompt("python script", "MODERATE", 10, "api")

        results = manager.search("python", search_in="prompt", case_sensitive=True)
        assert len(results) == 1
        assert results[0]["prompt"] == "python script"

    def test_search_in_complexity(self):
        """Test searching in complexity field"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")
        manager.add_prompt("p2", "COMPLEX", 10, "api")
        manager.add_prompt("p3", "SIMPLE", 8, "claude_code")

        results = manager.search("SIMPLE", search_in="complexity")
        assert len(results) == 2

    def test_search_in_mode(self):
        """Test searching in mode field"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")
        manager.add_prompt("p2", "COMPLEX", 10, "api")
        manager.add_prompt("p3", "MODERATE", 8, "claude_code")

        results = manager.search("claude_code", search_in="mode")
        assert len(results) == 2

    def test_search_in_all(self):
        """Test searching in all fields"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("test prompt", "SIMPLE", 5, "claude_code")
        manager.add_prompt("another", "test", 10, "api")
        manager.add_prompt("third", "COMPLEX", 8, "test")

        results = manager.search("test", search_in="all")
        assert len(results) == 3

    def test_get_by_date_start_only(self):
        """Test getting prompts by start date only"""
        manager = PromptHistoryManager(str(self.history_file))

        # Add prompts with specific timestamps
        history = [
            {"id": 1, "timestamp": "2025-11-20 10:00:00", "prompt": "p1"},
            {"id": 2, "timestamp": "2025-11-21 10:00:00", "prompt": "p2"},
            {"id": 3, "timestamp": "2025-11-22 10:00:00", "prompt": "p3"}
        ]
        manager._save_history(history)

        results = manager.get_by_date(start_date="2025-11-21")
        assert len(results) == 2
        assert results[0]["prompt"] == "p3"
        assert results[1]["prompt"] == "p2"

    def test_get_by_date_end_only(self):
        """Test getting prompts by end date only"""
        manager = PromptHistoryManager(str(self.history_file))

        history = [
            {"id": 1, "timestamp": "2025-11-20 10:00:00", "prompt": "p1"},
            {"id": 2, "timestamp": "2025-11-21 10:00:00", "prompt": "p2"},
            {"id": 3, "timestamp": "2025-11-22 10:00:00", "prompt": "p3"}
        ]
        manager._save_history(history)

        results = manager.get_by_date(end_date="2025-11-21")
        assert len(results) == 2
        assert results[0]["prompt"] == "p2"
        assert results[1]["prompt"] == "p1"

    def test_get_by_date_range(self):
        """Test getting prompts by date range"""
        manager = PromptHistoryManager(str(self.history_file))

        history = [
            {"id": 1, "timestamp": "2025-11-20 10:00:00", "prompt": "p1"},
            {"id": 2, "timestamp": "2025-11-21 10:00:00", "prompt": "p2"},
            {"id": 3, "timestamp": "2025-11-22 10:00:00", "prompt": "p3"},
            {"id": 4, "timestamp": "2025-11-23 10:00:00", "prompt": "p4"}
        ]
        manager._save_history(history)

        results = manager.get_by_date(start_date="2025-11-21", end_date="2025-11-22")
        assert len(results) == 2
        assert results[0]["prompt"] == "p3"
        assert results[1]["prompt"] == "p2"

    def test_get_statistics_empty(self):
        """Test getting statistics for empty history"""
        manager = PromptHistoryManager(str(self.history_file))
        stats = manager.get_statistics()

        assert stats["total_prompts"] == 0
        assert stats["total_successful"] == 0
        assert stats["total_failed"] == 0
        assert stats["avg_duration_seconds"] == 0

    def test_get_statistics_with_data(self):
        """Test getting statistics with data"""
        manager = PromptHistoryManager(str(self.history_file))

        manager.add_prompt("p1", "SIMPLE", 5, "claude_code", duration_seconds=1.0, success=True)
        manager.add_prompt("p2", "COMPLEX", 20, "api", duration_seconds=3.0, success=False)
        manager.add_prompt("p3", "SIMPLE", 8, "claude_code", duration_seconds=2.0, success=True)

        stats = manager.get_statistics()

        assert stats["total_prompts"] == 3
        assert stats["total_successful"] == 2
        assert stats["total_failed"] == 1
        assert stats["success_rate"] == pytest.approx(66.67, rel=0.01)
        assert stats["avg_duration_seconds"] == 2.0
        assert stats["complexity_breakdown"]["SIMPLE"] == 2
        assert stats["complexity_breakdown"]["COMPLEX"] == 1
        assert stats["mode_breakdown"]["claude_code"] == 2
        assert stats["mode_breakdown"]["api"] == 1
        assert stats["agents_stats"]["min"] == 5
        assert stats["agents_stats"]["max"] == 20
        assert stats["agents_stats"]["avg"] == pytest.approx(11.0, rel=0.01)

    def test_clear_history_without_confirm(self):
        """Test clear history without confirmation"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")

        result = manager.clear_history(confirm=False)
        assert result == False

        # History should still exist
        history = manager._load_history()
        assert len(history) == 1

    def test_clear_history_with_confirm(self):
        """Test clear history with confirmation"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")

        result = manager.clear_history(confirm=True)
        assert result == True

        # History should be empty
        history = manager._load_history()
        assert len(history) == 0

        # Backup should exist
        backup_files = list(Path(self.temp_dir).glob("test_history.json.backup.*"))
        assert len(backup_files) == 1

    def test_export_to_file_json(self):
        """Test exporting to JSON file"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")
        manager.add_prompt("p2", "COMPLEX", 10, "api")

        export_file = Path(self.temp_dir) / "export.json"
        result = manager.export_to_file(str(export_file), format="json")

        assert result == True
        assert export_file.exists()

        with open(export_file) as f:
            exported = json.load(f)
        assert len(exported) == 2

    @patch('builtins.open', side_effect=IOError("Write error"))
    def test_export_to_file_error(self, mock_open):
        """Test export file error handling"""
        manager = PromptHistoryManager(str(self.history_file))

        export_file = "/invalid/path/export.json"
        result = manager.export_to_file(export_file, format="json")

        assert result == False

    def test_export_to_file_csv(self):
        """Test exporting to CSV file"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code", duration_seconds=1.5)
        manager.add_prompt("p2", "COMPLEX", 10, "api", duration_seconds=2.5)

        export_file = Path(self.temp_dir) / "export.csv"
        result = manager.export_to_file(str(export_file), format="csv")

        assert result == True
        assert export_file.exists()

        # Check CSV content
        with open(export_file) as f:
            lines = f.readlines()
        assert len(lines) == 3  # Header + 2 entries
        assert "id,timestamp,prompt,complexity" in lines[0]

    def test_export_to_file_txt(self):
        """Test exporting to text file"""
        manager = PromptHistoryManager(str(self.history_file))
        manager.add_prompt("p1", "SIMPLE", 5, "claude_code")

        export_file = Path(self.temp_dir) / "export.txt"
        result = manager.export_to_file(str(export_file), format="txt")

        assert result == True
        assert export_file.exists()

        with open(export_file) as f:
            content = f.read()
        assert "ID: 1" in content
        assert "Prompt: p1" in content
        assert "Complexity: SIMPLE" in content


class TestFormatHistoryEntry:
    """Test the format_history_entry function"""

    def test_format_basic_entry(self):
        """Test formatting a basic history entry"""
        entry = {
            "id": 1,
            "timestamp": "2025-11-22 10:00:00",
            "prompt": "Test prompt",
            "complexity": "SIMPLE",
            "agents_allocated": 8,
            "mode": "claude_code",
            "duration_seconds": 1.234,
            "success": True,
            "flags": {"verbose": False, "quiet": False}
        }

        formatted = format_history_entry(entry)

        assert "ID: 1" in formatted
        assert "Date: 2025-11-22 10:00:00" in formatted
        assert "Test prompt" in formatted
        assert "SIMPLE" in formatted
        assert "✅ Yes" in formatted

    def test_format_long_prompt_truncated(self):
        """Test that long prompts are truncated"""
        entry = {
            "id": 1,
            "timestamp": "2025-11-22 10:00:00",
            "prompt": "x" * 100,  # Very long prompt
            "complexity": "COMPLEX",
            "agents_allocated": 20,
            "mode": "api",
            "duration_seconds": 5.0,
            "success": False,
            "flags": {"verbose": False, "quiet": False}
        }

        formatted = format_history_entry(entry, show_full_prompt=False)

        # Should be truncated to 77 chars + "..."
        assert "..." in formatted
        assert len(entry["prompt"]) > 80  # Original is long
        prompt_line = [line for line in formatted.split('\n') if 'Prompt:' in line][0]
        assert "xxx..." in prompt_line  # Truncated

    def test_format_full_prompt_shown(self):
        """Test showing full prompt when requested"""
        long_prompt = "x" * 100
        entry = {
            "id": 1,
            "timestamp": "2025-11-22 10:00:00",
            "prompt": long_prompt,
            "complexity": "MODERATE",
            "agents_allocated": 15,
            "mode": "claude_code",
            "duration_seconds": 3.0,
            "success": True,
            "flags": {"verbose": False, "quiet": False}
        }

        formatted = format_history_entry(entry, show_full_prompt=True)

        # Full prompt should be shown
        assert "..." not in formatted
        assert long_prompt in formatted

    def test_format_with_flags(self):
        """Test formatting entry with flags"""
        entry = {
            "id": 1,
            "timestamp": "2025-11-22 10:00:00",
            "prompt": "Test",
            "complexity": "SIMPLE",
            "agents_allocated": 5,
            "mode": "claude_code",
            "duration_seconds": 1.0,
            "success": True,
            "flags": {"verbose": True, "quiet": True}
        }

        formatted = format_history_entry(entry)

        assert "--verbose" in formatted
        assert "--quiet" in formatted

    def test_format_failed_entry(self):
        """Test formatting a failed entry"""
        entry = {
            "id": 1,
            "timestamp": "2025-11-22 10:00:00",
            "prompt": "Failed test",
            "complexity": "COMPLEX",
            "agents_allocated": 25,
            "mode": "api",
            "duration_seconds": 10.0,
            "success": False,
            "flags": {"verbose": False, "quiet": False}
        }

        formatted = format_history_entry(entry)

        assert "❌ No" in formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])