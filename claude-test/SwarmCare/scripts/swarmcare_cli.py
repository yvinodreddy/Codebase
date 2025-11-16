#!/usr/bin/env python3
"""
SwarmCare CLI - Phase Tracking and Resumable Execution Tool
Version: 1.0
Purpose: Track project progress and enable resumable execution across sessions
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import shutil

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
STATE_DIR = PROJECT_ROOT / ".phase_state"
CHECKPOINTS_DIR = STATE_DIR / "checkpoints"

# State files
CURRENT_PHASE_FILE = STATE_DIR / "current_phase.json"
COMPLETED_STORIES_FILE = STATE_DIR / "completed_stories.json"
EXECUTION_LOG_FILE = STATE_DIR / "execution_log.json"
INTEGRATION_POINTS_FILE = STATE_DIR / "integration_points.json"

# Phase definitions (ULTIMATE v2.1 - PERFECT SCORE 120/120)
PHASES = {
    # Original Phases (Epic 1-12) - 565 points
    0: {"name": "Foundation & Infrastructure", "story_points": 37},
    1: {"name": "RAG Heat System", "story_points": 60},
    2: {"name": "SWARMCARE Agents", "story_points": 94},
    3: {"name": "Workflow Orchestration", "story_points": 76},
    4: {"name": "Frontend Application", "story_points": 47},
    5: {"name": "Audio Generation", "story_points": 21},
    6: {"name": "HIPAA Compliance (Base)", "story_points": 47},
    7: {"name": "Testing & QA", "story_points": 68},
    8: {"name": "Production Deployment", "story_points": 47},
    9: {"name": "Documentation", "story_points": 21},
    10: {"name": "Business & Partnerships", "story_points": 26},
    11: {"name": "Research & Publications", "story_points": 21},
    # Enhanced Phases (Epic 13-20) - 406 points
    12: {"name": "Real-time Clinical Decision Support (Base)", "story_points": 55},
    13: {"name": "Predictive Analytics & ML Models (Base)", "story_points": 62},
    14: {"name": "Multi-modal AI - Medical Imaging (Base)", "story_points": 76},
    15: {"name": "Advanced Medical NLP & Auto-Coding (Base)", "story_points": 47},
    16: {"name": "Explainable AI & Interpretability (Base)", "story_points": 34},
    17: {"name": "Population Health Management (Base)", "story_points": 43},
    18: {"name": "Clinical Trial Matching & Research (Base)", "story_points": 38},
    19: {"name": "Voice AI & Ambient Intelligence (Base)", "story_points": 51},
    # Perfect Score Sub-Phases (Epic A) - 131 points for 120/120
    20: {"name": "Epic 7A: Security Certifications (SOC 2, HITRUST)", "story_points": 13},
    21: {"name": "Epic 13A: Closed-Loop Clinical Automation", "story_points": 13},
    22: {"name": "Epic 14A: Continuous Learning & Federated ML", "story_points": 8},
    23: {"name": "Epic 15A: FDA Clearance & PACS Integration", "story_points": 21},
    24: {"name": "Epic 16A: 100% Automated Coding & EHR Integration", "story_points": 13},
    25: {"name": "Epic 17A: Validated Patient-Facing XAI", "story_points": 8},
    26: {"name": "Epic 18A: Real-time CDC & Public Health Integration", "story_points": 21},
    27: {"name": "Epic 19A: Full Trial Lifecycle (EDC, eConsent, AE Reporting)", "story_points": 21},
    28: {"name": "Epic 20A: Ultra-fast Offline Voice AI (<500ms, 8 EHRs)", "story_points": 13},
}

TOTAL_STORY_POINTS = sum(p["story_points"] for p in PHASES.values())


def ensure_state_dir():
    """Ensure state directory exists"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)


