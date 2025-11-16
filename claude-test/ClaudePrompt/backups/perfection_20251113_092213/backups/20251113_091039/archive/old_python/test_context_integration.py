#!/usr/bin/env python3
"""
Test context manager integration with orchestration system
"""

import sys
from master_orchestrator import MasterOrchestrator

def test_context_management():
    """Test that context manager is working and saving tokens"""

    print("=" * 80)
    print("TESTING CONTEXT MANAGER INTEGRATION")
    print("=" * 80)

    # Create orchestrator
    orchestrator = MasterOrchestrator(min_confidence_score=95.0)

    # Simulate multiple requests to trigger compaction
    print("\n📝 Simulating 15 requests to test auto-compaction...")

    for i in range(15):
        prompt = f"Request {i}: " + "This is a test prompt. " * 50  # ~125 tokens each

        print(f"\n--- Request {i+1}/15 ---")
        result = orchestrator.process(prompt)

        # Get context stats
        context_stats = result.quality_metrics.get('context_management', {})

        print(f"   Messages: {context_stats.get('total_messages', 0)}")
        print(f"   Tokens: {context_stats.get('total_tokens', 0):,}")
        print(f"   Usage: {context_stats.get('usage_percentage', 0):.1f}%")

        if context_stats.get('compactions_performed', 0) > 0:
            print(f"   ✨ COMPACTION TRIGGERED!")
            print(f"   Tokens Saved: {context_stats.get('total_tokens_saved', 0):,}")

    # Final summary
    print("\n" + "=" * 80)
    print("FINAL CONTEXT STATISTICS")
    print("=" * 80)

    final_stats = orchestrator.context_manager.get_statistics()

    print(f"Total Messages: {final_stats['total_messages']}")
    print(f"Total Tokens: {final_stats['total_tokens']:,}")
    print(f"Max Tokens: {final_stats['max_tokens']:,}")
    print(f"Usage: {final_stats['usage_percentage']:.1f}%")
    print(f"Compactions Performed: {final_stats['compactions_performed']}")
    print(f"Total Tokens Saved: {final_stats['total_tokens_saved']:,}")

    if final_stats['compactions_performed'] > 0:
        print(f"\n✅ SUCCESS: Context manager is working and saved {final_stats['total_tokens_saved']:,} tokens!")
        print(f"   Reduction: {(final_stats['total_tokens_saved'] / (final_stats['total_tokens'] + final_stats['total_tokens_saved']) * 100):.1f}%")
    else:
        print("\n⚠️  No compactions triggered. Try running more requests or reducing compact_threshold.")

    # Show compaction history
    if orchestrator.context_manager.compaction_log:
        print("\n" + "=" * 80)
        print("COMPACTION HISTORY")
        print("=" * 80)

        for i, log in enumerate(orchestrator.context_manager.compaction_log, 1):
            print(f"\nCompaction {i}:")
            print(f"   Time: {log.timestamp}")
            print(f"   Messages: {log.messages_before} → {log.messages_after}")
            print(f"   Tokens: {log.tokens_before:,} → {log.tokens_after:,}")
            print(f"   Saved: {log.tokens_saved:,} tokens ({log.tokens_saved/log.tokens_before*100:.1f}%)")
            print(f"   Summary: {log.compaction_summary}")

    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_context_management()
