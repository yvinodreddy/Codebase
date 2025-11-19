#!/usr/bin/env python3
"""
Multi-Project Manager for Database-First Architecture

Manages multiple projects with multiple instances each.
Supports project creation, instance management, and context coordination.

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import uuid
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlite_context_loader import SQLiteContextLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiProjectManager:
    """
    Manages multiple projects with multiple instances each.

    Architecture:
    - Each project has unique project_id
    - Each instance has unique instance_id
    - Context isolated by project_id in database
    - Supports 5 projects × 3 instances = 15 total (or more)

    Example:
        >>> manager = MultiProjectManager("ultrathink_context.db")
        >>> project_id = manager.create_project(
        ...     name="My Project",
        ...     description="Large-scale project",
        ...     total_story_points=1300
        ... )
        >>> instance_id = manager.launch_instance(project_id, phase_id=1)
        >>> print(f"Instance {instance_id} ready for project {project_id}")
    """

    def __init__(self, db_path: str = "ultrathink_context.db"):
        """
        Initialize MultiProjectManager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.loader = SQLiteContextLoader(db_path)
        logger.info(f"✅ MultiProjectManager initialized")

    def create_project(
        self,
        name: str,
        description: str,
        total_story_points: int = 1300
    ) -> str:
        """
        Create a new project.

        Args:
            name: Project name
            description: Project description
            total_story_points: Total story points for project

        Returns:
            project_id of created project
        """
        # Generate unique project ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        project_id = f"proj_{timestamp}_{unique_id}"

        # Insert into database
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO projects (project_id, name, description, total_story_points)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (project_id, name, description, total_story_points))
            conn.commit()

            logger.info(f"✅ Project created: {project_id} ({name})")
            return project_id

        except Exception as e:
            logger.error(f"❌ Failed to create project: {e}")
            conn.rollback()
            raise

    def launch_instance(
        self,
        project_id: str,
        phase_id: Optional[int] = None
    ) -> str:
        """
        Launch a new instance for a project.

        Args:
            project_id: Project identifier
            phase_id: Optional phase identifier

        Returns:
            instance_id of launched instance
        """
        # Generate unique instance ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        instance_id = f"inst_{timestamp}_{unique_id}"

        # Load context for instance
        result = self.loader.load_context_for_instance(
            instance_id=instance_id,
            project_id=project_id,
            phase_id=phase_id
        )

        logger.info(f"✅ Instance launched: {instance_id} for project {project_id}")
        return instance_id

    def get_project_instances(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all active instances for a project.

        Args:
            project_id: Project identifier

        Returns:
            List of instance dictionaries
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT instance_id, project_id, phase_id, hostname, process_id,
                   started_at, last_heartbeat, status, current_token_usage
            FROM active_instances
            WHERE project_id = ?
              AND status = 'active'
            ORDER BY started_at DESC
        """
        cursor.execute(query, (project_id,))

        instances = []
        for row in cursor.fetchall():
            instances.append({
                'instance_id': row['instance_id'],
                'project_id': row['project_id'],
                'phase_id': row['phase_id'],
                'hostname': row['hostname'],
                'process_id': row['process_id'],
                'started_at': row['started_at'],
                'last_heartbeat': row['last_heartbeat'],
                'status': row['status'],
                'current_token_usage': row['current_token_usage']
            })

        return instances

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects.

        Returns:
            List of project dictionaries
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT project_id, name, description, total_story_points,
                   completed_story_points, total_phases, created_at, updated_at
            FROM projects
            ORDER BY created_at DESC
        """
        cursor.execute(query)

        projects = []
        for row in cursor.fetchall():
            projects.append({
                'project_id': row['project_id'],
                'name': row['name'],
                'description': row['description'],
                'total_story_points': row['total_story_points'],
                'completed_story_points': row['completed_story_points'],
                'total_phases': row['total_phases'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })

        return projects

    def store_context(
        self,
        project_id: str,
        content: Dict[str, Any],
        priority: str = 'HIGH',
        content_type: str = 'code',
        phase_id: Optional[int] = None
    ) -> int:
        """
        Store context for a project.

        This is called whenever new context is created (code written, decisions made, etc.).
        All instances of this project will see this context.

        Args:
            project_id: Project identifier
            content: Context data
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            content_type: Type of content
            phase_id: Optional phase identifier

        Returns:
            snapshot_id of created snapshot
        """
        return self.loader.store_context(
            project_id=project_id,
            content=content,
            priority=priority,
            content_type=content_type,
            phase_id=phase_id
        )

    def create_phase(
        self,
        project_id: str,
        phase_number: int,
        name: str,
        story_points: int = 0
    ) -> int:
        """
        Create a new phase for a project.

        Args:
            project_id: Project identifier
            phase_number: Phase number (1, 2, 3, ...)
            name: Phase name
            story_points: Story points for this phase

        Returns:
            phase_id of created phase
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO phases (project_id, phase_number, name, story_points, status)
                VALUES (?, ?, ?, ?, 'pending')
            """
            cursor.execute(query, (project_id, phase_number, name, story_points))
            conn.commit()

            phase_id = cursor.lastrowid
            logger.info(f"✅ Phase created: {phase_id} ({name}) for project {project_id}")
            return phase_id

        except Exception as e:
            logger.error(f"❌ Failed to create phase: {e}")
            conn.rollback()
            raise

    def get_project_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary of all projects with instance counts.

        Returns:
            List of project summaries
        """
        conn = self.loader._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM v_project_summary
            ORDER BY created_at DESC
        """
        cursor.execute(query)

        summaries = []
        for row in cursor.fetchall():
            summaries.append({
                'project_id': row['project_id'],
                'name': row['name'],
                'total_story_points': row['total_story_points'],
                'completed_story_points': row['completed_story_points'],
                'active_instances': row['active_instances'],
                'total_snapshots': row['total_snapshots'],
                'total_tokens': row['total_tokens'] or 0,
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })

        return summaries

    def close(self):
        """Close database connection."""
        self.loader.close()


def launch_multi_project_environment():
    """
    Example: Launch 5 projects × 3 instances = 15 total instances.

    This demonstrates the multi-project, multi-instance architecture.
    """
    manager = MultiProjectManager("ultrathink_context.db")

    print("\n" + "=" * 80)
    print("🚀 LAUNCHING MULTI-PROJECT ENVIRONMENT")
    print("=" * 80 + "\n")

    # Create 5 projects
    projects = []
    for i in range(1, 6):
        project_id = manager.create_project(
            name=f"Project {i}",
            description=f"Large-scale project {i} with 1300 story points",
            total_story_points=1300
        )
        projects.append(project_id)
        print(f"✅ Created {project_id}: Project {i}")

    print()

    # Launch 3 instances per project (15 total)
    instances = []
    for i, project_id in enumerate(projects, 1):
        print(f"\n📦 Launching instances for Project {i}:")
        for j in range(1, 4):
            instance_id = manager.launch_instance(project_id, phase_id=None)
            instances.append({
                'instance_id': instance_id,
                'project_id': project_id,
                'project_name': f"Project {i}",
                'instance_number': j
            })
            print(f"  ✅ Instance {j}: {instance_id}")

    print("\n" + "=" * 80)
    print(f"🎉 SUCCESS: {len(projects)} projects, {len(instances)} instances running")
    print("=" * 80 + "\n")

    # Display summary
    print("📊 PROJECT SUMMARY:")
    print("-" * 80)
    summaries = manager.get_project_summary()
    for summary in summaries:
        print(f"  • {summary['name']}: {summary['active_instances']} active instances, "
              f"{summary['total_snapshots']} snapshots")

    manager.close()
    return projects, instances


if __name__ == "__main__":
    launch_multi_project_environment()
