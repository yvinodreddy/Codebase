#!/usr/bin/env python3
"""
Automatic Context Integration for cpp/cpps Commands

This module provides automatic integration of database-first context management
with cpp/cpps commands. It handles:
- Auto project detection/creation based on working directory
- Auto instance assignment
- Auto context storage after commands

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import os
import sys
import socket
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import json

# Add database directory to path
sys.path.insert(0, str(Path(__file__).parent))

from multi_project_manager import MultiProjectManager


class AutoContextIntegration:
    """Automatic context integration for ULTRATHINK commands."""

    def __init__(self, db_path: str = None):
        """Initialize auto context integration."""
        if db_path is None:
            self.db_path = Path(__file__).parent / "ultrathink_context.db"
        else:
            self.db_path = Path(db_path)

        self.manager = MultiProjectManager(str(self.db_path))
        self.session_file = Path.home() / ".ultrathink" / "current_session.json"
        self.session_file.parent.mkdir(parents=True, exist_ok=True)

    def get_or_create_project(self) -> Tuple[str, bool]:
        """
        Get or create project based on current working directory.

        Returns:
            Tuple of (project_id, is_new)
        """
        # Use working directory as project identifier
        cwd = Path.cwd()
        project_name = cwd.name or "root"

        # STEP 1: Check if we have an existing mapping for this directory
        # This handles backward compatibility with timestamp-based project IDs
        mapping_file = Path.home() / ".ultrathink" / "project_mappings.json"
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r') as f:
                    mappings = json.load(f)
                    if str(cwd) in mappings:
                        existing_project_id = mappings[str(cwd)]
                        # Verify this project still exists in database
                        projects = self.manager.get_all_projects()
                        if any(p['project_id'] == existing_project_id for p in projects):
                            return existing_project_id, False
            except:
                pass  # Continue with normal flow if mapping file is corrupted

        # STEP 2: Create deterministic project ID based on directory path
        # This ensures the same directory always gets the same project ID
        path_hash = hashlib.md5(str(cwd).encode()).hexdigest()[:8]
        deterministic_project_id = f"proj_{project_name}_{path_hash}"

        # STEP 3: Check if deterministic project exists in database
        projects = self.manager.get_all_projects()
        existing = next((p for p in projects if p['project_id'] == deterministic_project_id), None)

        if existing:
            # Save mapping for faster lookup next time
            self._save_project_mapping(str(cwd), deterministic_project_id)
            return deterministic_project_id, False

        # STEP 4: Create new project with deterministic ID
        # Pass the deterministic ID to create_project() so it uses our ID instead of generating one
        actual_project_id = self.manager.create_project(
            name=f"{project_name} (Auto)",
            description=f"Auto-created project for directory: {cwd}",
            total_story_points=1300,
            project_id=deterministic_project_id  # Use deterministic ID
        )

        # Store mapping for this directory
        self._save_project_mapping(str(cwd), actual_project_id)

        return actual_project_id, True

    def get_or_create_instance(self, project_id: str, phase_id: Optional[int] = None) -> Tuple[str, bool]:
        """
        Get or create instance for current session.

        Returns:
            Tuple of (instance_id, is_new)
        """
        # Check for existing session
        session = self._load_session()

        if session and session.get('project_id') == project_id:
            # Reuse existing instance from this session
            instance_id = session.get('instance_id')
            if instance_id:
                # Verify instance still exists and is active
                instances = self.manager.get_project_instances(project_id)
                if any(i['instance_id'] == instance_id and i['status'] == 'active' for i in instances):
                    return instance_id, False

        # Create new instance
        instance_id = self.manager.launch_instance(project_id, phase_id)

        # Save session
        self._save_session({
            'project_id': project_id,
            'instance_id': instance_id,
            'started_at': datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'process_id': os.getpid(),
            'working_directory': str(Path.cwd())
        })

        return instance_id, True

    def store_command_context(
        self,
        project_id: str,
        prompt: str,
        output: Optional[str] = None,
        priority: str = 'HIGH',
        phase_id: Optional[int] = None
    ) -> int:
        """
        Store context from a command execution.

        Args:
            project_id: Project identifier
            prompt: The prompt that was executed
            output: The output from the command (optional)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            phase_id: Optional phase identifier

        Returns:
            snapshot_id of created snapshot
        """
        content = {
            'prompt': prompt,
            'timestamp': datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'working_directory': str(Path.cwd())
        }

        if output:
            content['output'] = output

        return self.manager.store_context(
            project_id=project_id,
            content=content,
            priority=priority,
            content_type='decision',  # Using 'decision' for command execution context
            phase_id=phase_id
        )

    def update_instance_tokens(self, instance_id: str, token_count: int) -> bool:
        """
        Update token usage for an instance.

        Args:
            instance_id: Instance identifier
            token_count: Current token count

        Returns:
            True if successful
        """
        try:
            conn = self.manager.loader._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE active_instances
                SET current_token_usage = ?,
                    last_heartbeat = datetime('now')
                WHERE instance_id = ?
            """, (token_count, instance_id))

            conn.commit()
            return True
        except Exception as e:
            print(f"Warning: Failed to update instance tokens: {e}")
            return False

    def get_current_session(self) -> Optional[Dict]:
        """Get current session information."""
        return self._load_session()

    def end_session(self):
        """End current session and mark instance as completed."""
        session = self._load_session()
        if session:
            instance_id = session.get('instance_id')
            if instance_id:
                try:
                    conn = self.manager.loader._get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE active_instances
                        SET status = 'completed'
                        WHERE instance_id = ?
                    """, (instance_id,))

                    conn.commit()
                except Exception as e:
                    print(f"Warning: Failed to end session: {e}")

            # Clear session file
            if self.session_file.exists():
                self.session_file.unlink()

    def _load_session(self) -> Optional[Dict]:
        """Load current session from file."""
        if not self.session_file.exists():
            return None

        try:
            with open(self.session_file, 'r') as f:
                return json.load(f)
        except:
            return None

    def _save_session(self, session: Dict):
        """Save session to file."""
        with open(self.session_file, 'w') as f:
            json.dump(session, f, indent=2)

    def _save_project_mapping(self, directory: str, project_id: str):
        """Save directory to project ID mapping."""
        mapping_file = Path.home() / ".ultrathink" / "project_mappings.json"

        mappings = {}
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r') as f:
                    mappings = json.load(f)
            except:
                pass

        mappings[directory] = project_id

        with open(mapping_file, 'w') as f:
            json.dump(mappings, f, indent=2)

    def close(self):
        """Close manager and connections."""
        self.manager.close()


def initialize_for_command(prompt: str, manual_project_id: Optional[str] = None) -> Tuple[str, str, bool, bool]:
    """
    Initialize database-first context for a command.

    This is called automatically before each cpp/cpps command.

    Args:
        prompt: The prompt being executed
        manual_project_id: Optional manual project ID to use instead of auto-detection

    Returns:
        Tuple of (project_id, instance_id, project_created, instance_created)
    """
    integration = AutoContextIntegration()

    # Get or create project
    if manual_project_id:
        # Use manually specified project ID
        # Verify it exists
        projects = integration.manager.get_all_projects()
        if any(p['project_id'] == manual_project_id for p in projects):
            project_id = manual_project_id
            project_created = False
        else:
            # Project doesn't exist, fall back to auto-detection
            print(f"⚠️  Warning: Project ID '{manual_project_id}' not found, using auto-detection", file=sys.stderr)
            project_id, project_created = integration.get_or_create_project()
    else:
        # Auto-detect project from directory
        project_id, project_created = integration.get_or_create_project()

    # Get or create instance
    instance_id, instance_created = integration.get_or_create_instance(project_id)

    integration.close()

    return project_id, instance_id, project_created, instance_created


def finalize_for_command(
    project_id: str,
    instance_id: str,
    prompt: str,
    output_file: Optional[str] = None
) -> int:
    """
    Finalize database-first context after a command.

    This is called automatically after each cpp/cpps command.

    Args:
        project_id: Project identifier
        instance_id: Instance identifier
        prompt: The prompt that was executed
        output_file: Path to output file (optional)

    Returns:
        snapshot_id of created context snapshot
    """
    integration = AutoContextIntegration()

    # Read output if file provided
    output = None
    if output_file and Path(output_file).exists():
        try:
            with open(output_file, 'r') as f:
                # Only store first 10KB of output
                output = f.read(10240)
        except:
            pass

    # Store context
    snapshot_id = integration.store_command_context(
        project_id=project_id,
        prompt=prompt,
        output=output,
        priority='HIGH'
    )

    integration.close()

    return snapshot_id


def main():
    """CLI entry point for testing."""
    if len(sys.argv) < 2:
        print("Usage: python3 auto_context_integration.py <command> [args]")
        print()
        print("Commands:")
        print("  init <prompt>           Initialize for command")
        print("  finalize <proj> <inst> <prompt> [output_file]")
        print("  session                 Show current session")
        print("  end                     End current session")
        sys.exit(1)

    command = sys.argv[1]
    integration = AutoContextIntegration()

    if command == "init":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "test prompt"

        # Check for --project-id flag
        manual_project_id = None
        if '--project-id' in sys.argv:
            proj_idx = sys.argv.index('--project-id')
            if proj_idx + 1 < len(sys.argv):
                manual_project_id = sys.argv[proj_idx + 1]

        project_id, instance_id, proj_new, inst_new = initialize_for_command(prompt, manual_project_id)
        print(f"Project: {project_id} {'(new)' if proj_new else '(existing)'}")
        print(f"Instance: {instance_id} {'(new)' if inst_new else '(existing)'}")

    elif command == "finalize":
        if len(sys.argv) < 5:
            print("Error: finalize requires project_id, instance_id, and prompt")
            sys.exit(1)
        project_id = sys.argv[2]
        instance_id = sys.argv[3]
        prompt = sys.argv[4]
        output_file = sys.argv[5] if len(sys.argv) > 5 else None
        snapshot_id = finalize_for_command(project_id, instance_id, prompt, output_file)
        print(f"Context stored: snapshot_id={snapshot_id}")

    elif command == "session":
        session = integration.get_current_session()
        if session:
            print("Current Session:")
            for key, value in session.items():
                print(f"  {key}: {value}")
        else:
            print("No active session")

    elif command == "end":
        integration.end_session()
        print("Session ended")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    integration.close()


if __name__ == "__main__":
    main()
