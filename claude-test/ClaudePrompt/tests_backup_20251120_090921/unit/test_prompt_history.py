#!/usr/bin/env python3
"""
Unit Tests for prompt_history.py
Tests prompt history tracking and management.

Test Coverage Target: 85%+
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from prompt_history import PromptHistoryManager, format_history_entry


# ==========================================
# INITIALIZATION TESTS
# ==========================================

class TestPromptHistoryManagerInit:
    """Test PromptHistoryManager initialization."""

    def test_init_with_custom_file(self):
        """PromptHistoryManager should initialize with custom file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)
            assert manager.history_file == Path(tf.name)

    def test_init_creates_empty_history(self):
        """PromptHistoryManager should create empty history file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            # File should exist
            assert manager.history_file.exists()

            # Should be empty list
            history = manager._load_history()
            assert history == []

    def test_init_handles_existing_file(self):
        """PromptHistoryManager should handle existing history file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as tf:
            # Write existing history
            json.dump([
                {"id": 1, "prompt": "test", "complexity": "SIMPLE"}
            ], tf)
            tf.flush()

            manager = PromptHistoryManager(history_file=tf.name)
            history = manager._load_history()

            assert len(history) == 1
            assert history[0]["id"] == 1

    def test_init_handles_corrupted_file(self):
        """PromptHistoryManager should handle corrupted JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as tf:
            # Write invalid JSON
            tf.write("{ invalid json }")
            tf.flush()

            manager = PromptHistoryManager(history_file=tf.name)

            # Should create backup and start fresh
            history = manager._load_history()
            assert history == []


# ==========================================
# ADD PROMPT TESTS
# ==========================================

class TestAddPrompt:
    """Test add_prompt method."""

    def test_add_prompt_basic(self):
        """add_prompt should add prompt to history."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            prompt_id = manager.add_prompt(
                prompt="What is 2+2?",
                complexity="SIMPLE",
                agents_allocated=8,
                mode="claude_code"
            )

            assert prompt_id == 1

            history = manager._load_history()
            assert len(history) == 1
            assert history[0]["prompt"] == "What is 2+2?"
            assert history[0]["complexity"] == "SIMPLE"

    def test_add_prompt_increments_id(self):
        """add_prompt should increment ID for each prompt."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            id1 = manager.add_prompt("First", "SIMPLE", 5, "claude_code")
            id2 = manager.add_prompt("Second", "MODERATE", 10, "claude_code")
            id3 = manager.add_prompt("Third", "COMPLEX", 20, "claude_code")

            assert id1 == 1
            assert id2 == 2
            assert id3 == 3

    def test_add_prompt_with_metadata(self):
        """add_prompt should store additional metadata."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt(
                prompt="Test",
                complexity="SIMPLE",
                agents_allocated=5,
                mode="claude_code",
                duration_seconds=1.234,
                success=True,
                verbose=True,
                quiet=False,
                additional_metadata={"custom": "data"}
            )

            history = manager._load_history()
            entry = history[0]

            assert entry["duration_seconds"] == 1.234
            assert entry["success"] is True
            assert entry["flags"]["verbose"] is True
            assert entry["flags"]["quiet"] is False
            assert entry["metadata"]["custom"] == "data"

    def test_add_prompt_rounds_duration(self):
        """add_prompt should round duration to 3 decimals."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt(
                prompt="Test",
                complexity="SIMPLE",
                agents_allocated=5,
                mode="claude_code",
                duration_seconds=1.23456789
            )

            history = manager._load_history()
            assert history[0]["duration_seconds"] == 1.235


# ==========================================
# GET ALL TESTS
# ==========================================

class TestGetAll:
    """Test get_all method."""

    def test_get_all_empty(self):
        """get_all should return empty list for no history."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            result = manager.get_all()
            assert result == []

    def test_get_all_returns_newest_first(self):
        """get_all should return prompts newest first."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("First", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Second", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Third", "SIMPLE", 5, "claude_code")

            results = manager.get_all()

            # Should be reversed (newest first)
            assert results[0]["id"] == 3
            assert results[1]["id"] == 2
            assert results[2]["id"] == 1

    def test_get_all_with_limit(self):
        """get_all should respect limit parameter."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            for i in range(10):
                manager.add_prompt(f"Prompt {i}", "SIMPLE", 5, "claude_code")

            results = manager.get_all(limit=5)

            assert len(results) == 5

    def test_get_all_with_offset(self):
        """get_all should respect offset parameter."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            for i in range(10):
                manager.add_prompt(f"Prompt {i}", "SIMPLE", 5, "claude_code")

            results = manager.get_all(offset=5)

            # Skip first 5 (newest), get remaining 5
            assert len(results) == 5
            assert results[0]["id"] == 5  # 6th newest (ID 5)

    def test_get_all_with_limit_and_offset(self):
        """get_all should handle both limit and offset."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            for i in range(10):
                manager.add_prompt(f"Prompt {i}", "SIMPLE", 5, "claude_code")

            results = manager.get_all(limit=3, offset=2)

            assert len(results) == 3
            # Should be IDs 8, 7, 6 (skip 10, 9, get next 3)
            assert results[0]["id"] == 8


