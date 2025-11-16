#!/usr/bin/env python3
"""
UNIFIED TRACKER SYSTEM - Production Ready
Integrates .state phase tracker with change tracking and documentation sync
CRITICAL: Preserves .state/phase_state.json (mandatory for phase integration)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class UnifiedTracker:
    """
    Unified tracker that integrates:
    1. .state/phase_state.json (MANDATORY - phase-level state)
    2. .tracker/state.json (MANDATORY - main tracker)
    3. Change tracking (consolidated into .state)
    4. Documentation sync (4 locations)
    """

    def __init__(self, phase_number: str = "15", phase_name: str = "Advanced Medical NLP & Auto-Coding"):
        self.phase_number = phase_number
        self.phase_name = phase_name

        # Paths setup
        self.script_dir = Path(__file__).parent
        self.standalone_dir = self.script_dir.parent
        self.phase_dir = self.standalone_dir.parent
        self.phases_dir = self.phase_dir.parent
        self.project_root = self.phases_dir.parent

        # CRITICAL PATHS (MANDATORY)
        self.phase_state_file = self.phase_dir / ".state" / "phase_state.json"
        self.main_tracker_file = self.project_root / ".tracker" / "state.json"
        self.manifest_file = self.project_root / ".tracker" / "phase_manifest.json"

        # Requirements
        self.requirements_dir = self.standalone_dir / "requirements"
        self.stories_file = self.requirements_dir / "user_stories.json"

        # Documentation sync locations (4 paths)
        self.doc_sync_locations = [
            self.project_root,
            self.project_root / "ai_prompts",
            self.project_root.parent,  # SwarmCare root
            self.project_root.parent / "ProjectPlan"
        ]

        # Ensure critical directories exist
        self.phase_state_file.parent.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # PHASE STATE MANAGEMENT (CRITICAL - .state/phase_state.json)
    # ========================================================================

    def read_phase_state(self) -> Dict[str, Any]:
        """Read phase state from .state/phase_state.json"""
        if not self.phase_state_file.exists():
            return self._init_phase_state()

        with open(self.phase_state_file, 'r') as f:
            return json.load(f)

    def write_phase_state(self, state: Dict[str, Any]):
        """Write phase state to .state/phase_state.json"""
        state['last_sync'] = datetime.now().isoformat()
        with open(self.phase_state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def _init_phase_state(self) -> Dict[str, Any]:
        """Initialize phase state"""
        return {
            "phase": self.phase_number,
            "phase_name": self.phase_name,
            "status": "active",
            "last_sync": datetime.now().isoformat(),
            "changes": [],
            "metrics": {
                "total_stories": 0,
                "total_story_points": 0,
                "completed_story_points": 0,
                "test_pass_rate": 0,
                "documentation_updated": False
            }
        }

    # ========================================================================
    # CHANGE TRACKING (Consolidated into .state)
    # ========================================================================

    def track_change(self, change_type: str, description: str,
                     story_id: Optional[str] = None,
                     story_title: Optional[str] = None) -> Dict[str, Any]:
        """
        Track a change in the phase state
        Replaces separate phase00_tracker.json and main_tracker.json
        """
        change = {
            "timestamp": datetime.now().isoformat(),
            "change_type": change_type,  # added, modified, deleted, tested, generated
            "description": description,
            "story_id": story_id,
            "story_title": story_title,
            "changed_by": "UI"
        }

        # Update phase state
        state = self.read_phase_state()
        state.setdefault("changes", []).append(change)
        state["total_changes"] = len(state["changes"])
        self.write_phase_state(state)

        # Sync to main tracker
        self._sync_to_main_tracker(change)

        return change

    def _sync_to_main_tracker(self, change: Dict[str, Any]):
        """Sync change to main tracker"""
        if not self.main_tracker_file.exists():
            return

        try:
            with open(self.main_tracker_file, 'r') as f:
                main_tracker = json.load(f)

            # Add to phase-specific changes
            phase_key = f"phase_{self.phase_number}_changes"
            main_tracker.setdefault(phase_key, []).append(change)

            # Update timestamp
            main_tracker["last_updated"] = datetime.now().isoformat()

            with open(self.main_tracker_file, 'w') as f:
                json.dump(main_tracker, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to sync to main tracker: {e}")

    # ========================================================================
    # USER STORY MANAGEMENT
    # ========================================================================

    def read_user_stories(self) -> Dict[str, Any]:
        """Read user stories from requirements"""
        if not self.stories_file.exists():
            return self._init_user_stories()

        with open(self.stories_file, 'r') as f:
            return json.load(f)

    def write_user_stories(self, data: Dict[str, Any]):
        """Write user stories to requirements"""
        with open(self.stories_file, 'w') as f:
            json.dump(data, f, indent=4)

    def _init_user_stories(self) -> Dict[str, Any]:
        """Initialize user stories structure"""
        return {
            "phase": f"phase{self.phase_number}",
            "phase_name": self.phase_name,
            "total_story_points": 0,
            "priority": "P0",
            "status": "in_progress",
            "stories": []
        }

    def update_metrics(self):
        """Update metrics based on current user stories"""
        stories_data = self.read_user_stories()
        stories = stories_data.get("stories", [])

        total_points = sum(s.get('story_points', 0) for s in stories)
        completed_points = sum(
            s.get('story_points', 0) for s in stories
            if s.get('status') == 'completed'
        )

        state = self.read_phase_state()
        state["metrics"] = {
            "total_stories": len(stories),
            "total_story_points": total_points,
            "completed_story_points": completed_points,
            "completion_percentage": round(
                (completed_points / total_points * 100) if total_points > 0 else 0,
                1
            ),
            "test_pass_rate": state.get("metrics", {}).get("test_pass_rate", 0),
            "documentation_updated": state.get("metrics", {}).get("documentation_updated", False)
        }
        self.write_phase_state(state)

        return state["metrics"]

    # ========================================================================
    # DOCUMENTATION SYNC (4 Locations)
    # ========================================================================

    def sync_documentation(self) -> List[str]:
        """
        Sync documentation to all 4 required locations:
        1. SwarmCare_Production
        2. SwarmCare_Production/ai_prompts
        3. SwarmCare (parent)
        4. SwarmCare/ProjectPlan
        """
        results = []

        # Generate current status document
        status_doc = self._generate_phase_status_doc()

        for location in self.doc_sync_locations:
            try:
                if not location.exists():
                    location.mkdir(parents=True, exist_ok=True)

                doc_file = location / f"PHASE_{self.phase_number}_STATUS.md"
                doc_file.write_text(status_doc)
                results.append(f"✅ Updated {location.name}/{doc_file.name}")
            except Exception as e:
                results.append(f"❌ Failed {location.name}: {str(e)}")

        # Update phase state
        state = self.read_phase_state()
        state["metrics"]["documentation_updated"] = True
        state["last_documentation_sync"] = datetime.now().isoformat()
        self.write_phase_state(state)

        # Track change
        self.track_change(
            "documentation_sync",
            f"Synced documentation to {len(results)} locations"
        )

        return results

    def _generate_phase_status_doc(self) -> str:
        """Generate phase status documentation"""
        state = self.read_phase_state()
        stories_data = self.read_user_stories()
        stories = stories_data.get("stories", [])

        content = f"""# Phase {self.phase_number}: {self.phase_name} - Current Status

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** {state.get('status', 'unknown').upper()}
**Total Story Points:** {state['metrics']['total_story_points']}
**Completed Story Points:** {state['metrics']['completed_story_points']}
**Completion:** {state['metrics']['completion_percentage']}%

