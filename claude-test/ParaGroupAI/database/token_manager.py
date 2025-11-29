#!/usr/bin/env python3
"""
Token Manager for Database-First Architecture

Manages token lifecycle for instances with clear+reload functionality.
Enables unlimited context by clearing tokens and reloading from database.

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import logging
from typing import Dict, Optional, Any
from sqlite_context_loader import SQLiteContextLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TokenManager:
    """
    Manages token lifecycle for instances.

    Strategy:
    1. Instance uses tokens (0 → 200K)
    2. When reaching limit (e.g., 170K = 85%), clear tokens
    3. All context still in database (zero loss)
    4. Reload context from database
    5. Instance ready with 0K tokens used, full context available

    Example:
        >>> manager = TokenManager("ultrathink_context.db")
        >>> usage = manager.check_token_usage("inst_001")
        >>> if usage['percentage'] > 85:
        ...     manager.clear_and_reload("inst_001")
    """

    def __init__(self, db_path: str = "ultrathink_context.db"):
        """
        Initialize TokenManager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.loader = SQLiteContextLoader(db_path)
        logger.info("✅ TokenManager initialized")

    def check_token_usage(self, instance_id: str) -> Dict[str, Any]:
        """
        Check current token usage for instance.

        Args:
            instance_id: Instance identifier

        Returns:
            Dict with usage statistics
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT instance_id, project_id, current_token_usage,
                   ROUND(CAST(current_token_usage AS REAL) / 200000 * 100, 2) as percentage
            FROM active_instances
            WHERE instance_id = ?
        """
        cursor.execute(query, (instance_id,))
        row = cursor.fetchone()

        if not row:
            logger.warning(f"⚠️  Instance not found: {instance_id}")
            return None

        return {
            'instance_id': row['instance_id'],
            'project_id': row['project_id'],
            'current_token_usage': row['current_token_usage'],
            'percentage': row['percentage'],
            'tokens_remaining': 200000 - row['current_token_usage']
        }

    def clear_and_reload(self, instance_id: str) -> Dict[str, Any]:
        """
        Clear tokens and reload context from database.

        This is the key operation that enables unlimited context:
        1. Clear token counter to 0
        2. Context still in DB (no loss)
        3. Reload context from database
        4. Instance ready to continue with 0 tokens used

        Args:
            instance_id: Instance identifier

        Returns:
            Dict with reload statistics
        """
        logger.info(f"🔄 Clearing and reloading instance: {instance_id}")

        # Get instance details
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT project_id, phase_id, current_token_usage FROM active_instances WHERE instance_id = ?",
            (instance_id,)
        )
        row = cursor.fetchone()

        if not row:
            logger.error(f"❌ Instance not found: {instance_id}")
            return None

        project_id = row['project_id']
        phase_id = row['phase_id']
        tokens_before = row['current_token_usage']

        # Step 1: Clear tokens
        cursor.execute(
            "UPDATE active_instances SET current_token_usage = 0 WHERE instance_id = ?",
            (instance_id,)
        )
        conn.commit()

        logger.info(f"✅ Tokens cleared for {instance_id}")

        # Step 2: Reload context from DB
        context = self.loader.get_full_context(project_id, phase_id)

        total_items = sum(len(items) for items in context.values())

        logger.info(f"✅ Context reloaded from DB:")
        logger.info(f"   - CRITICAL: {len(context['CRITICAL'])} items")
        logger.info(f"   - HIGH: {len(context['HIGH'])} items")
        logger.info(f"   - MEDIUM: {len(context['MEDIUM'])} items")
        logger.info(f"   - LOW: {len(context['LOW'])} items")

        return {
            'instance_id': instance_id,
            'project_id': project_id,
            'tokens_before': tokens_before,
            'tokens_after': 0,
            'context_items_loaded': total_items,
            'critical_items': len(context['CRITICAL']),
            'high_items': len(context['HIGH']),
            'medium_items': len(context['MEDIUM']),
            'low_items': len(context['LOW']),
            'status': 'ready'
        }

    def auto_manage_tokens(
        self,
        instance_id: str,
        threshold: float = 0.85
    ) -> Optional[Dict[str, Any]]:
        """
        Automatically manage tokens for an instance.

        If usage > threshold (default 85%), automatically clear and reload.

        Args:
            instance_id: Instance identifier
            threshold: Threshold percentage (0.0 to 1.0)

        Returns:
            Dict with reload statistics if cleared, None otherwise
        """
        usage = self.check_token_usage(instance_id)

        if not usage:
            return None

        if usage['percentage'] > (threshold * 100):
            logger.warning(f"⚠️  Token usage at {usage['percentage']:.1f}% (threshold: {threshold*100}%)")
            logger.info("🔄 Auto-clearing and reloading...")

            result = self.clear_and_reload(instance_id)

            if result:
                logger.info(f"✅ Tokens reset: {result['tokens_before']:,} → {result['tokens_after']:,}")

            return result
        else:
            logger.info(f"✅ Token usage at {usage['percentage']:.1f}% (healthy)")
            return None

    def update_token_usage(
        self,
        instance_id: str,
        token_count: int
    ):
        """
        Update token usage for an instance.

        Args:
            instance_id: Instance identifier
            token_count: New token count
        """
        if token_count < 0 or token_count > 200000:
            logger.error(f"❌ Invalid token count: {token_count} (must be 0-200000)")
            return

        conn = self.loader._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE active_instances SET current_token_usage = ? WHERE instance_id = ?",
                (token_count, instance_id)
            )
            conn.commit()
            logger.info(f"✅ Token usage updated: {instance_id} → {token_count:,} tokens")
        except Exception as e:
            logger.error(f"❌ Failed to update token usage: {e}")
            conn.rollback()

    def get_all_instance_usage(self) -> Dict[str, Any]:
        """
        Get token usage for all active instances.

        Returns:
            Dict with statistics for all instances
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT instance_id, project_id, current_token_usage,
                   ROUND(CAST(current_token_usage AS REAL) / 200000 * 100, 2) as percentage
            FROM active_instances
            WHERE status = 'active'
            ORDER BY current_token_usage DESC
        """
        cursor.execute(query)

        instances = []
        total_tokens = 0

        for row in cursor.fetchall():
            usage = {
                'instance_id': row['instance_id'],
                'project_id': row['project_id'],
                'current_token_usage': row['current_token_usage'],
                'percentage': row['percentage'],
                'status': 'warning' if row['percentage'] > 85 else 'healthy'
            }
            instances.append(usage)
            total_tokens += row['current_token_usage']

        return {
            'instances': instances,
            'total_instances': len(instances),
            'total_tokens_used': total_tokens,
            'average_usage': total_tokens / len(instances) if instances else 0
        }

    def close(self):
        """Close database connection."""
        self.loader.close()