# ==========================================
# GET BY ID TESTS
# ==========================================

class TestGetById:
    """Test get_by_id method."""

    def test_get_by_id_found(self):
        """get_by_id should return entry if found."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("First", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Second", "MODERATE", 10, "claude_code")

            result = manager.get_by_id(2)

            assert result is not None
            assert result["id"] == 2
            assert result["prompt"] == "Second"

    def test_get_by_id_not_found(self):
        """get_by_id should return None if not found."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("First", "SIMPLE", 5, "claude_code")

            result = manager.get_by_id(999)

            assert result is None


# ==========================================
# SEARCH TESTS
# ==========================================

class TestSearch:
    """Test search method."""

    def test_search_in_prompt(self):
        """search should find matches in prompt text."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Calculate fibonacci", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Sort a list", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Generate fibonacci sequence", "MODERATE", 10, "claude_code")

            results = manager.search("fibonacci")

            assert len(results) == 2
            assert all("fibonacci" in r["prompt"].lower() for r in results)

    def test_search_case_insensitive(self):
        """search should be case-insensitive by default."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("FIBONACCI", "SIMPLE", 5, "claude_code")

            results = manager.search("fibonacci")

            assert len(results) == 1

    def test_search_case_sensitive(self):
        """search should support case-sensitive search."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("FIBONACCI", "SIMPLE", 5, "claude_code")
            manager.add_prompt("fibonacci", "SIMPLE", 5, "claude_code")

            results = manager.search("fibonacci", case_sensitive=True)

            # Should only match lowercase
            assert len(results) == 1

    def test_search_in_complexity(self):
        """search should support searching in complexity."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Task 1", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Task 2", "COMPLEX", 20, "claude_code")
            manager.add_prompt("Task 3", "SIMPLE", 5, "claude_code")

            results = manager.search("complex", search_in="complexity")

            assert len(results) == 1
            assert results[0]["complexity"] == "COMPLEX"

    def test_search_in_all_fields(self):
        """search should support searching in all fields."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test prompt", "SIMPLE", 5, "claude_code")
            manager.add_prompt("Another task", "SIMPLE", 5, "api")

            results = manager.search("api", search_in="all")

            assert len(results) == 1
            assert results[0]["mode"] == "api"


# ==========================================
# GET BY DATE TESTS
# ==========================================

class TestGetByDate:
    """Test get_by_date method."""

    def test_get_by_date_with_start(self):
        """get_by_date should filter by start date."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            # Manually create entries with specific dates
            history = [
                {"id": 1, "timestamp": "2025-01-01 10:00:00", "prompt": "Old"},
                {"id": 2, "timestamp": "2025-01-15 10:00:00", "prompt": "Recent"}
            ]
            manager._save_history(history)

            results = manager.get_by_date(start_date="2025-01-10")

            assert len(results) == 1
            assert results[0]["id"] == 2

    def test_get_by_date_with_end(self):
        """get_by_date should filter by end date."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            history = [
                {"id": 1, "timestamp": "2025-01-01 10:00:00", "prompt": "Old"},
                {"id": 2, "timestamp": "2025-01-15 10:00:00", "prompt": "Recent"}
            ]
            manager._save_history(history)

            results = manager.get_by_date(end_date="2025-01-10")

            assert len(results) == 1
            assert results[0]["id"] == 1

    def test_get_by_date_range(self):
        """get_by_date should filter by date range."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            history = [
                {"id": 1, "timestamp": "2025-01-01 10:00:00", "prompt": "Old"},
                {"id": 2, "timestamp": "2025-01-15 10:00:00", "prompt": "Mid"},
                {"id": 3, "timestamp": "2025-01-30 10:00:00", "prompt": "Recent"}
            ]
            manager._save_history(history)

            results = manager.get_by_date(start_date="2025-01-10", end_date="2025-01-20")

            assert len(results) == 1
            assert results[0]["id"] == 2


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    def test_get_statistics_empty(self):
        """get_statistics should handle empty history."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            stats = manager.get_statistics()

            assert stats["total_prompts"] == 0
            assert stats["total_successful"] == 0
            assert stats["total_failed"] == 0
            assert stats["avg_duration_seconds"] == 0

    def test_get_statistics_with_data(self):
        """get_statistics should calculate correct stats."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Task 1", "SIMPLE", 5, "claude_code", duration_seconds=1.0, success=True)
            manager.add_prompt("Task 2", "COMPLEX", 20, "api", duration_seconds=3.0, success=True)
            manager.add_prompt("Task 3", "SIMPLE", 5, "claude_code", duration_seconds=2.0, success=False)

            stats = manager.get_statistics()

            assert stats["total_prompts"] == 3
            assert stats["total_successful"] == 2
            assert stats["total_failed"] == 1
            assert stats["success_rate"] == pytest.approx(66.67, abs=0.1)
            assert stats["avg_duration_seconds"] == 2.0

    def test_get_statistics_complexity_breakdown(self):
        """get_statistics should show complexity breakdown."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("T1", "SIMPLE", 5, "claude_code")
            manager.add_prompt("T2", "SIMPLE", 5, "claude_code")
            manager.add_prompt("T3", "COMPLEX", 20, "claude_code")

            stats = manager.get_statistics()

            assert stats["complexity_breakdown"]["SIMPLE"] == 2
            assert stats["complexity_breakdown"]["COMPLEX"] == 1

    def test_get_statistics_mode_breakdown(self):
        """get_statistics should show mode breakdown."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("T1", "SIMPLE", 5, "claude_code")
            manager.add_prompt("T2", "SIMPLE", 5, "claude_code")
            manager.add_prompt("T3", "SIMPLE", 5, "api")

            stats = manager.get_statistics()

            assert stats["mode_breakdown"]["claude_code"] == 2
            assert stats["mode_breakdown"]["api"] == 1

    def test_get_statistics_agents_stats(self):
        """get_statistics should calculate agent statistics."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("T1", "SIMPLE", 5, "claude_code")
            manager.add_prompt("T2", "MODERATE", 15, "claude_code")
            manager.add_prompt("T3", "COMPLEX", 25, "claude_code")

            stats = manager.get_statistics()

            assert stats["agents_stats"]["min"] == 5
            assert stats["agents_stats"]["max"] == 25
            assert stats["agents_stats"]["avg"] == 15.0


# ==========================================
# CLEAR HISTORY TESTS
# ==========================================

class TestClearHistory:
    """Test clear_history method."""

    def test_clear_history_requires_confirmation(self):
        """clear_history should require confirmation."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test", "SIMPLE", 5, "claude_code")

            # Without confirmation
            result = manager.clear_history(confirm=False)

            assert result is False
            assert len(manager._load_history()) == 1

    def test_clear_history_with_confirmation(self):
        """clear_history should clear with confirmation."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test", "SIMPLE", 5, "claude_code")

            # With confirmation
            result = manager.clear_history(confirm=True)

            assert result is True
            assert len(manager._load_history()) == 0


# ==========================================
# EXPORT TESTS
# ==========================================

class TestExportToFile:
    """Test export_to_file method."""

    def test_export_to_json(self):
        """export_to_file should export to JSON."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test", "SIMPLE", 5, "claude_code")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as export_file:
                result = manager.export_to_file(export_file.name, format='json')

                assert result is True

                # Verify exported content
                with open(export_file.name, 'r') as f:
                    exported = json.load(f)
                    assert len(exported) == 1
                    assert exported[0]["prompt"] == "Test"

    def test_export_to_csv(self):
        """export_to_file should export to CSV."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test", "SIMPLE", 5, "claude_code")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as export_file:
                result = manager.export_to_file(export_file.name, format='csv')

                assert result is True
                assert Path(export_file.name).stat().st_size > 0

    def test_export_to_txt(self):
        """export_to_file should export to TXT."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            manager.add_prompt("Test", "SIMPLE", 5, "claude_code")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as export_file:
                result = manager.export_to_file(export_file.name, format='txt')

                assert result is True

                with open(export_file.name, 'r') as f:
                    content = f.read()
                    assert "ID: 1" in content
                    assert "Prompt: Test" in content


