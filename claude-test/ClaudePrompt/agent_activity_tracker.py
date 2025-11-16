#!/usr/bin/env python3
"""
agent_activity_tracker.py - Comprehensive Agent Activity Tracking System

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Track EVERY agent (tool call) with full details
- Provide visibility into what each agent is doing
- Auto-clear completed agents after idle period
- Persist background agents
- Enable 'view-agents' command

FEATURES:
- ✅ Per-agent tracking (tool name, params, status, timing)
- ✅ Agent lifecycle management (pending → running → completed → cleared)
- ✅ Background agent detection and persistence
- ✅ Auto-clearing of stale completed agents
- ✅ JSON-based agent database
- ✅ CLI command for viewing agent details

FIXES:
1. Agent counter never decreases - NOW HAS AUTO-CLEAR LOGIC
2. No visibility into agents - NOW HAS VIEW COMMAND
3. Can't see agent status - NOW TRACKS LIFECYCLE
4. Background agents not persisted - NOW DETECTED AND KEPT

USAGE:
    # Track new agent
    python3 agent_activity_tracker.py --add --tool Read --params '{"file_path":"/path/to/file"}'

    # View all agents
    python3 agent_activity_tracker.py --view

    # View active agents only
    python3 agent_activity_tracker.py --view --active

    # Clear completed agents
    python3 agent_activity_tracker.py --clear-completed

    # Get agent count
    python3 agent_activity_tracker.py --count
"""

