#!/usr/bin/env python3
"""
Example: Integrate database-first context management with ULTRATHINK.

This shows how to use the database-first architecture in your code.
"""

import sys
sys.path.insert(0, '/home/user01/claude-test/ClaudePrompt/database')

from sqlite_context_loader import SQLiteContextLoader
from multi_project_manager import MultiProjectManager
from token_manager import TokenManager


def main():
    """Example integration."""
    print("\n" + "=" * 80)
    print("DATABASE-FIRST CONTEXT MANAGEMENT - INTEGRATION EXAMPLE")
    print("=" * 80 + "\n")

    # Create managers
    manager = MultiProjectManager("ultrathink_context.db")
    token_mgr = TokenManager("ultrathink_context.db")

    # Example 1: Create a project
    print("1. Creating a project...")
    project_id = manager.create_project(
        name="Example Integration Project",
        description="Demonstrating database-first context management",
        total_story_points=1300
    )
    print(f"   ✅ Project created: {project_id}\n")

    # Example 2: Launch instances
    print("2. Launching instances...")
    instances = []
    for i in range(1, 4):
        instance_id = manager.launch_instance(project_id, phase_id=None)
        instances.append(instance_id)
        print(f"   ✅ Instance {i}: {instance_id}")

    print(f"\n   Total: {len(instances)} instances for project {project_id}\n")

    # Example 3: Store context
    print("3. Storing context...")
    snapshot_id = manager.store_context(
        project_id=project_id,
        content={"message": "Example context snapshot", "step": "integration_test"},
        priority="HIGH",
        content_type="code"
    )
    print(f"   ✅ Context snapshot stored: ID {snapshot_id}\n")

    # Example 4: Check token usage
    print("4. Checking token usage...")
    for instance_id in instances:
        usage = token_mgr.check_token_usage(instance_id)
        if usage:
            print(f"   Instance {instance_id}: {usage['current_token_usage']:,} tokens ({usage['percentage']:.1f}%)")
    print()

    # Example 5: Get project summary
    print("5. Project summary:")
    summaries = manager.get_project_summary()
    for summary in summaries:
        print(f"   • {summary['name']}: {summary['active_instances']} instances, {summary['total_snapshots']} snapshots")

    print("\n" + "=" * 80)
    print("✅ INTEGRATION EXAMPLE COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")

    manager.close()
    token_mgr.close()


if __name__ == "__main__":
    main()