---

## Metrics

- **Total Stories:** {state['metrics']['total_stories']}
- **Total Story Points:** {state['metrics']['total_story_points']}
- **Completed Story Points:** {state['metrics']['completed_story_points']}
- **Test Pass Rate:** {state['metrics']['test_pass_rate']}%

---

## User Stories ({len(stories)})

"""
        for story in stories:
            content += f"""### {story.get('id', 'N/A')}: {story.get('title', 'N/A')}
- **Points:** {story.get('story_points', 0)} SP
- **Priority:** {story.get('priority', 'N/A')}
- **Status:** {story.get('status', 'N/A')}
- **Description:** {story.get('description', 'N/A')}

"""

        content += f"""---

## Recent Changes (Last 10)

"""
        recent_changes = state.get("changes", [])[-10:]
        for change in reversed(recent_changes):
            content += f"""- **{change['timestamp']}**: {change['change_type'].upper()} - {change.get('description', 'N/A')}
"""

        content += f"""
---

**Auto-generated by Unified Tracker System**
**Last Sync:** {state.get('last_sync', 'N/A')}
"""
        return content

    # ========================================================================
    # COMPREHENSIVE STATUS
    # ========================================================================

    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get complete status for dashboard"""
        phase_state = self.read_phase_state()
        stories_data = self.read_user_stories()

        return {
            "phase": {
                "number": self.phase_number,
                "name": self.phase_name,
                "status": phase_state.get("status", "unknown"),
                "last_sync": phase_state.get("last_sync", "N/A")
            },
            "metrics": phase_state.get("metrics", {}),
            "stories": {
                "total": len(stories_data.get("stories", [])),
                "total_points": stories_data.get("total_story_points", 0),
                "by_status": self._count_stories_by_status(stories_data)
            },
            "changes": {
                "total": len(phase_state.get("changes", [])),
                "recent": phase_state.get("changes", [])[-5:]
            },
            "documentation": {
                "last_sync": phase_state.get("last_documentation_sync", "Never"),
                "locations": len(self.doc_sync_locations),
                "updated": phase_state.get("metrics", {}).get("documentation_updated", False)
            }
        }

    def _count_stories_by_status(self, stories_data: Dict[str, Any]) -> Dict[str, int]:
        """Count stories by status"""
        stories = stories_data.get("stories", [])
        return {
            "pending": len([s for s in stories if s.get('status') == 'pending']),
            "in_progress": len([s for s in stories if s.get('status') == 'in_progress']),
            "completed": len([s for s in stories if s.get('status') == 'completed']),
            "blocked": len([s for s in stories if s.get('status') == 'blocked'])
        }

    # ========================================================================
    # CLEANUP (Remove Redundant Trackers)
    # ========================================================================

    def cleanup_redundant_trackers(self) -> List[str]:
        """Remove redundant tracker files that are now consolidated into .state"""
        results = []
        redundant_files = [
            self.phase_dir / f"phase{self.phase_number}_tracker.json",
            self.project_root / "main_tracker.json"
        ]

        for file_path in redundant_files:
            if file_path.exists():
                try:
                    # Backup before removing
                    backup_path = file_path.with_suffix('.json.backup')
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    file_path.unlink()
                    results.append(f"✅ Removed redundant {file_path.name} (backup created)")
                except Exception as e:
                    results.append(f"❌ Failed to remove {file_path.name}: {e}")

        return results


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI interface for unified tracker"""
    import sys

    tracker = UnifiedTracker()

    if len(sys.argv) < 2:
        print("""