def log_action(action: str, message: str, **kwargs):
    """Log an action to execution log"""
    ensure_state_dir()

    if EXECUTION_LOG_FILE.exists():
        with open(EXECUTION_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {"logs": []}

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "message": message,
        "user": os.getenv("USER", "system"),
        **kwargs
    }

    log_data["logs"].append(log_entry)

    with open(EXECUTION_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def init_project():
    """Initialize project structure"""
    print("=" * 60)
    print("SWARMCARE PROJECT INITIALIZATION")
    print("=" * 60)
    print()

    ensure_state_dir()

    # Initialize current_phase.json
    if not CURRENT_PHASE_FILE.exists():
        current_phase_data = {
            "current_phase": None,
            "phase_name": None,
            "status": "NOT_STARTED",
            "progress_percentage": 0,
            "started_at": None,
            "last_updated": datetime.now().isoformat(),
            "current_user_story": None,
            "completed_stories": [],
            "next_steps": [
                "Run: python scripts/swarmcare_cli.py start-phase --phase 0",
                "Begin with Phase 0: Foundation & Infrastructure"
            ],
            "blockers": [],
            "notes": "Project initialized. Ready to start Phase 0."
        }
        with open(CURRENT_PHASE_FILE, 'w') as f:
            json.dump(current_phase_data, f, indent=2)
        print("✓ Created current_phase.json")
    else:
        print("⚠ current_phase.json already exists, skipping")

    # Initialize completed_stories.json
    if not COMPLETED_STORIES_FILE.exists():
        completed_stories_data = {
            "completed_stories": [],
            "total_completed": 0,
            "total_story_points_completed": 0,
            "total_story_points": TOTAL_STORY_POINTS
        }
        with open(COMPLETED_STORIES_FILE, 'w') as f:
            json.dump(completed_stories_data, f, indent=2)
        print("✓ Created completed_stories.json")
    else:
        print("⚠ completed_stories.json already exists, skipping")

    # Initialize execution_log.json
    if not EXECUTION_LOG_FILE.exists():
        with open(EXECUTION_LOG_FILE, 'w') as f:
            json.dump({"logs": []}, f, indent=2)
        print("✓ Created execution_log.json")
    else:
        print("⚠ execution_log.json already exists, skipping")

    # Initialize integration_points.json
    if not INTEGRATION_POINTS_FILE.exists():
        integration_data = {
            "integration_points": [
                {
                    "id": "IP1",
                    "name": "RAG Heat API → SWARMCARE Agents",
                    "phases": [1, 2],
                    "description": "Agents call RAG Heat API for knowledge retrieval",
                    "status": "NOT_STARTED",
                    "validated": False
                },
                {
                    "id": "IP2",
                    "name": "SWARMCARE Backend → Frontend",
                    "phases": [2, 4],
                    "description": "Frontend displays agent status and workflows",
                    "status": "NOT_STARTED",
                    "validated": False
                },
                {
                    "id": "IP3",
                    "name": "RAG Heat → Frontend",
                    "phases": [1, 4],
                    "description": "Frontend query interface for RAG Heat",
                    "status": "NOT_STARTED",
                    "validated": False
                }
            ]
        }
        with open(INTEGRATION_POINTS_FILE, 'w') as f:
            json.dump(integration_data, f, indent=2)
        print("✓ Created integration_points.json")
    else:
        print("⚠ integration_points.json already exists, skipping")

    log_action("INIT_PROJECT", "Project initialized")

    print()
    print("=" * 60)
    print("PROJECT OVERVIEW")
    print("=" * 60)
    print(f"Total Phases: {len(PHASES)}")
    print(f"Total Story Points: {TOTAL_STORY_POINTS}")
    print()
    print("Phases:")
    for phase_num, phase_info in PHASES.items():
        print(f"  Phase {phase_num}: {phase_info['name']:<35} ({phase_info['story_points']} points)")
    print()
    print("Next Steps:")
    print("  1. python scripts/swarmcare_cli.py start-phase --phase 0")
    print("  2. Begin implementing user stories from IMPLEMENTATION_MASTER_PLAN.md")
    print("  3. Mark stories complete with: python scripts/swarmcare_cli.py complete-story --story X.Y")
    print()
    print("Initialization complete! ✓")
    print("=" * 60)


def start_phase(phase_num: int, force: bool = False):
    """Start a specific phase"""
    if phase_num not in PHASES:
        print(f"Error: Invalid phase number {phase_num}. Must be 0-{len(PHASES)-1}")
        sys.exit(1)

    phase_info = PHASES[phase_num]

    print("=" * 60)
    print(f"STARTING PHASE {phase_num}: {phase_info['name']}")
    print("=" * 60)
    print()

    # Check prerequisites (previous phase completed)
    if phase_num > 0 and not force:
        with open(CURRENT_PHASE_FILE, 'r') as f:
            current_data = json.load(f)

        # Check if previous phase is complete
        # In a full implementation, you'd check completed_stories.json
        # For now, we'll allow starting any phase with --force flag
        pass

    # Update current_phase.json
    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    current_data.update({
        "current_phase": phase_num,
        "phase_name": phase_info["name"],
        "status": "IN_PROGRESS",
        "started_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "notes": f"Started Phase {phase_num}: {phase_info['name']}"
    })

    with open(CURRENT_PHASE_FILE, 'w') as f:
        json.dump(current_data, f, indent=2)

    log_action("START_PHASE", f"Started Phase {phase_num}: {phase_info['name']}", phase=phase_num)

    print(f"Phase: {phase_info['name']}")
    print(f"Story Points: {phase_info['story_points']}")
    print()
    print("Status: IN_PROGRESS")
    print()
    print("Next Steps:")
    print(f"  1. Review user stories for Phase {phase_num} in IMPLEMENTATION_MASTER_PLAN.md")
    print("  2. Begin implementing features")
    print("  3. Mark stories complete as you finish them")
    print()
    print(f"Phase {phase_num} started! ✓")
    print("=" * 60)


def resume_execution():
    """Resume from last checkpoint"""
    print("=" * 60)
    print("SWARMCARE PROJECT RESUMPTION")
    print("=" * 60)
    print()

    if not CURRENT_PHASE_FILE.exists():
        print("Error: Project not initialized. Run: python scripts/swarmcare_cli.py init")
        sys.exit(1)

    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    with open(COMPLETED_STORIES_FILE, 'r') as f:
        completed_data = json.load(f)

    current_phase = current_data.get("current_phase")

    if current_phase is None:
        print("Status: Project initialized, no phase started yet")
        print()
        print("Next Steps:")
        print("  1. python scripts/swarmcare_cli.py start-phase --phase 0")
        print("  2. Begin with Phase 0: Foundation & Infrastructure")
        print()
        return

    phase_info = PHASES[current_phase]

    print(f"Current Phase: Phase {current_phase} - {phase_info['name']}")
    print(f"Status: {current_data['status']}")
    print(f"Progress: {current_data['progress_percentage']}% ({phase_info['story_points']} story points)")
    print()

    if current_data.get('last_updated'):
        print(f"Last Updated: {current_data['last_updated']}")

    print()

    # Show completed stories
    completed_stories = current_data.get('completed_stories', [])
    if completed_stories:
        print("Completed User Stories:")
        for story_id in completed_stories:
            print(f"  ✓ {story_id}")
        print()

    # Show next steps
    if current_data.get('next_steps'):
        print("Next Steps:")
        for i, step in enumerate(current_data['next_steps'], 1):
            print(f"  {i}. {step}")
        print()

    # Show blockers
    blockers = current_data.get('blockers', [])
    if blockers:
        print("Blockers:")
        for blocker in blockers:
            print(f"  ⚠ {blocker}")
        print()

    # Notes
    if current_data.get('notes'):
        print(f"Notes: {current_data['notes']}")
        print()

    print("Recommended Commands:")
    print("  - Show next user story: python scripts/swarmcare_cli.py next")
    print("  - Complete a story: python scripts/swarmcare_cli.py complete-story --story X.Y")
    print("  - Create checkpoint: python scripts/swarmcare_cli.py checkpoint --message 'Your message'")
    print("  - Generate report: python scripts/swarmcare_cli.py report")
    print()
    print("=" * 60)


def complete_story(story_id: str, notes: Optional[str] = None):
    """Mark a user story as completed"""
    print(f"Completing User Story {story_id}...")

    # Load completed stories
    with open(COMPLETED_STORIES_FILE, 'r') as f:
        completed_data = json.load(f)

    # Check if already completed
    existing_stories = [s['story_id'] for s in completed_data['completed_stories']]
    if story_id in existing_stories:
        print(f"Warning: Story {story_id} already marked as completed")
        return

    # Add to completed stories
    story_entry = {
        "story_id": story_id,
        "phase": int(story_id.split('.')[0]),
        "completed_at": datetime.now().isoformat(),
        "completed_by": os.getenv("USER", "team"),
        "notes": notes or ""
    }

    completed_data['completed_stories'].append(story_entry)
    completed_data['total_completed'] = len(completed_data['completed_stories'])

    with open(COMPLETED_STORIES_FILE, 'w') as f:
        json.dump(completed_data, f, indent=2)

    # Update current phase
    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    completed_stories_list = current_data.get('completed_stories', [])
    if story_id not in completed_stories_list:
        completed_stories_list.append(story_id)

    current_data['completed_stories'] = completed_stories_list
    current_data['last_updated'] = datetime.now().isoformat()

    with open(CURRENT_PHASE_FILE, 'w') as f:
        json.dump(current_data, f, indent=2)

    log_action("COMPLETE_STORY", f"Completed User Story {story_id}", story=story_id)

    print(f"✓ User Story {story_id} marked as completed")
    if notes:
        print(f"  Notes: {notes}")
    print()
    print("Run 'python scripts/swarmcare_cli.py resume' to see updated progress")


def create_checkpoint(message: str):
    """Create a manual checkpoint"""
    checkpoint_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_file = CHECKPOINTS_DIR / f"checkpoint_{checkpoint_id}.json"

    # Read current state
    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    with open(COMPLETED_STORIES_FILE, 'r') as f:
        completed_data = json.load(f)

    # Create checkpoint
    checkpoint_data = {
        "checkpoint_id": checkpoint_id,
        "created_at": datetime.now().isoformat(),
        "message": message,
        "current_phase": current_data,
        "completed_stories": completed_data
    }

    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint_data, f, indent=2)

    log_action("CHECKPOINT", message, checkpoint_id=checkpoint_id)

    print(f"✓ Checkpoint created: {checkpoint_id}")
    print(f"  Message: {message}")
    print(f"  File: {checkpoint_file}")


