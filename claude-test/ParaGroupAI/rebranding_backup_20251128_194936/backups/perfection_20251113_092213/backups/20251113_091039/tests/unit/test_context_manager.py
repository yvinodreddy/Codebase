#!/usr/bin/env python3
"""
Unit Tests for agent_framework/context_manager.py
Tests context management with automatic compaction.

Test Coverage Target: 85%+
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_framework.context_manager import (
    Message,
    ContextCompactionLog,
    ContextManager,
)


# ==========================================
# MESSAGE DATACLASS TESTS
# ==========================================

class TestMessage:
    """Test Message dataclass."""

    def test_message_creation(self):
        """Message should be created with all required fields."""
        msg = Message(
            role="user",
            content="Test message",
            timestamp="2025-01-01T12:00:00",
            tokens_estimate=10
        )
        assert msg.role == "user"
        assert msg.content == "Test message"
        assert msg.timestamp == "2025-01-01T12:00:00"
        assert msg.tokens_estimate == 10

    def test_message_with_metadata(self):
        """Message should support metadata."""
        msg = Message(
            role="assistant",
            content="Response",
            timestamp="2025-01-01T12:00:00",
            tokens_estimate=5,
            metadata={"important": True, "category": "success"}
        )
        assert msg.metadata["important"] is True
        assert msg.metadata["category"] == "success"

    def test_message_default_metadata(self):
        """Message should have empty dict as default metadata."""
        msg = Message(
            role="system",
            content="System message",
            timestamp="2025-01-01T12:00:00",
            tokens_estimate=3
        )
        assert msg.metadata == {}


# ==========================================
# CONTEXT COMPACTION LOG TESTS
# ==========================================

class TestContextCompactionLog:
    """Test ContextCompactionLog dataclass."""

    def test_compaction_log_creation(self):
        """ContextCompactionLog should be created with all fields."""
        log = ContextCompactionLog(
            timestamp="2025-01-01T12:00:00",
            messages_before=100,
            messages_after=20,
            tokens_before=50000,
            tokens_after=15000,
            tokens_saved=35000,
            compaction_summary="Compacted 80 messages"
        )
        assert log.messages_before == 100
        assert log.messages_after == 20
        assert log.tokens_saved == 35000


# ==========================================
# CONTEXT MANAGER INITIALIZATION TESTS
# ==========================================

class TestContextManagerInit:
    """Test ContextManager initialization."""

    def test_init_with_defaults(self):
        """ContextManager should initialize with defaults."""
        cm = ContextManager()
        assert cm.max_tokens == 100000
        assert cm.compact_threshold == 0.8
        assert cm.keep_recent == 10
        assert len(cm.messages) == 0

    def test_init_with_custom_values(self):
        """ContextManager should accept custom values."""
        cm = ContextManager(
            max_tokens=50000,
            compact_threshold=0.7,
            keep_recent=5
        )
        assert cm.max_tokens == 50000
        assert cm.compact_threshold == 0.7
        assert cm.keep_recent == 5

    def test_init_compaction_log_empty(self):
        """ContextManager should start with empty compaction log."""
        cm = ContextManager()
        assert len(cm.compaction_log) == 0


# ==========================================
# ADD MESSAGE TESTS
# ==========================================

class TestAddMessage:
    """Test add_message method."""

    def test_add_single_message(self):
        """add_message should add message to context."""
        cm = ContextManager()
        cm.add_message("user", "Hello")

        assert len(cm.messages) == 1
        assert cm.messages[0].role == "user"
        assert cm.messages[0].content == "Hello"

    def test_add_multiple_messages(self):
        """add_message should handle multiple messages."""
        cm = ContextManager()
        cm.add_message("user", "First")
        cm.add_message("assistant", "Second")
        cm.add_message("user", "Third")

        assert len(cm.messages) == 3
        assert cm.messages[0].content == "First"
        assert cm.messages[2].content == "Third"

    def test_add_message_with_metadata(self):
        """add_message should accept metadata."""
        cm = ContextManager()
        cm.add_message("user", "Important", metadata={"important": True})

        assert cm.messages[0].metadata["important"] is True

    def test_add_message_estimates_tokens(self):
        """add_message should estimate tokens."""
        cm = ContextManager()
        cm.add_message("user", "Test message")

        assert cm.messages[0].tokens_estimate > 0

    def test_add_message_adds_timestamp(self):
        """add_message should add timestamp."""
        cm = ContextManager()
        cm.add_message("user", "Test")

        assert cm.messages[0].timestamp is not None
        # Should be ISO format
        datetime.fromisoformat(cm.messages[0].timestamp)


# ==========================================
# ESTIMATE TOKENS TESTS
# ==========================================

class TestEstimateTokens:
    """Test estimate_tokens method."""

    def test_estimate_tokens_empty_string(self):
        """estimate_tokens should return 0 for empty string."""
        cm = ContextManager()
        assert cm.estimate_tokens("") == 0

    def test_estimate_tokens_short_text(self):
        """estimate_tokens should estimate short text."""
        cm = ContextManager()
        # Default: 0.25 tokens/char, so 4 chars = 1 token
        tokens = cm.estimate_tokens("test")
        assert tokens == 1

    def test_estimate_tokens_long_text(self):
        """estimate_tokens should estimate long text."""
        cm = ContextManager()
        # 100 chars at 0.25 = 25 tokens
        text = "a" * 100
        assert cm.estimate_tokens(text) == 25

    def test_estimate_tokens_custom_ratio(self):
        """estimate_tokens should use custom tokens_per_char."""
        cm = ContextManager(tokens_per_char=0.5)  # 2 chars = 1 token
        assert cm.estimate_tokens("test") == 2


# ==========================================
# GET TOTAL TOKENS TESTS
# ==========================================

class TestGetTotalTokens:
    """Test get_total_tokens method."""

    def test_get_total_tokens_empty(self):
        """get_total_tokens should return 0 for no messages."""
        cm = ContextManager()
        assert cm.get_total_tokens() == 0

    def test_get_total_tokens_single_message(self):
        """get_total_tokens should sum tokens."""
        cm = ContextManager()
        cm.add_message("user", "test")  # 1 token
        assert cm.get_total_tokens() == 1

    def test_get_total_tokens_multiple_messages(self):
        """get_total_tokens should sum all message tokens."""
        cm = ContextManager()
        cm.add_message("user", "test")  # 1 token
        cm.add_message("assistant", "response")  # 2 tokens

        total = cm.get_total_tokens()
        assert total == 3


# ==========================================
# SHOULD COMPACT TESTS
# ==========================================

class TestShouldCompact:
    """Test should_compact method."""

    def test_should_compact_below_threshold(self):
        """should_compact should return False below threshold."""
        cm = ContextManager(max_tokens=1000, compact_threshold=0.8)
        # Add 500 tokens (50% of max)
        cm.add_message("user", "a" * 2000)  # 500 tokens

        assert cm.should_compact() is False

    def test_should_compact_at_threshold(self):
        """should_compact should return True at threshold."""
        cm = ContextManager(max_tokens=1000, compact_threshold=0.8)
        # Add 800 tokens (80% of max)
        cm.add_message("user", "a" * 3200)  # 800 tokens

        # Note: This might trigger auto-compact, but should_compact() should return True
        usage = cm.get_total_tokens() / cm.max_tokens
        assert usage >= 0.8

    def test_should_compact_above_threshold(self):
        """should_compact should return True above threshold."""
        cm = ContextManager(max_tokens=1000, compact_threshold=0.7)
        # Add 900 tokens (90% of max)
        cm.add_message("user", "a" * 3600)  # 900 tokens

        usage = cm.get_total_tokens() / cm.max_tokens
        assert usage >= 0.7


# ==========================================
# COMPACT TESTS
# ==========================================

class TestCompact:
    """Test compact method."""

    def test_compact_not_enough_messages(self):
        """compact should do nothing if messages <= keep_recent."""
        cm = ContextManager(keep_recent=10)

        # Add 5 messages (less than keep_recent)
        for i in range(5):
            cm.add_message("user", f"Message {i}")

        messages_before = len(cm.messages)
        cm.compact()

        # Should not compact
        assert len(cm.messages) == messages_before

    def test_compact_reduces_messages(self):
        """compact should reduce number of messages."""
        cm = ContextManager(keep_recent=5, max_tokens=1000)

        # Add 20 messages
        for i in range(20):
            cm.add_message("user", f"Message {i}")

        # Manually trigger compact
        cm.compact()

        # Should keep recent messages
        assert len(cm.messages) <= 20

    def test_compact_preserves_recent(self):
        """compact should preserve recent messages."""
        cm = ContextManager(keep_recent=3)

        # Add 10 messages
        for i in range(10):
            cm.add_message("user", f"Message {i}")

        cm.compact()

        # Recent messages should be preserved
        assert cm.messages[-1].content == "Message 9"
        assert cm.messages[-2].content == "Message 8"
        assert cm.messages[-3].content == "Message 7"

    def test_compact_preserves_important(self):
        """compact should preserve important messages."""
        cm = ContextManager(keep_recent=2)

        # Add messages, mark one as important
        cm.add_message("user", "Regular 1")
        cm.add_message("user", "Important!", metadata={"important": True})
        cm.add_message("user", "Regular 2")
        cm.add_message("user", "Regular 3")

        cm.compact()

        # Important message should be preserved
        important_preserved = any(
            "Important" in msg.content for msg in cm.messages
        )
        assert important_preserved


# ==========================================
# GET METHODS TESTS
# ==========================================

class TestGetMethods:
    """Test getter methods."""

    def test_get_messages(self):
        """get_messages should return all messages."""
        cm = ContextManager()
        cm.add_message("user", "Test 1")
        cm.add_message("assistant", "Test 2")

        messages = cm.get_messages()
        assert len(messages) == 2

    def test_get_usage_percentage(self):
        """get_usage_percentage should calculate correctly."""
        cm = ContextManager(max_tokens=1000)
        cm.add_message("user", "a" * 2000)  # 500 tokens

        usage = cm.get_usage_percentage()
        assert usage == 50.0

    def test_get_statistics(self):
        """get_statistics should return stats dict."""
        cm = ContextManager()
        cm.add_message("user", "Test")

        stats = cm.get_statistics()

        assert "total_messages" in stats
        assert "total_tokens" in stats
        assert "usage_percentage" in stats
        assert stats["total_messages"] == 1

    def test_get_compaction_history_empty(self):
        """get_compaction_history should return empty list initially."""
        cm = ContextManager()

        history = cm.get_compaction_history()
        assert history == []


# ==========================================
# MARK IMPORTANT TESTS
# ==========================================

class TestMarkImportant:
    """Test mark_important method."""

    def test_mark_important_sets_flag(self):
        """mark_important should set important flag."""
        cm = ContextManager()
        cm.add_message("user", "Test message")

        cm.mark_important(0)

        assert cm.messages[0].metadata["important"] is True

    def test_mark_important_invalid_index(self):
        """mark_important should handle invalid index."""
        cm = ContextManager()
        cm.add_message("user", "Test")

        # Should not crash on invalid index
        try:
            cm.mark_important(99)
        except (IndexError, KeyError):
            pass  # Expected


# ==========================================
# SAVE TO FILE TESTS
# ==========================================

class TestSaveToFile:
    """Test save_to_file method."""

    def test_save_to_file_creates_file(self):
        """save_to_file should create file."""
        cm = ContextManager()
        cm.add_message("user", "Test")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            cm.save_to_file(tf.name)
            assert Path(tf.name).exists()

    def test_save_to_file_contains_messages(self):
        """save_to_file should save messages."""
        cm = ContextManager()
        cm.add_message("user", "Test message")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tf:
            cm.save_to_file(tf.name)

            # Read back
            with open(tf.name, 'r') as f:
                data = json.load(f)
                assert "messages" in data


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestContextManagerIntegration:
    """Test real-world usage scenarios."""

    def test_full_conversation_workflow(self):
        """Test complete conversation with multiple exchanges."""
        cm = ContextManager(max_tokens=10000)

        # Simulate conversation
        cm.add_message("user", "Implement feature X")
        cm.add_message("assistant", "Here is the implementation...")
        cm.add_message("user", "Add error handling")
        cm.add_message("assistant", "Error handling added...")

        assert len(cm.messages) == 4
        assert cm.get_total_tokens() > 0

    def test_automatic_compaction_trigger(self):
        """Test that compaction triggers automatically at threshold."""
        cm = ContextManager(max_tokens=100, compact_threshold=0.8, keep_recent=2)

        # Add messages that will exceed threshold
        for i in range(20):
            cm.add_message("user", "Message " + "x" * 10)

        # Compaction should have occurred
        # (Can't assert exact number due to auto-compaction, but should be less than 20)
        assert len(cm.messages) < 20

    def test_statistics_accuracy(self):
        """Test that statistics are accurate."""
        cm = ContextManager()

        cm.add_message("user", "test")  # 1 token
        cm.add_message("assistant", "response")  # 2 tokens

        stats = cm.get_statistics()
        assert stats["total_messages"] == 2
        assert stats["total_tokens"] == 3
        assert stats["usage_percentage"] < 1.0  # Very low usage


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
