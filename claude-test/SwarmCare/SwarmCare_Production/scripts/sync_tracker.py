#!/usr/bin/env python3
"""
Tracker Synchronization System
Syncs phase-level state to root-level tracker
"""

import json
import sys
from pathlib import Path
from datetime import datetime

class TrackerSync:
    """Synchronize phase and root trackers"""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.root_tracker = self.root_dir / ".tracker" / "state.json"
        self.manifest = self.root_dir / ".tracker" / "phase_manifest.json"

    def sync_phase_to_root(self, phase_id):
        """Sync a single phase state to root tracker"""
        # Read phase state
        phase_state_file = self.root_dir / "phases" / f"phase{phase_id:02d}" / ".state" / "phase_state.json"

        if not phase_state_file.exists():
            print(f"⚠️  Phase {phase_id} state file not found")
            return False

        with open(phase_state_file) as f:
            phase_state = json.load(f)

        # Read root tracker
        with open(self.root_tracker) as f:
            root_state = json.load(f)

        # Read manifest for story points
        with open(self.manifest) as f:
            manifest = json.load(f)

        # Update root tracker based on phase status
        phase_info = next((p for p in manifest['phases'] if p['phase_id'] == phase_id), None)

        if not phase_info:
            print(f"⚠️  Phase {phase_id} not found in manifest")
            return False

        story_points = phase_info['story_points']

        # Update completion status
        if phase_state.get('status') == 'COMPLETED' and phase_id not in root_state['completed_phases']:
            root_state['completed_phases'].append(phase_id)
            root_state['story_points_completed'] += story_points
            root_state['story_points_remaining'] -= story_points
            root_state['progress_percentage'] = int(
                (root_state['story_points_completed'] / root_state['total_story_points']) * 100
            )
            root_state['last_activity'] = f"Completed Phase {phase_id}"

            # Move to next phase
            if phase_id < 28:
                root_state['current_phase'] = phase_id + 1
                root_state['status'] = 'IN_PROGRESS'
            else:
                root_state['status'] = 'COMPLETED'
                root_state['current_phase'] = 28

        elif phase_state.get('status') == 'IN_PROGRESS':
            root_state['current_phase'] = phase_id
            root_state['status'] = 'IN_PROGRESS'
            root_state['in_progress_phase'] = phase_id
            root_state['last_activity'] = f"Working on Phase {phase_id}"

        # Update timestamp
        root_state['last_updated'] = datetime.now().isoformat()

        # Write back root tracker
        with open(self.root_tracker, 'w') as f:
            json.dump(root_state, f, indent=2)

        print(f"✅ Synced Phase {phase_id} to root tracker")
        return True

    def sync_all_phases(self):
        """Scan all phases and sync their states"""
        synced = 0
        for phase_id in range(29):
            phase_state_file = self.root_dir / "phases" / f"phase{phase_id:02d}" / ".state" / "phase_state.json"
            if phase_state_file.exists():
                if self.sync_phase_to_root(phase_id):
                    synced += 1

        print(f"\n✅ Synced {synced}/29 phases to root tracker")
        return synced

    def get_current_phase(self):
        """Get current phase from root tracker"""
        with open(self.root_tracker) as f:
            root_state = json.load(f)
        return root_state['current_phase']

    def mark_phase_started(self, phase_id):
        """Mark a phase as started"""
        phase_state_file = self.root_dir / "phases" / f"phase{phase_id:02d}" / ".state" / "phase_state.json"

        if phase_state_file.exists():
            with open(phase_state_file) as f:
                phase_state = json.load(f)

            phase_state['status'] = 'IN_PROGRESS'
            phase_state['started_at'] = datetime.now().isoformat()
            phase_state['last_updated'] = datetime.now().isoformat()

            with open(phase_state_file, 'w') as f:
                json.dump(phase_state, f, indent=2)

            # Sync to root
            self.sync_phase_to_root(phase_id)
            print(f"✅ Phase {phase_id} marked as IN_PROGRESS")
            return True

        return False

    def mark_phase_completed(self, phase_id):
        """Mark a phase as completed"""
        phase_state_file = self.root_dir / "phases" / f"phase{phase_id:02d}" / ".state" / "phase_state.json"

        if phase_state_file.exists():
            with open(phase_state_file) as f:
                phase_state = json.load(f)

            phase_state['status'] = 'COMPLETED'
            phase_state['progress_percentage'] = 100
            phase_state['completed_at'] = datetime.now().isoformat()
            phase_state['last_updated'] = datetime.now().isoformat()

            with open(phase_state_file, 'w') as f:
                json.dump(phase_state, f, indent=2)

            # Sync to root
            self.sync_phase_to_root(phase_id)
            print(f"✅ Phase {phase_id} marked as COMPLETED")
            return True

        return False


def main():
    """CLI Interface"""
    sync = TrackerSync()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  sync_tracker.py sync <phase_id>    - Sync specific phase")
        print("  sync_tracker.py sync-all           - Sync all phases")
        print("  sync_tracker.py start <phase_id>   - Mark phase as started")
        print("  sync_tracker.py complete <phase_id> - Mark phase as completed")
        print("  sync_tracker.py current            - Show current phase")
        sys.exit(1)

    command = sys.argv[1]

    if command == "sync" and len(sys.argv) == 3:
        phase_id = int(sys.argv[2])
        sync.sync_phase_to_root(phase_id)

    elif command == "sync-all":
        sync.sync_all_phases()

    elif command == "start" and len(sys.argv) == 3:
        phase_id = int(sys.argv[2])
        sync.mark_phase_started(phase_id)

    elif command == "complete" and len(sys.argv) == 3:
        phase_id = int(sys.argv[2])
        sync.mark_phase_completed(phase_id)

    elif command == "current":
        current = sync.get_current_phase()
        print(f"Current Phase: {current}")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
