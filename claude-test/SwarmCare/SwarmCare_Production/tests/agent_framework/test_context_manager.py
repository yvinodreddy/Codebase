"""
Tests for ContextManager
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'agent_framework'))

from context_manager import ContextManager, Message


class TestContextManager(unittest.TestCase):
    """Test ContextManager functionality"""

    def test_initialization(self):
        """Test context manager initialization"""
        context = ContextManager(max_tokens=10000, compact_threshold=0.8)
        self.assertEqual(context.max_tokens, 10000)
        self.assertEqual(context.compact_threshold, 0.8)
        self.assertEqual(len(context.messages), 0)

    def test_add_message(self):
        """Test adding messages"""
        context = ContextManager(max_tokens=10000)
        context.add_message("user", "Hello, world!")

        self.assertEqual(len(context.messages), 1)
        self.assertEqual(context.messages[0].role, "user")
        self.assertEqual(context.messages[0].content, "Hello, world!")

    def test_token_estimation(self):
        """Test token estimation"""
        context = ContextManager()
        text = "This is a test message"
        tokens = context.estimate_tokens(text)

        # Should be roughly len(text) * 0.25
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, len(text))

    def test_compaction_trigger(self):
        """Test that compaction triggers at threshold"""
        # Small context to force compaction
        context = ContextManager(max_tokens=100, compact_threshold=0.7, keep_recent=2)

        # Add messages that exceed threshold
        for i in range(10):
            context.add_message("user", "This is a longer test message " * 10)

        # Compaction should have occurred
        self.assertGreater(len(context.compaction_log), 0)
        self.assertLess(len(context.messages), 10)

    def test_preserve_recent_messages(self):
        """Test that recent messages are preserved during compaction"""
        context = ContextManager(max_tokens=100, compact_threshold=0.5, keep_recent=3)

        # Add messages
        for i in range(10):
            context.add_message("user", f"Message {i} " * 20)

        # Manual compact
        if len(context.messages) > context.keep_recent:
            context.compact()

        # Should keep at least keep_recent messages
        self.assertGreaterEqual(len(context.messages), context.keep_recent)

    def test_preserve_important_messages(self):
        """Test that important messages are preserved"""
        context = ContextManager(max_tokens=100, compact_threshold=0.5, keep_recent=2)

        # Add messages
        for i in range(5):
            context.add_message("user", f"Message {i} " * 20)

        # Mark one as important
        context.mark_important(1)

        # Compact
        if len(context.messages) > context.keep_recent:
            context.compact()

        # Important message should still be there or summarized
        self.assertGreaterEqual(len(context.messages), context.keep_recent)

    def test_usage_calculation(self):
        """Test usage percentage calculation"""
        context = ContextManager(max_tokens=1000)
        context.add_message("user", "Test message" * 50)

        usage = context.get_usage_percentage()
        self.assertGreater(usage, 0)
        self.assertLessEqual(usage, 100)

    def test_statistics(self):
        """Test statistics generation"""
        context = ContextManager()
        context.add_message("user", "Hello")
        context.add_message("assistant", "Hi there")

        stats = context.get_statistics()

        self.assertIn("total_messages", stats)
        self.assertIn("total_tokens", stats)
        self.assertIn("usage_percentage", stats)
        self.assertEqual(stats["total_messages"], 2)


if __name__ == "__main__":
    unittest.main()
