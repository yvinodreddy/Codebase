"""
Context Manager with Automatic Compaction
Manages agent context and automatically compacts when approaching token limits

Based on Anthropic's /compact command in Claude Code
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Single message in context"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str
    tokens_estimate: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextCompactionLog:
    """Log entry for context compaction event"""
    timestamp: str
    messages_before: int
    messages_after: int
    tokens_before: int
    tokens_after: int
    tokens_saved: int
    compaction_summary: str


class ContextManager:
    """
    Manages agent context with automatic compaction.

    Key features:
    - Tracks token usage
    - Auto-compacts when approaching limit (default 80%)
    - Preserves recent messages
    - Preserves key information (errors, successes)
    - Creates summaries of old messages

    This is critical for long-running agents that would otherwise
    hit context limits.

    Example:
        >>> context = ContextManager(max_tokens=100000)
        >>> context.add_message("user", "Implement feature X")
        >>> context.add_message("assistant", "Here is the implementation...")
        >>> # ... many more messages ...
        >>> # Automatic compaction occurs at 80% usage
        >>> messages = context.get_messages()
    """

    def __init__(
        self,
        max_tokens: int = 100000,
        compact_threshold: float = 0.8,
        keep_recent: int = 10,
        tokens_per_char: float = 0.25  # Rough estimate: 4 chars = 1 token
    ):
        """
        Initialize context manager.

        Args:
            max_tokens: Maximum tokens allowed in context
            compact_threshold: Trigger compaction at this % of max (0.8 = 80%)
            keep_recent: Number of recent messages to always preserve
            tokens_per_char: Estimation factor for token counting
        """
        self.max_tokens = max_tokens
        self.compact_threshold = compact_threshold
        self.keep_recent = keep_recent
        self.tokens_per_char = tokens_per_char

        self.messages: List[Message] = []
        self.compaction_log: List[ContextCompactionLog] = []

        logger.info(
            f"ContextManager initialized (max_tokens={max_tokens}, "
            f"threshold={compact_threshold*100}%)"
        )

    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add message to context and check if compaction needed.

        Args:
            role: "user", "assistant", or "system"
            content: Message content
            metadata: Optional metadata (e.g., {"important": True})
        """
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            tokens_estimate=self.estimate_tokens(content),
            metadata=metadata or {}
        )

        self.messages.append(message)

        logger.debug(f"Added {role} message ({message.tokens_estimate} tokens)")

        # Check if compaction needed
        if self.should_compact():
            logger.info("Context approaching limit, triggering compaction")
            self.compact()

    def should_compact(self) -> bool:
        """Check if context usage exceeds threshold"""
        current_tokens = self.get_total_tokens()
        usage = current_tokens / self.max_tokens

        return usage >= self.compact_threshold

    def compact(self):
        """
        Compact old messages while preserving:
        1. Recent messages (last N)
        2. Important messages (marked in metadata)
        3. Key information (errors, successes)
        """
        if len(self.messages) <= self.keep_recent:
            logger.info("Not enough messages to compact")
            return

        tokens_before = self.get_total_tokens()
        messages_before = len(self.messages)

        # Separate messages
        recent_messages = self.messages[-self.keep_recent:]
        old_messages = self.messages[:-self.keep_recent]

        # Find important messages in old_messages
        important_old = [msg for msg in old_messages if msg.metadata.get("important", False)]

        # Summarize non-important old messages
        regular_old = [msg for msg in old_messages if not msg.metadata.get("important", False)]
        summary = self._create_summary(regular_old)

        # Create compacted message list
        compacted = []

        # Add summary as first message
        if summary:
            compacted.append(Message(
                role="system",
                content=summary,
                timestamp=datetime.now().isoformat(),
                tokens_estimate=self.estimate_tokens(summary),
                metadata={"type": "compaction_summary", "messages_summarized": len(regular_old)}
            ))

        # Add important old messages
        compacted.extend(important_old)

        # Add recent messages
        compacted.extend(recent_messages)

        # Replace messages
        self.messages = compacted

        tokens_after = self.get_total_tokens()
        tokens_saved = tokens_before - tokens_after

        # Log compaction
        log_entry = ContextCompactionLog(
            timestamp=datetime.now().isoformat(),
            messages_before=messages_before,
            messages_after=len(self.messages),
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            tokens_saved=tokens_saved,
            compaction_summary=f"Compacted {len(regular_old)} messages into summary"
        )
        self.compaction_log.append(log_entry)

        logger.info(
            f"Compaction complete: {messages_before} → {len(self.messages)} messages, "
            f"saved {tokens_saved} tokens ({tokens_saved/tokens_before*100:.1f}%)"
        )

    def _create_summary(self, messages: List[Message]) -> str:
        """
        Create summary of old messages.

        Extracts:
        - Key actions taken
        - Important failures/errors
        - Successful outcomes
        - State changes
        """
        if not messages:
            return ""

        # Extract key information
        actions = []
        errors = []
        successes = []
        state_changes = []

        for msg in messages:
            content_lower = msg.content.lower()

            # Identify actions
            if any(word in content_lower for word in ["implement", "create", "build", "execute"]):
                actions.append(msg.content[:200])

            # Identify errors
            if any(word in content_lower for word in ["error", "failed", "exception", "problem"]):
                errors.append(msg.content[:200])

            # Identify successes
            if any(word in content_lower for word in ["success", "completed", "passed", "correct"]):
                successes.append(msg.content[:200])

            # Identify state changes
            if any(word in content_lower for word in ["status:", "state:", "updated to", "changed to"]):
                state_changes.append(msg.content[:200])

        # Build summary
        summary_parts = [
            f"[CONTEXT COMPACTION: Summarized {len(messages)} messages]",
            "",
            "KEY ACTIONS TAKEN:",
        ]

        if actions:
            summary_parts.extend([f"  - {action[:150]}..." for action in actions[:5]])
        else:
            summary_parts.append("  - (none)")

        summary_parts.append("")
        summary_parts.append("IMPORTANT FAILURES/ERRORS:")

        if errors:
            summary_parts.extend([f"  - {error[:150]}..." for error in errors[:5]])
        else:
            summary_parts.append("  - (none)")

        summary_parts.append("")
        summary_parts.append("SUCCESSFUL OUTCOMES:")

        if successes:
            summary_parts.extend([f"  - {success[:150]}..." for success in successes[:5]])
        else:
            summary_parts.append("  - (none)")

        summary_parts.append("")
        summary_parts.append("STATE CHANGES:")

        if state_changes:
            summary_parts.extend([f"  - {change[:150]}..." for change in state_changes[:5]])
        else:
            summary_parts.append("  - (none)")

        summary_parts.append("")
        summary_parts.append(f"Original message count: {len(messages)}")
        summary_parts.append(f"Timespan: {messages[0].timestamp} to {messages[-1].timestamp}")

        return "\n".join(summary_parts)

    def estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count"""
        return int(len(text) * self.tokens_per_char)

    def get_total_tokens(self) -> int:
        """Get total tokens in current context"""
        return sum(msg.tokens_estimate for msg in self.messages)

    def get_messages(self) -> List[Message]:
        """Get all current messages"""
        return self.messages.copy()

    def get_usage_percentage(self) -> float:
        """Get current context usage as percentage"""
        return (self.get_total_tokens() / self.max_tokens) * 100

    def get_statistics(self) -> Dict[str, Any]:
        """Get context statistics"""
        return {
            "total_messages": len(self.messages),
            "total_tokens": self.get_total_tokens(),
            "max_tokens": self.max_tokens,
            "usage_percentage": round(self.get_usage_percentage(), 2),
            "compactions_performed": len(self.compaction_log),
            "total_tokens_saved": sum(log.tokens_saved for log in self.compaction_log)
        }

    def get_compaction_history(self) -> List[Dict[str, Any]]:
        """Get history of compaction events"""
        return [
            {
                "timestamp": log.timestamp,
                "messages_before": log.messages_before,
                "messages_after": log.messages_after,
                "tokens_saved": log.tokens_saved,
                "summary": log.compaction_summary
            }
            for log in self.compaction_log
        ]

    def mark_important(self, message_index: int):
        """Mark a message as important (will be preserved during compaction)"""
        if 0 <= message_index < len(self.messages):
            self.messages[message_index].metadata["important"] = True
            logger.debug(f"Marked message {message_index} as important")

    def save_to_file(self, filepath: str):
        """Save context to file"""
        data = {
            "config": {
                "max_tokens": self.max_tokens,
                "compact_threshold": self.compact_threshold,
                "keep_recent": self.keep_recent
            },
            "statistics": self.get_statistics(),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "tokens": msg.tokens_estimate,
                    "metadata": msg.metadata
                }
                for msg in self.messages
            ],
            "compaction_history": self.get_compaction_history()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Context saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    context = ContextManager(max_tokens=5000, compact_threshold=0.7, keep_recent=3)

    # Simulate a long-running conversation
    print("=" * 60)
    print("CONTEXT MANAGER EXAMPLE")
    print("=" * 60)

    # Add many messages
    for i in range(20):
        context.add_message(
            "user",
            f"Message {i}: " + "This is a test message. " * 20  # ~100 tokens each
        )

        if i % 2 == 0:
            context.add_message(
                "assistant",
                f"Response {i}: " + "This is a response. " * 30  # ~150 tokens each
            )

        # Mark some as important
        if i % 5 == 0:
            context.mark_important(len(context.messages) - 1)

        print(f"\nAfter message {i}:")
        print(f"  Messages: {len(context.messages)}")
        print(f"  Tokens: {context.get_total_tokens()}")
        print(f"  Usage: {context.get_usage_percentage():.1f}%")

    # Show statistics
    print("\n" + "=" * 60)
    print("FINAL STATISTICS")
    print("=" * 60)
    stats = context.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Show compaction history
    if context.compaction_log:
        print("\n" + "=" * 60)
        print("COMPACTION HISTORY")
        print("=" * 60)
        for i, log in enumerate(context.compaction_log, 1):
            print(f"\nCompaction {i}:")
            print(f"  Timestamp: {log.timestamp}")
            print(f"  Messages: {log.messages_before} → {log.messages_after}")
            print(f"  Tokens saved: {log.tokens_saved}")

    # Save to file
    context.save_to_file("/tmp/context_manager_example.json")
    print("\n✅ Context saved to /tmp/context_manager_example.json")
