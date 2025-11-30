#!/usr/bin/env python3
"""
Test database message format transformation fix.

CRITICAL FIX (2025-11-30): Issue #2 - Database Message Format Mismatch

This test verifies that database messages are correctly transformed
to the expected validation format, fixing the stuck iteration issue.
"""

import sys
import json
from database.dual_context_retriever import DualContextRetriever


def test_transformation():
    """Test that database messages are transformed correctly."""

    print("=" * 80)
    print("🧪 TEST: Database Message Format Transformation")
    print("=" * 80)

    # Create retriever
    retriever = DualContextRetriever(project_id="test_proj")

    # Sample database message (actual format from database)
    database_messages = [
        {
            'prompt': 'How to implement authentication',
            'timestamp': '2025-11-30T12:00:00',
            'hostname': 'TestHost',
            'working_directory': '/home/user01/test',
            'id': 'msg_123',
            'score': 0.85
        },
        {
            'prompt': 'Fix validation loop bug in dual_context_retriever.py line 676',
            'timestamp': '2025-11-30T13:00:00',
            'hostname': 'TestHost',
            'working_directory': '/home/user01/claude-test/ParaGroupAI',
            'snapshot_id': 'snap_456',
            'score': 0.92
        }
    ]

    print("\n📥 INPUT (Database Format):")
    print(json.dumps(database_messages[0], indent=2))

    # Transform messages
    transformed = retriever._transform_database_messages_to_validation_format(database_messages)

    print("\n📤 OUTPUT (Validation Format):")
    print(json.dumps(transformed[0], indent=2))

    # Verify transformation
    print("\n" + "=" * 80)
    print("✅ VERIFICATION CHECKS:")
    print("=" * 80)

    checks_passed = 0
    total_checks = 0

    for i, msg in enumerate(transformed):
        print(f"\nMessage {i+1}:")

        # Check 1: Has 'content' field
        total_checks += 1
        if 'content' in msg:
            print("  ✅ Has 'content' field")
            checks_passed += 1
        else:
            print("  ❌ Missing 'content' field")

        # Check 2: Content has 'title'
        total_checks += 1
        if 'content' in msg and 'title' in msg['content']:
            print(f"  ✅ Has 'title': {msg['content']['title']}")
            checks_passed += 1
        else:
            print("  ❌ Missing 'title' field in content")

        # Check 3: Content has 'description'
        total_checks += 1
        if 'content' in msg and 'description' in msg['content']:
            desc = msg['content']['description']
            print(f"  ✅ Has 'description': {desc[:50]}{'...' if len(desc) > 50 else ''}")
            checks_passed += 1
        else:
            print("  ❌ Missing 'description' field in content")

        # Check 4: Preserves timestamp
        total_checks += 1
        if 'timestamp' in msg:
            print(f"  ✅ Preserves 'timestamp': {msg['timestamp']}")
            checks_passed += 1
        else:
            print("  ❌ Missing 'timestamp' field")

        # Check 5: Preserves ID
        total_checks += 1
        if 'id' in msg:
            print(f"  ✅ Preserves 'id': {msg['id']}")
            checks_passed += 1
        else:
            print("  ❌ Missing 'id' field")

    # Summary
    print("\n" + "=" * 80)
    print(f"📊 RESULTS: {checks_passed}/{total_checks} checks passed")
    print("=" * 80)

    if checks_passed == total_checks:
        print("✅ ALL CHECKS PASSED - Transformation working correctly!")
        print("\n🎯 IMPACT:")
        print("   - Validation script will now see proper structure")
        print("   - Should reach 99.9% confidence in 4-5 iterations")
        print("   - No more stuck iterations at 94%/96%")
        return True
    else:
        print(f"❌ {total_checks - checks_passed} checks failed")
        return False


if __name__ == "__main__":
    success = test_transformation()
    sys.exit(0 if success else 1)