Unified Tracker System - Production Ready

Usage:
  unified_tracker.py status              - Show comprehensive status
  unified_tracker.py update-metrics      - Update metrics from user stories
  unified_tracker.py sync-docs           - Sync documentation to all locations
  unified_tracker.py track <type> <msg>  - Track a change
  unified_tracker.py cleanup             - Remove redundant tracker files
  unified_tracker.py init                - Initialize phase state
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        status = tracker.get_comprehensive_status()
        print(json.dumps(status, indent=2))

    elif command == "update-metrics":
        metrics = tracker.update_metrics()
        print("✅ Metrics updated:")
        print(json.dumps(metrics, indent=2))

    elif command == "sync-docs":
        results = tracker.sync_documentation()
        print("📄 Documentation Sync Results:")
        for result in results:
            print(f"  {result}")

    elif command == "track" and len(sys.argv) >= 4:
        change_type = sys.argv[2]
        description = " ".join(sys.argv[3:])
        change = tracker.track_change(change_type, description)
        print(f"✅ Change tracked: {change['change_type']} - {change['description']}")

    elif command == "cleanup":
        results = tracker.cleanup_redundant_trackers()
        print("🧹 Cleanup Results:")
        for result in results:
            print(f"  {result}")

    elif command == "init":
        state = tracker.read_phase_state()
        tracker.write_phase_state(state)
        print(f"✅ Phase state initialized: .state/phase_state.json")
        print(json.dumps(state, indent=2))

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
