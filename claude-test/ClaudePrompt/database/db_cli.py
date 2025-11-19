#!/usr/bin/env python3
"""
Database-First CLI Monitoring Tool

Provides CLI commands for monitoring and managing database-first context system.

Commands:
  db-status      - Show system status and overview
  db-projects    - List all projects
  db-instances   - List all active instances
  db-context     - View context snapshots
  db-inspect     - Inspect specific project/instance details

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import sys
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class DBCli:
    """CLI tool for database-first context management."""

    def __init__(self, db_path: str = None):
        """Initialize CLI with database path."""
        if db_path is None:
            # Default to ClaudePrompt database
            self.db_path = Path(__file__).parent / "ultrathink_context.db"
        else:
            self.db_path = Path(db_path)

        if not self.db_path.exists():
            print(f"❌ Database not found: {self.db_path}")
            print(f"   Run './deploy_db_first.sh' to initialize the database")
            sys.exit(1)

    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def cmd_status(self):
        """Show system status and overview."""
        conn = self._get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print("📊 DATABASE-FIRST CONTEXT MANAGEMENT - SYSTEM STATUS")
        print("=" * 80 + "\n")

        # Database info
        print(f"📁 Database: {self.db_path}")
        print(f"   Size: {self.db_path.stat().st_size:,} bytes")
        print()

        # Projects
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total_story_points), SUM(completed_story_points) FROM projects")
        row = cursor.fetchone()
        total_points = row[0] or 0
        completed_points = row[1] or 0

        print(f"📦 Projects: {project_count}")
        print(f"   Total story points: {total_points:,}")
        print(f"   Completed story points: {completed_points:,}")
        if total_points > 0:
            completion = (completed_points / total_points) * 100
            print(f"   Overall completion: {completion:.1f}%")
        print()

        # Instances
        cursor.execute("SELECT COUNT(*) FROM active_instances WHERE status = 'active'")
        active_instances = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM active_instances")
        total_instances = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(current_token_usage) FROM active_instances WHERE status = 'active'")
        total_tokens = cursor.fetchone()[0] or 0

        print(f"🚀 Instances: {active_instances} active / {total_instances} total")
        print(f"   Total token usage: {total_tokens:,} / 200,000")
        if active_instances > 0:
            avg_tokens = total_tokens / active_instances
            print(f"   Average per instance: {avg_tokens:,.0f} tokens")
        print()

        # Context snapshots
        cursor.execute("SELECT COUNT(*) FROM context_snapshots")
        snapshot_count = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(token_count) FROM context_snapshots")
        total_context_tokens = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT priority, COUNT(*) as count
            FROM context_snapshots
            GROUP BY priority
            ORDER BY
                CASE priority
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'LOW' THEN 4
                END
        """)
        priority_counts = {row['priority']: row['count'] for row in cursor.fetchall()}

        print(f"💾 Context Snapshots: {snapshot_count:,}")
        print(f"   Total tokens stored: {total_context_tokens:,}")
        print(f"   By priority:")
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = priority_counts.get(priority, 0)
            if count > 0:
                print(f"     - {priority}: {count:,}")
        print()

        # Recent activity
        cursor.execute("""
            SELECT project_id, name, updated_at
            FROM projects
            ORDER BY updated_at DESC
            LIMIT 5
        """)
        recent_projects = cursor.fetchall()

        if recent_projects:
            print(f"📅 Recent Projects:")
            for row in recent_projects:
                print(f"   • {row['name']} ({row['project_id']})")
                print(f"     Updated: {row['updated_at']}")

        conn.close()
        print("\n" + "=" * 80 + "\n")

    def cmd_projects(self, verbose: bool = False):
        """List all projects."""
        conn = self._get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print("📦 PROJECTS")
        print("=" * 80 + "\n")

        cursor.execute("""
            SELECT * FROM v_project_summary
            ORDER BY created_at DESC
        """)
        projects = cursor.fetchall()

        if not projects:
            print("No projects found.")
            print("\nTo create a project:")
            print("  python3 -c \"from database.multi_project_manager import MultiProjectManager;")
            print("            m = MultiProjectManager();")
            print("            m.create_project('My Project', 'Description', 1300)\"")
        else:
            for row in projects:
                print(f"📁 {row['name']}")
                print(f"   ID: {row['project_id']}")
                print(f"   Story Points: {row['completed_story_points']} / {row['total_story_points']}")
                if row['total_story_points'] > 0:
                    completion = (row['completed_story_points'] / row['total_story_points']) * 100
                    print(f"   Completion: {completion:.1f}%")
                print(f"   Active Instances: {row['active_instances']}")
                print(f"   Context Snapshots: {row['total_snapshots']}")
                total_tokens = row['total_tokens'] if row['total_tokens'] is not None else 0
                print(f"   Total Tokens: {total_tokens:,}")
                print(f"   Created: {row['created_at']}")

                if verbose:
                    # Show instances
                    cursor.execute("""
                        SELECT instance_id, status, started_at, current_token_usage
                        FROM active_instances
                        WHERE project_id = ?
                        ORDER BY started_at DESC
                    """, (row['project_id'],))
                    instances = cursor.fetchall()

                    if instances:
                        print(f"   Instances:")
                        for inst in instances:
                            status_emoji = "🟢" if inst['status'] == 'active' else "🔴"
                            print(f"     {status_emoji} {inst['instance_id']}")
                            print(f"        Status: {inst['status']}")
                            print(f"        Tokens: {inst['current_token_usage']:,}")
                            print(f"        Started: {inst['started_at']}")

                print()

        conn.close()
        print("=" * 80 + "\n")

    def cmd_instances(self, project_id: Optional[str] = None):
        """List all active instances."""
        conn = self._get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print("🚀 ACTIVE INSTANCES")
        print("=" * 80 + "\n")

        if project_id:
            cursor.execute("""
                SELECT ai.*, p.name as project_name
                FROM active_instances ai
                JOIN projects p ON ai.project_id = p.project_id
                WHERE ai.project_id = ?
                ORDER BY ai.started_at DESC
            """, (project_id,))
        else:
            cursor.execute("""
                SELECT ai.*, p.name as project_name
                FROM active_instances ai
                JOIN projects p ON ai.project_id = p.project_id
                ORDER BY ai.started_at DESC
            """)

        instances = cursor.fetchall()

        if not instances:
            if project_id:
                print(f"No instances found for project: {project_id}")
            else:
                print("No instances found.")
            print("\nTo launch an instance:")
            print("  python3 -c \"from database.multi_project_manager import MultiProjectManager;")
            print("            m = MultiProjectManager();")
            print("            m.launch_instance('project_id')\"")
        else:
            for row in instances:
                status_emoji = {
                    'active': '🟢',
                    'idle': '🟡',
                    'crashed': '🔴',
                    'completed': '✅'
                }.get(row['status'], '⚪')

                print(f"{status_emoji} {row['instance_id']}")
                print(f"   Project: {row['project_name']} ({row['project_id']})")
                print(f"   Status: {row['status']}")
                print(f"   Tokens: {row['current_token_usage']:,} / 200,000 ({row['current_token_usage']/2000:.1f}%)")
                print(f"   Hostname: {row['hostname']}")
                print(f"   Process ID: {row['process_id']}")
                print(f"   Started: {row['started_at']}")
                print(f"   Last Heartbeat: {row['last_heartbeat']}")

                # Calculate uptime
                try:
                    started = datetime.fromisoformat(row['started_at'])
                    now = datetime.now()
                    uptime = now - started
                    hours = uptime.total_seconds() / 3600
                    print(f"   Uptime: {hours:.1f} hours")
                except:
                    pass

                print()

        conn.close()
        print("=" * 80 + "\n")

    def cmd_context(self, project_id: Optional[str] = None, priority: Optional[str] = None, limit: int = 20):
        """View context snapshots."""
        conn = self._get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print("💾 CONTEXT SNAPSHOTS")
        print("=" * 80 + "\n")

        query = """
            SELECT cs.*, p.name as project_name
            FROM context_snapshots cs
            JOIN projects p ON cs.project_id = p.project_id
            WHERE 1=1
        """
        params = []

        if project_id:
            query += " AND cs.project_id = ?"
            params.append(project_id)

        if priority:
            query += " AND cs.priority = ?"
            params.append(priority.upper())

        query += " ORDER BY cs.created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        snapshots = cursor.fetchall()

        if not snapshots:
            print("No context snapshots found.")
        else:
            for row in snapshots:
                priority_emoji = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(row['priority'], '⚪')

                print(f"{priority_emoji} Snapshot #{row['snapshot_id']} - {row['priority']}")
                print(f"   Project: {row['project_name']} ({row['project_id']})")
                print(f"   Type: {row['content_type']}")
                print(f"   Tokens: {row['token_count']:,}")
                print(f"   Sequence: {row['sequence_number']}")
                print(f"   Created: {row['created_at']}")

                # Show content preview (first 100 chars)
                try:
                    content = json.loads(row['content'])
                    content_str = json.dumps(content, indent=2)
                    if len(content_str) > 100:
                        preview = content_str[:100] + "..."
                    else:
                        preview = content_str
                    print(f"   Preview: {preview}")
                except:
                    pass

                print()

        conn.close()
        print("=" * 80 + "\n")

    def cmd_inspect(self, identifier: str):
        """Inspect specific project or instance details."""
        conn = self._get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 80)
        print(f"🔍 INSPECTING: {identifier}")
        print("=" * 80 + "\n")

        # Try as project ID
        cursor.execute("SELECT * FROM projects WHERE project_id = ?", (identifier,))
        project = cursor.fetchone()

        if project:
            print("📦 PROJECT DETAILS")
            print(f"   Name: {project['name']}")
            print(f"   ID: {project['project_id']}")
            print(f"   Description: {project['description']}")
            print(f"   Story Points: {project['completed_story_points']} / {project['total_story_points']}")
            print(f"   Total Phases: {project['total_phases']}")
            print(f"   Created: {project['created_at']}")
            print(f"   Updated: {project['updated_at']}")
            print()

            # Show phases
            cursor.execute("""
                SELECT * FROM phases
                WHERE project_id = ?
                ORDER BY phase_number
            """, (identifier,))
            phases = cursor.fetchall()

            if phases:
                print("   PHASES:")
                for phase in phases:
                    status_emoji = {
                        'pending': '⏳',
                        'in_progress': '🔄',
                        'completed': '✅',
                        'blocked': '🚫'
                    }.get(phase['status'], '⚪')
                    print(f"     {status_emoji} Phase {phase['phase_number']}: {phase['name']}")
                    print(f"        Story Points: {phase['story_points']}")
                    print(f"        Status: {phase['status']}")
                print()

            # Show instances
            cursor.execute("""
                SELECT * FROM active_instances
                WHERE project_id = ?
                ORDER BY started_at DESC
            """, (identifier,))
            instances = cursor.fetchall()

            if instances:
                print(f"   INSTANCES: {len(instances)}")
                for inst in instances:
                    status_emoji = "🟢" if inst['status'] == 'active' else "🔴"
                    print(f"     {status_emoji} {inst['instance_id']}")
                    print(f"        Status: {inst['status']}")
                    print(f"        Tokens: {inst['current_token_usage']:,}")
                print()

            # Show context snapshots
            cursor.execute("""
                SELECT priority, COUNT(*) as count, SUM(token_count) as total_tokens
                FROM context_snapshots
                WHERE project_id = ?
                GROUP BY priority
            """, (identifier,))
            snapshots = cursor.fetchall()

            if snapshots:
                print("   CONTEXT SNAPSHOTS:")
                for snap in snapshots:
                    print(f"     {snap['priority']}: {snap['count']} snapshots, {snap['total_tokens']:,} tokens")
        else:
            # Try as instance ID
            cursor.execute("""
                SELECT ai.*, p.name as project_name
                FROM active_instances ai
                JOIN projects p ON ai.project_id = p.project_id
                WHERE ai.instance_id = ?
            """, (identifier,))
            instance = cursor.fetchone()

            if instance:
                print("🚀 INSTANCE DETAILS")
                print(f"   ID: {instance['instance_id']}")
                print(f"   Project: {instance['project_name']} ({instance['project_id']})")
                print(f"   Status: {instance['status']}")
                print(f"   Tokens: {instance['current_token_usage']:,} / 200,000")
                print(f"   Hostname: {instance['hostname']}")
                print(f"   Process ID: {instance['process_id']}")
                print(f"   Started: {instance['started_at']}")
                print(f"   Last Heartbeat: {instance['last_heartbeat']}")

                # Show context available to this instance
                cursor.execute("""
                    SELECT priority, COUNT(*) as count, SUM(token_count) as total_tokens
                    FROM context_snapshots
                    WHERE project_id = ?
                    GROUP BY priority
                """, (instance['project_id'],))
                snapshots = cursor.fetchall()

                if snapshots:
                    print()
                    print("   AVAILABLE CONTEXT:")
                    for snap in snapshots:
                        print(f"     {snap['priority']}: {snap['count']} snapshots, {snap['total_tokens']:,} tokens")
            else:
                print(f"❌ Not found: {identifier}")
                print("   Try 'db-projects' or 'db-instances' to see available IDs")

        conn.close()
        print("\n" + "=" * 80 + "\n")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: db-cli <command> [options]")
        print()
        print("Commands:")
        print("  status              Show system status and overview")
        print("  projects            List all projects")
        print("  projects -v         List all projects with instances")
        print("  instances           List all active instances")
        print("  instances <proj>    List instances for specific project")
        print("  context             View recent context snapshots")
        print("  context <proj>      View context for specific project")
        print("  context -p HIGH     View context with specific priority")
        print("  inspect <id>        Inspect specific project/instance")
        print()
        print("Examples:")
        print("  db-cli status")
        print("  db-cli projects -v")
        print("  db-cli instances proj_20251119_153441_e8628e6f")
        print("  db-cli context -p CRITICAL")
        print("  db-cli inspect proj_20251119_153441_e8628e6f")
        sys.exit(1)

    command = sys.argv[1]
    cli = DBCli()

    if command == "status":
        cli.cmd_status()
    elif command == "projects":
        verbose = "-v" in sys.argv or "--verbose" in sys.argv
        cli.cmd_projects(verbose=verbose)
    elif command == "instances":
        project_id = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else None
        cli.cmd_instances(project_id=project_id)
    elif command == "context":
        project_id = None
        priority = None
        limit = 20

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "-p" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "-l" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            elif not sys.argv[i].startswith("-"):
                project_id = sys.argv[i]
                i += 1
            else:
                i += 1

        cli.cmd_context(project_id=project_id, priority=priority, limit=limit)
    elif command == "inspect":
        if len(sys.argv) < 3:
            print("❌ Error: inspect requires an ID")
            print("Usage: db-cli inspect <project_id|instance_id>")
            sys.exit(1)
        cli.cmd_inspect(sys.argv[2])
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'db-cli' to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()