# ==========================================
# FORMAT ENTRY TESTS
# ==========================================

class TestFormatHistoryEntry:
    """Test format_history_entry function."""

    def test_format_entry_basic(self):
        """format_history_entry should format entry."""
        entry = {
            'id': 1,
            'timestamp': '2025-01-01 12:00:00',
            'prompt': 'Test prompt',
            'complexity': 'SIMPLE',
            'agents_allocated': 5,
            'mode': 'claude_code',
            'duration_seconds': 1.234,
            'success': True,
            'flags': {}
        }

        result = format_history_entry(entry)

        assert "ID: 1" in result
        assert "Test prompt" in result
        assert "✅ Yes" in result

    def test_format_entry_truncates_long_prompt(self):
        """format_history_entry should truncate long prompts."""
        entry = {
            'id': 1,
            'timestamp': '2025-01-01 12:00:00',
            'prompt': 'a' * 100,
            'complexity': 'SIMPLE',
            'agents_allocated': 5,
            'mode': 'claude_code',
            'duration_seconds': 1.0,
            'success': True,
            'flags': {}
        }

        result = format_history_entry(entry, show_full_prompt=False)

        assert "..." in result

    def test_format_entry_shows_flags(self):
        """format_history_entry should show flags."""
        entry = {
            'id': 1,
            'timestamp': '2025-01-01 12:00:00',
            'prompt': 'Test',
            'complexity': 'SIMPLE',
            'agents_allocated': 5,
            'mode': 'claude_code',
            'duration_seconds': 1.0,
            'success': True,
            'flags': {'verbose': True, 'quiet': False}
        }

        result = format_history_entry(entry)

        assert "--verbose" in result


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestPromptHistoryIntegration:
    """Test real-world prompt history scenarios."""

    def test_complete_workflow(self):
        """Test complete prompt history workflow."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            manager = PromptHistoryManager(history_file=tf.name)

            # Add multiple prompts
            manager.add_prompt("Task 1", "SIMPLE", 5, "claude_code", duration_seconds=1.0)
            manager.add_prompt("Task 2", "MODERATE", 10, "claude_code", duration_seconds=2.5)
            manager.add_prompt("Task 3", "COMPLEX", 20, "api", duration_seconds=5.0, success=False)

            # Get all
            all_prompts = manager.get_all()
            assert len(all_prompts) == 3

            # Search
            results = manager.search("Task")
            assert len(results) == 3

            # Get statistics
            stats = manager.get_statistics()
            assert stats["total_prompts"] == 3
            assert stats["total_successful"] == 2
            assert stats["total_failed"] == 1


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