def generate_report(output_format: str = "markdown"):
    """Generate progress report"""
    print("=" * 60)
    print("SWARMCARE PROJECT PROGRESS REPORT")
    print("=" * 60)
    print()

    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    with open(COMPLETED_STORIES_FILE, 'r') as f:
        completed_data = json.load(f)

    total_completed_points = completed_data['total_story_points_completed']
    total_points = completed_data['total_story_points']
    overall_progress = (total_completed_points / total_points * 100) if total_points > 0 else 0

    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print(f"Overall Progress: {overall_progress:.1f}% ({total_completed_points}/{total_points} story points)")
    print()

    # Progress bar
    bar_length = 40
    filled = int(bar_length * overall_progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"[{bar}] {overall_progress:.1f}%")
    print()

    print("Phases:")
    for phase_num, phase_info in PHASES.items():
        # Calculate phase progress
        phase_stories = [s for s in completed_data['completed_stories'] if s['phase'] == phase_num]
        # For now, we don't have story point data per story, so we'll use story count
        phase_progress = (len(phase_stories) / phase_info['story_points'] * 100) if phase_info['story_points'] > 0 else 0

        status_icon = "✓" if phase_progress == 100 else "→" if phase_progress > 0 else " "
        bar_length = 20
        filled = int(bar_length * phase_progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"{status_icon} Phase {phase_num}: {phase_info['name']:<35} [{bar}] {phase_progress:.0f}%")

    print()
    print(f"Total User Stories Completed: {completed_data['total_completed']}")
    print()

    if current_data.get('current_phase') is not None:
        current_phase = current_data['current_phase']
        print(f"Current Focus: Phase {current_phase} - {PHASES[current_phase]['name']}")
        print(f"Status: {current_data['status']}")

    print()
    print("=" * 60)


