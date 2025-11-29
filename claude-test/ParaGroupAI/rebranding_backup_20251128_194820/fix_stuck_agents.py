#!/usr/bin/env python3
"""
fix_stuck_agents.py - Clean up stuck and orphaned agents

PRODUCTION-READY FIX (2025-11-21)
==================================

PURPOSE:
- Clear all stuck "running" agents that have been running for > 1 hour
- Clear all completed agents
- Reset agent tracking to clean state
- Prevent accumulation of zombie agents

USAGE:
    python3 fix_stuck_agents.py
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def fix_stuck_agents():
    """Clean up stuck and completed agents."""

    db_path = Path("/home/user01/claude-test/ClaudePrompt/tmp/agent_activity.json")

    if not db_path.exists():
        print("✅ No agent database found - nothing to clean")
        return

    # Load database
    with open(db_path, 'r') as f:
        db = json.load(f)

    agents = db.get('agents', [])
    original_count = len(agents)

    print(f"📊 Original agent count: {original_count}")

    # Categorize agents
    completed_agents = [a for a in agents if a.get('status') == 'completed']
    running_agents = [a for a in agents if a.get('status') == 'running']
    pending_agents = [a for a in agents if a.get('status') == 'pending']

    print(f"   Completed: {len(completed_agents)}")
    print(f"   Running: {len(running_agents)}")
    print(f"   Pending: {len(pending_agents)}")

    # Check for stuck running agents (running > 1 hour)
    stuck_threshold = datetime.now() - timedelta(hours=1)
    stuck_agents = []
    valid_running_agents = []

    for agent in running_agents:
        start_time_str = agent.get('start_time')
        if start_time_str:
            try:
                start_time = datetime.fromisoformat(start_time_str)
                if start_time < stuck_threshold:
                    stuck_agents.append(agent)
                else:
                    valid_running_agents.append(agent)
            except:
                # Invalid timestamp - consider stuck
                stuck_agents.append(agent)
        else:
            # No timestamp - consider stuck
            stuck_agents.append(agent)

    print(f"\n🔍 Analysis:")
    print(f"   Stuck agents (running > 1 hour): {len(stuck_agents)}")
    print(f"   Valid running agents: {len(valid_running_agents)}")

    # Strategy: Keep only valid running agents and recent pending agents
    agents_to_keep = valid_running_agents + pending_agents

    print(f"\n🧹 Cleanup Plan:")
    print(f"   Removing {len(completed_agents)} completed agents")
    print(f"   Removing {len(stuck_agents)} stuck running agents")
    print(f"   Keeping {len(agents_to_keep)} active agents")

    # Update database
    db['agents'] = agents_to_keep
    db['last_clear'] = datetime.now().isoformat()

    # Save
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)

    new_count = len(agents_to_keep)
    removed_count = original_count - new_count

    print(f"\n✅ Cleanup Complete!")
    print(f"   Original: {original_count} agents")
    print(f"   Removed: {removed_count} agents")
    print(f"   Remaining: {new_count} agents")

    if stuck_agents:
        print(f"\n📋 Stuck Agents Removed:")
        for agent in stuck_agents[:10]:  # Show first 10
            agent_id = agent.get('id', 'unknown')
            tool = agent.get('tool', 'None')
            start_time = agent.get('start_time', 'unknown')
            print(f"   Agent #{agent_id}: {tool} (started: {start_time})")

        if len(stuck_agents) > 10:
            print(f"   ... and {len(stuck_agents) - 10} more")

    return removed_count, new_count

if __name__ == '__main__':
    try:
        removed, remaining = fix_stuck_agents()
        print(f"\n🎉 Success! Cleaned up {removed} agents, {remaining} remain active.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