import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class AgentActivityTracker:
    """
    Comprehensive agent tracking with lifecycle management.
    """

    def __init__(self, db_path: Optional[str] = None):
        """Initialize tracker."""
        if db_path is None:
            db_path = "/home/user01/claude-test/ClaudePrompt/tmp/agent_activity.json"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Agent counter file (for backward compatibility)
        self.counter_file = self.db_path.parent / "agent_usage_counter.txt"

        # Auto-clear settings
        self.auto_clear_after_seconds = 300  # 5 minutes
        self.background_task_indicators = [
            'sleep', 'npm', 'node', 'tail -f', 'watch',
            'serve', 'dev', 'background', 'pending'
        ]

    def load_agents(self) -> Dict:
        """Load agent database."""
        if not self.db_path.exists():
            return {
                'agents': [],
                'next_id': 1,
                'last_clear': datetime.now().isoformat()
            }

        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return {
                'agents': [],
                'next_id': 1,
                'last_clear': datetime.now().isoformat()
            }

    def save_agents(self, db: Dict):
        """Save agent database."""
        with open(self.db_path, 'w') as f:
            json.dump(db, f, indent=2)

        # Update counter file for backward compatibility
        active_count = len([a for a in db['agents'] if a['status'] in ['pending', 'running']])
        self.counter_file.write_text(str(active_count))

    def add_agent(self, tool_name: str, params: Optional[Dict] = None,
                  metadata: Optional[Dict] = None) -> int:
        """
        Add new agent to tracking database.

        Args:
            tool_name: Name of the tool being executed
            params: Tool parameters
            metadata: Additional metadata

        Returns:
            Agent ID
        """
        db = self.load_agents()

        agent_id = db['next_id']
        db['next_id'] += 1

        agent = {
            'id': agent_id,
            'tool_name': tool_name,
            'params': params or {},
            'metadata': metadata or {},
            'status': 'running',  # pending → running → completed → cleared
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'completed_at': None,
            'duration_seconds': None,
            'is_background': self._is_background_task(tool_name, params),
            'result_summary': None,
            'error': None
        }

        db['agents'].append(agent)
        self.save_agents(db)

        return agent_id

    def update_agent_status(self, agent_id: int, status: str,
                           result_summary: Optional[str] = None,
                           error: Optional[str] = None):
        """Update agent status."""
        db = self.load_agents()

        for agent in db['agents']:
            if agent['id'] == agent_id:
                agent['status'] = status
                agent['updated_at'] = datetime.now().isoformat()

                if status == 'completed':
                    agent['completed_at'] = datetime.now().isoformat()

                    # Calculate duration
                    created = datetime.fromisoformat(agent['created_at'])
                    completed = datetime.fromisoformat(agent['completed_at'])
                    agent['duration_seconds'] = (completed - created).total_seconds()

                if result_summary:
                    agent['result_summary'] = result_summary

                if error:
                    agent['error'] = error

                break

        self.save_agents(db)

    def _is_background_task(self, tool_name: str, params: Optional[Dict]) -> bool:
        """Detect if this is a background task."""
        if tool_name == 'Bash':
            command = params.get('command', '') if params else ''
            return any(indicator in command.lower() for indicator in self.background_task_indicators)

        return False

    def get_active_agents(self) -> List[Dict]:
        """Get all active (pending or running) agents."""
        db = self.load_agents()
        return [a for a in db['agents'] if a['status'] in ['pending', 'running']]

    def get_all_agents(self) -> List[Dict]:
        """Get all agents."""
        db = self.load_agents()
        return db['agents']

    def auto_clear_completed(self) -> int:
        """
        Auto-clear completed agents that are older than threshold.

        Background agents are NEVER cleared automatically.

        Returns:
            Number of agents cleared
        """
        db = self.load_agents()
        now = datetime.now()
        cleared_count = 0

        new_agents = []
        for agent in db['agents']:
            # Keep if active
            if agent['status'] in ['pending', 'running']:
                new_agents.append(agent)
                continue

            # Keep if background task (never auto-clear background)
            if agent.get('is_background', False):
                new_agents.append(agent)
                continue

            # Clear if completed and old enough
            if agent['status'] == 'completed' and agent['completed_at']:
                completed_time = datetime.fromisoformat(agent['completed_at'])
                age_seconds = (now - completed_time).total_seconds()

                if age_seconds > self.auto_clear_after_seconds:
                    # Don't add to new_agents (effectively clearing it)
                    cleared_count += 1
                else:
                    new_agents.append(agent)
            else:
                new_agents.append(agent)

        if cleared_count > 0:
            db['agents'] = new_agents
            db['last_clear'] = now.isoformat()
            self.save_agents(db)

        return cleared_count

    def clear_all_completed(self) -> int:
        """
        Manually clear ALL completed agents (except background).

        Returns:
            Number of agents cleared
        """
        db = self.load_agents()
        original_count = len(db['agents'])

        # Keep only active agents and background agents
        db['agents'] = [
            a for a in db['agents']
            if a['status'] in ['pending', 'running'] or a.get('is_background', False)
        ]

        cleared_count = original_count - len(db['agents'])

        if cleared_count > 0:
            db['last_clear'] = datetime.now().isoformat()
            self.save_agents(db)

        return cleared_count

    def get_agent_count(self) -> Dict[str, int]:
        """Get agent counts by status."""
        db = self.load_agents()

        counts = {
            'total': len(db['agents']),
            'pending': 0,
            'running': 0,
            'completed': 0,
            'background': 0,
            'active': 0
        }

        for agent in db['agents']:
            status = agent['status']
            if status == 'pending':
                counts['pending'] += 1
            elif status == 'running':
                counts['running'] += 1
            elif status == 'completed':
                counts['completed'] += 1

            if agent.get('is_background', False):
                counts['background'] += 1

            if status in ['pending', 'running']:
                counts['active'] += 1

        return counts

    def format_agent_display(self, agent: Dict, verbose: bool = False) -> str:
        """Format agent for display."""
        status_emoji = {
            'pending': '⏳',
            'running': '▶️',
            'completed': '✅',
            'error': '❌'
        }

        emoji = status_emoji.get(agent['status'], '❓')
        bg_marker = ' 🔄' if agent.get('is_background', False) else ''

        # Duration
        if agent.get('duration_seconds'):
            duration = f"{agent['duration_seconds']:.2f}s"
        else:
            created = datetime.fromisoformat(agent['created_at'])
            now = datetime.now()
            duration = f"{(now - created).total_seconds():.2f}s (ongoing)"

        # Basic display
        display = f"{emoji} Agent #{agent['id']}: {agent['tool_name']}{bg_marker} [{agent['status']}] ({duration})"

        if verbose:
            display += f"\n  Created: {agent['created_at']}"
            display += f"\n  Updated: {agent['updated_at']}"

            if agent.get('params'):
                params_str = json.dumps(agent['params'], indent=4)
                display += f"\n  Params: {params_str}"

            if agent.get('result_summary'):
                display += f"\n  Result: {agent['result_summary']}"

            if agent.get('error'):
                display += f"\n  Error: {agent['error']}"

        return display


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Agent Activity Tracker')
    parser.add_argument('--add', action='store_true', help='Add new agent')
    parser.add_argument('--tool', help='Tool name (for --add)')
    parser.add_argument('--params', help='Tool params as JSON (for --add)')
    parser.add_argument('--update', type=int, metavar='AGENT_ID', help='Update agent status')
    parser.add_argument('--status', help='New status (for --update)')
    parser.add_argument('--result', help='Result summary (for --update)')
    parser.add_argument('--view', action='store_true', help='View agents')
    parser.add_argument('--active', action='store_true', help='Show only active agents (with --view)')
    parser.add_argument('--verbose', action='store_true', help='Verbose output (with --view)')
    parser.add_argument('--count', action='store_true', help='Show agent counts')
    parser.add_argument('--clear-completed', action='store_true', help='Clear completed agents')
    parser.add_argument('--auto-clear', action='store_true', help='Auto-clear old completed agents')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    tracker = AgentActivityTracker()

    if args.add:
        if not args.tool:
            print("Error: --tool required with --add")
            return 1

        params = json.loads(args.params) if args.params else {}
        agent_id = tracker.add_agent(args.tool, params)

        if args.json:
            print(json.dumps({'agent_id': agent_id}))
        else:
            print(f"✅ Agent #{agent_id} added: {args.tool}")

    elif args.update:
        if not args.status:
            print("Error: --status required with --update")
            return 1

        tracker.update_agent_status(args.update, args.status, result_summary=args.result)

        if not args.json:
            print(f"✅ Agent #{args.update} updated: {args.status}")

    elif args.view:
        if args.active:
            agents = tracker.get_active_agents()
        else:
            agents = tracker.get_all_agents()

        if args.json:
            print(json.dumps(agents, indent=2))
        else:
            if not agents:
                print("No agents found.")
            else:
                print(f"{'Active ' if args.active else ''}Agents ({len(agents)} total):\n")
                for agent in agents:
                    print(tracker.format_agent_display(agent, verbose=args.verbose))
                    print()

    elif args.count:
        counts = tracker.get_agent_count()

        if args.json:
            print(json.dumps(counts))
        else:
            print(f"Agent Counts:")
            print(f"  Total: {counts['total']}")
            print(f"  Active: {counts['active']} (Pending: {counts['pending']}, Running: {counts['running']})")
            print(f"  Completed: {counts['completed']}")
            print(f"  Background: {counts['background']}")

    elif args.clear_completed:
        cleared = tracker.clear_all_completed()

        if not args.json:
            print(f"✅ Cleared {cleared} completed agents")

    elif args.auto_clear:
        cleared = tracker.auto_clear_completed()

        if not args.json:
            if cleared > 0:
                print(f"✅ Auto-cleared {cleared} old completed agents")
            else:
                print("No agents to clear")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