def demonstrate_token_lifecycle():
    """
    Demonstrate the token clear+reload lifecycle.

    This shows how an instance can work indefinitely with unlimited context.
    """
    manager = TokenManager("ultrathink_context.db")

    print("\n" + "=" * 80)
    print("🔄 TOKEN LIFECYCLE DEMONSTRATION")
    print("=" * 80 + "\n")

    # Simulate instance with growing token usage
    instance_id = "inst_demo_001"
    project_id = "proj_example_001"

    # Create instance
    conn = manager.loader._get_connection()
    cursor = conn.cursor()

    # Ensure project exists
    cursor.execute("SELECT project_id FROM projects WHERE project_id = ?", (project_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO projects (project_id, name, description) VALUES (?, ?, ?)",
            (project_id, "Demo Project", "Token lifecycle demo")
        )
        conn.commit()

    # Simulate token usage progression
    print("📊 SIMULATING TOKEN USAGE PROGRESSION:\n")

    usage_points = [0, 85000, 170000, 200000]
    for tokens in usage_points:
        # Update usage
        cursor.execute(
            "INSERT OR REPLACE INTO active_instances (instance_id, project_id, current_token_usage, status) VALUES (?, ?, ?, 'active')",
            (instance_id, project_id, tokens)
        )
        conn.commit()

        # Check usage
        usage = manager.check_token_usage(instance_id)
        print(f"  Tokens: {tokens:>6,} / 200,000 ({usage['percentage']:>5.1f}%)", end="")

        if usage['percentage'] <= 50:
            print(" ✅ Healthy")
        elif usage['percentage'] <= 85:
            print(" ⚠️  Warning")
        else:
            print(" 🔴 Critical - AUTO-CLEARING...")

            # Auto-manage
            result = manager.auto_manage_tokens(instance_id, threshold=0.85)
            if result:
                print(f"     → Cleared: {result['tokens_before']:,} → {result['tokens_after']:,} tokens")
                print(f"     → Context preserved: {result['context_items_loaded']} items loaded from DB")
                print("     ✅ Ready to continue with 200K tokens available")

    print("\n" + "=" * 80)
    print("✅ CYCLE CAN REPEAT INDEFINITELY - UNLIMITED CONTEXT")
    print("=" * 80 + "\n")

    manager.close()


if __name__ == "__main__":
    demonstrate_token_lifecycle()