def list_phases():
    """List all phases with status"""
    print("=" * 60)
    print("SWARMCARE PHASES")
    print("=" * 60)
    print()

    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    current_phase_num = current_data.get('current_phase')

    for phase_num, phase_info in PHASES.items():
        status = "CURRENT" if phase_num == current_phase_num else "NOT_STARTED"
        marker = "→" if phase_num == current_phase_num else " "

        print(f"{marker} Phase {phase_num}: {phase_info['name']:<40} ({phase_info['story_points']:>3} points) - {status}")

    print()
    print("=" * 60)


def show_dashboard():
    """Show project dashboard"""
    print("=" * 60)
    print("SWARMCARE PROJECT DASHBOARD")
    print("=" * 60)
    print()

    with open(CURRENT_PHASE_FILE, 'r') as f:
        current_data = json.load(f)

    with open(COMPLETED_STORIES_FILE, 'r') as f:
        completed_data = json.load(f)

    total_completed_points = completed_data['total_story_points_completed']
    total_points = completed_data['total_story_points']
    overall_progress = (total_completed_points / total_points * 100) if total_points > 0 else 0

    # Overall progress bar
    bar_length = 40
    filled = int(bar_length * overall_progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"Overall Progress: [{bar}] {overall_progress:.1f}% ({total_completed_points}/{total_points} story points)")
    print()

    # Phases
    print("Phases:")
    for phase_num, phase_info in PHASES.items():
        phase_stories = [s for s in completed_data['completed_stories'] if s['phase'] == phase_num]
        # Simplified progress calculation
        phase_progress = (len(phase_stories) / max(1, phase_info['story_points']) * 100)

        status_icon = "✓" if phase_progress >= 100 else "→" if phase_progress > 0 else " "
        bar_length = 20
        filled = int(bar_length * min(phase_progress, 100) / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"{status_icon} Phase {phase_num}: {phase_info['name']:<35} [{bar}] {phase_progress:.0f}%")

    print()

    if current_data.get('current_phase') is not None:
        current_phase = current_data['current_phase']
        print(f"Current Focus: Phase {current_phase} - {PHASES[current_phase]['name']}")
        print(f"Status: {current_data['status']}")
        print()

    # Recent activity (last 5 completed stories)
    recent_stories = sorted(
        completed_data['completed_stories'],
        key=lambda x: x['completed_at'],
        reverse=True
    )[:5]

    if recent_stories:
        print("Recent Activity:")
        for story in recent_stories:
            completed_time = datetime.fromisoformat(story['completed_at']).strftime('%Y-%m-%d %H:%M')
            print(f"✓ [{completed_time}] Completed Story {story['story_id']}")
        print()

    # Blockers
    blockers = current_data.get('blockers', [])
    if blockers:
        print(f"Blockers: {len(blockers)}")
        for blocker in blockers:
            print(f"⚠ {blocker}")
        print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="SwarmCare CLI - Phase Tracking and Resumable Execution Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize project
  python scripts/swarmcare_cli.py init

  # Resume from last checkpoint
  python scripts/swarmcare_cli.py resume

  # Start a phase
  python scripts/swarmcare_cli.py start-phase --phase 0

  # Complete a user story
  python scripts/swarmcare_cli.py complete-story --story "1.1" --notes "Completed"

  # Create checkpoint
  python scripts/swarmcare_cli.py checkpoint --message "Day 1 complete"

  # Generate report
  python scripts/swarmcare_cli.py report

  # Show dashboard
  python scripts/swarmcare_cli.py dashboard
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Init command
    subparsers.add_parser('init', help='Initialize project structure')

    # Start phase command
    start_parser = subparsers.add_parser('start-phase', help='Start a specific phase')
    start_parser.add_argument('--phase', type=int, required=True, help='Phase number (0-11)')
    start_parser.add_argument('--force', action='store_true', help='Force start even if prerequisites not met')

    # Resume command
    subparsers.add_parser('resume', help='Resume from last checkpoint')

    # Complete story command
    complete_parser = subparsers.add_parser('complete-story', help='Mark a user story as completed')
    complete_parser.add_argument('--story', type=str, required=True, help='User story ID (e.g., "1.1")')
    complete_parser.add_argument('--notes', type=str, help='Optional completion notes')

    # Checkpoint command
    checkpoint_parser = subparsers.add_parser('checkpoint', help='Create manual checkpoint')
    checkpoint_parser.add_argument('--message', type=str, required=True, help='Checkpoint message')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate progress report')
    report_parser.add_argument('--format', type=str, default='markdown', choices=['markdown', 'html', 'json'], help='Output format')

    # List phases command
    subparsers.add_parser('list-phases', help='List all phases with status')

    # Dashboard command
    subparsers.add_parser('dashboard', help='Show project dashboard')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'init':
        init_project()
    elif args.command == 'start-phase':
        start_phase(args.phase, args.force)
    elif args.command == 'resume':
        resume_execution()
    elif args.command == 'complete-story':
        complete_story(args.story, args.notes)
    elif args.command == 'checkpoint':
        create_checkpoint(args.message)
    elif args.command == 'report':
        generate_report(args.format)
    elif args.command == 'list-phases':
        list_phases()
    elif args.command == 'dashboard':
        show_dashboard()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
