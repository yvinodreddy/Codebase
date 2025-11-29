#!/usr/bin/env python3
"""
Demonstrate Context Manager Token Savings
"""

import logging
from master_orchestrator import MasterOrchestrator

# Quieter logging
logging.basicConfig(level=logging.WARNING)

def demo():
    print("=" * 80)
    print("CONTEXT MANAGER INTEGRATION DEMONSTRATION")
    print("=" * 80)
    print()

    # Create orchestrator with LOWER threshold to trigger compaction sooner
    print("Creating orchestrator with:")
    print("  • Max Tokens: 10,000")
    print("  • Compact Threshold: 60% (6,000 tokens)")
    print("  • Keep Recent: 5 messages")
    print()

    orchestrator = MasterOrchestrator(min_confidence_score=95.0)

    # Manually override for demo purposes
    orchestrator.context_manager.max_tokens = 10000
    orchestrator.context_manager.compact_threshold = 0.6
    orchestrator.context_manager.keep_recent = 5

    print("Simulating 40 requests with ~200 tokens each...")
    print()

    for i in range(40):
        # Each prompt is ~200 tokens
        prompt = f"Request {i}: " + "Generate code for " * 40

        result = orchestrator.process(prompt)

        stats = orchestrator.context_manager.get_statistics()

        # Show progress every 5 requests
        if (i+1) % 5 == 0:
            print(f"After {i+1:2d} requests:")
            print(f"   Messages: {stats['total_messages']:3d}")
            print(f"   Tokens: {stats['total_tokens']:6,} / {stats['max_tokens']:,}")
            print(f"   Usage: {stats['usage_percentage']:5.1f}%")

            if stats['compactions_performed'] > 0:
                savings_pct = (stats['total_tokens_saved'] /
                              (stats['total_tokens'] + stats['total_tokens_saved']) * 100)
                print(f"   💾 COMPACTIONS: {stats['compactions_performed']}")
                print(f"   ✨ TOKENS SAVED: {stats['total_tokens_saved']:,} ({savings_pct:.1f}% reduction)")
            print()

    # Final summary
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    final_stats = orchestrator.context_manager.get_statistics()

    print(f"\n📊 Context Statistics:")
    print(f"   Total Messages: {final_stats['total_messages']}")
    print(f"   Total Tokens: {final_stats['total_tokens']:,}")
    print(f"   Context Usage: {final_stats['usage_percentage']:.1f}%")
    print(f"   Compactions Performed: {final_stats['compactions_performed']}")

    if final_stats['compactions_performed'] > 0:
        total_would_be = final_stats['total_tokens'] + final_stats['total_tokens_saved']
        savings_pct = (final_stats['total_tokens_saved'] / total_would_be * 100)

        print(f"\n💾 Token Savings:")
        print(f"   Without Compaction: {total_would_be:,} tokens")
        print(f"   With Compaction: {final_stats['total_tokens']:,} tokens")
        print(f"   Tokens Saved: {final_stats['total_tokens_saved']:,} tokens")
        print(f"   Reduction: {savings_pct:.1f}%")

        print(f"\n📈 Compaction History:")
        for i, log in enumerate(orchestrator.context_manager.compaction_log, 1):
            print(f"\n   Compaction #{i}:")
            print(f"      Messages: {log.messages_before} → {log.messages_after}")
            print(f"      Tokens: {log.tokens_before:,} → {log.tokens_after:,}")
            print(f"      Saved: {log.tokens_saved:,} tokens")
    else:
        print("\n⚠️  No compactions occurred (threshold not reached)")

    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 80)

    print("\nHow It Works:")
    print("  1. Every user message and assistant response is added to context")
    print("  2. When usage hits 60%, compaction automatically triggers")
    print("  3. Old messages are summarized, important ones preserved")
    print("  4. Recent messages (last 5) always kept intact")
    print("  5. Massive token savings = lower costs & better performance!")
    print()

if __name__ == "__main__":
    demo()
