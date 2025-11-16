# 🎯 COMPLETE TRACKER USAGE GUIDE

**The #1 Tool for Managing 1,362 Story Points**

---

## 📚 TABLE OF CONTENTS

1. [What is the Tracker?](#what-is-the-tracker)
2. [Tracker Architecture](#tracker-architecture)
3. [Quick Start (5 Minutes)](#quick-start-5-minutes)
4. [Root Level Commands](#root-level-commands)
5. [Phase Level Commands](#phase-level-commands)
6. [Complete Workflows](#complete-workflows)
7. [Continue from Where You Left Off](#continue-from-where-you-left-off)
8. [Multi-Machine Setup](#multi-machine-setup)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## What is the Tracker?

The tracker is your **progress management system** that lets you:

- ✅ **Continue from where you left off** (even after shutdown/sleep)
- ✅ **Track progress** across 29 phases and 1,362 story points
- ✅ **Work at any level** (root, phase, or task)
- ✅ **Switch between phases** safely
- ✅ **Survive interruptions** (power off, take breaks, come back tomorrow)
- ✅ **See real-time status** (progress bars, completion %)
- ✅ **Never lose progress** (auto-saves state)

**Think of it as Git for your development progress!**

---

## Tracker Architecture

### Two-Level System

```
ROOT LEVEL (.tracker/)
├── state.json          ← Overall project progress (29 phases, 1362 SP)
└── phase_manifest.json ← Phase definitions

PHASE LEVEL (phases/phaseXX/.state/)
└── phase_state.json    ← Individual phase progress
    ↑
    └── Syncs to root tracker automatically
```

###How It Works

1. **Root tracker** tracks overall project (which phase you're on, story points completed)
2. **Phase tracker** tracks individual phase progress (tasks, status, timestamps)
3. **Sync happens automatically** when you start/complete phases
4. **Both levels work independently** but stay in sync

---

## Quick Start (5 Minutes)

### First Time Setup

```bash
# 1. Check current status
./scripts/status.sh

# 2. Start first phase (Phase 0)
./scripts/start_phase.sh 0

# 3. Once complete, mark it done
./scripts/complete_phase.sh 0

# 4. Check updated status
./scripts/status.sh
```

**That's it!** You're now using the tracker.

---

## Root Level Commands

### View Status

```bash
# Quick status
./scripts/status.sh

# Detailed status (shows all 29 phases)
./scripts/status.sh --detailed

# Interactive status (continue script)
./continue
```

**Output:**
```
📊 SWARMCARE PROJECT STATUS
════════════════════════════════════════════════════════════════════
  Status:       IN_PROGRESS
  Current:      Phase 5
  Progress:     18%
  Completed:    245 / 1362 story points
  Remaining:    1117 story points
  Last:         Completed Phase 4

  [█████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  18%

✅ COMPLETED PHASES:
  ✅ Phase 00
  ✅ Phase 01
  ✅ Phase 02
  ✅ Phase 03
  ✅ Phase 04
```

### Start a Phase

```bash
# Start specific phase
./scripts/start_phase.sh <phase_id>

# Examples:
./scripts/start_phase.sh 0   # Start Phase 0
./scripts/start_phase.sh 5   # Start Phase 5
./scripts/start_phase.sh 15  # Start Phase 15
```

**What happens:**
1. Marks phase as "IN_PROGRESS" in trackers
2. Updates root tracker with current phase
3. Runs `phases/phaseXX/code/implementation.py`
4. Shows success/failure message
5. Tells you how to mark complete

### Complete a Phase

```bash
# Mark phase as complete
./scripts/complete_phase.sh <phase_id>

# Examples:
./scripts/complete_phase.sh 0   # Complete Phase 0
./scripts/complete_phase.sh 5   # Complete Phase 5
```

**What happens:**
1. Marks phase as "COMPLETED" (100%)
2. Adds story points to completed total
3. Updates progress percentage
4. Moves tracker to next phase
5. Tells you what to do next

### Continue Command (Interactive)

```bash
# Interactive tracker menu
./continue
```

**Features:**
- Shows current status
- Shows next steps
- Menu-driven (choose options)
- View detailed progress
- Jump to specific phases

---

## Phase Level Commands

### Navigate to Phase

```bash
# Go to any phase directory
cd phases/phase00    # Phase 0
cd phases/phase05    # Phase 5
cd phases/phase15    # Phase 15
```

### Run Phase from Phase Directory

```bash
# From within any phase directory
./continue

# Or explicitly:
../../scripts/run_from_phase.sh
```

**What happens:**
1. Auto-detects which phase you're in
2. Starts that phase through tracker
3. Updates both phase and root trackers
4. Runs implementation.py
5. Shows results

### Example Workflow from Phase Level

```bash
# 1. Navigate to phase
cd phases/phase03

# 2. Check phase-specific state
cat .state/phase_state.json

# 3. Run phase
./continue

# 4. Go back to root
cd ../../

# 5. Check overall status
./scripts/status.sh
```

---

## Complete Workflows

### Scenario 1: Linear Progress (One Phase at a Time)

```bash
# Day 1: Start Phase 0
./scripts/start_phase.sh 0
./scripts/complete_phase.sh 0

# Day 2: Continue with Phase 1
./scripts/start_phase.sh 1
./scripts/complete_phase.sh 1

# Day 3: Continue with Phase 2
./scripts/start_phase.sh 2
./scripts/complete_phase.sh 2

# And so on...
```

### Scenario 2: Work on Specific Phase

```bash
# Jump to Phase 10
cd phases/phase10

# Run it
./continue

# Complete it
cd ../../
./scripts/complete_phase.sh 10
```

### Scenario 3: Check Status Frequently

```bash
# Morning: Check where you left off
./scripts/status.sh

# Continue from current phase
CURRENT=$(python3 scripts/sync_tracker.py current)
./scripts/start_phase.sh $CURRENT

# Evening: Check progress
./scripts/status.sh --detailed
```

### Scenario 4: Parallel Development (Advanced)

```bash
# Terminal 1: Work on Phase 3
cd phases/phase03
./continue

# Terminal 2: Work on Phase 7
cd phases/phase07
./continue

# Root terminal: Monitor overall progress
./scripts/status.sh
```

---

## Continue from Where You Left Off

### ⭐ THE KILLER FEATURE ⭐

**Problem:** You shut down your system at 5pm. Next morning at 9am, where were you?

**Solution:** The tracker remembers everything.

### At Root Level

```bash
# Shut down at 5pm (middle of Phase 5)
#... system off overnight ...

# Next morning at 9am
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Option 1: Interactive
./continue
# → Shows you were on Phase 5
# → Menu option to continue Phase 5

# Option 2: Direct
./scripts/status.sh
# → See current phase
./scripts/start_phase.sh 5
# → Continue exactly where you left off
```

### At Phase Level

```bash
# Shut down at 5pm (middle of Phase 5)
cd phases/phase05
#... system off overnight ...

# Next morning at 9am
cd phases/phase05

# Just run:
./continue

# → Auto-detects Phase 5
# → Continues from saved state
# → You're back in business!
```

### How It Survives Shutdowns

```json
// Root tracker (.tracker/state.json)
{
  "current_phase": 5,
  "status": "IN_PROGRESS",
  "story_points_completed": 234,
  "last_activity": "Working on Phase 5",
  "last_updated": "2025-10-27T17:35:22"  ← Last saved state
}

// Phase tracker (phases/phase05/.state/phase_state.json)
{
  "phase_id": 5,
  "status": "IN_PROGRESS",
  "started_at": "2025-10-27T14:20:00",
  "current_task": "Audio post-processing",  ← Where you were
  "completed_tasks": ["TTS integration"]    ← What you finished
}
```

When you run `./continue` or `./scripts/start_phase.sh 5`:
1. Reads saved state
2. Shows you where you were
3. Resumes from that exact point
4. Updates timestamp to now

**You never lose progress, even after:**
- Shutdown
- Reboot
- Sleep/hibernate
- Power failure (if autosave enabled)
- Taking a break for days/weeks

---

## Multi-Machine Setup

### Scenario: Work on Different Machines

```bash
# Machine 1 (laptop): Work on Phase 0-5
./scripts/start_phase.sh 0
./scripts/complete_phase.sh 0
# ... up to Phase 5 ...

# Sync tracker to cloud/USB/git
cp -r .tracker ~/Dropbox/swarmcare-tracker/
# OR
git add .tracker phases/*/. state
git commit -m "Progress: Completed Phase 5"
git push

# Machine 2 (desktop): Continue from Phase 6
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Pull tracker state
cp -r ~/Dropbox/swarmcare-tracker/.tracker ./
# OR
git pull

# Check status
./scripts/status.sh
# → Shows Phase 5 complete, Phase 6 next

# Continue
./scripts/start_phase.sh 6
```

### Sync Strategy

```bash
# After each phase completion
./scripts/complete_phase.sh 5

# Immediately sync
rsync -avz .tracker phases/*/. state username@remote:/path/
# OR
git add .tracker phases
git commit -m "Completed Phase 5"
git push
```

---

## Troubleshooting

### Tracker Out of Sync

**Problem:** Phase state doesn't match root tracker

**Solution:**
```bash
# Re-sync all phases
python3 scripts/sync_tracker.py sync-all

# Or sync specific phase
python3 scripts/sync_tracker.py sync 5
```

### Lost Current Phase

**Problem:** Don't remember which phase you were on

**Solution:**
```bash
# Check tracker
python3 scripts/sync_tracker.py current
# → Outputs: 5

# Check detailed status
./scripts/status.sh --detailed
# → Shows all phases, marks current with 🔄
```

### Phase State File Missing

**Problem:** `.state/phase_state.json` missing for a phase

**Solution:**
```bash
# Recreate from manifest
python3 << EOF
import json
from pathlib import Path

phase_id = 5  # Change this
phase_dir = Path(f"phases/phase{phase_id:02d}")
state_dir = phase_dir / ".state"
state_dir.mkdir(exist_ok=True)

state = {
    "phase_id": phase_id,
    "phase_name": "Phase Name Here",
    "story_points": 0,
    "status": "NOT_STARTED",
    "progress_percentage": 0,
    "started_at": None,
    "completed_at": None,
    "current_task": None,
    "completed_tasks": [],
    "blocked": False,
    "blocker_description": None,
    "notes": [],
    "last_updated": None
}

with open(state_dir / "phase_state.json", 'w') as f:
    json.dump(state, f, indent=2)

print(f"✅ Recreated state file for Phase {phase_id}")
EOF
```

### Root Tracker Corrupted

**Problem:** `.tracker/state.json` is corrupted or wrong

**Solution:**
```bash
# Rebuild from phase states
python3 scripts/sync_tracker.py sync-all

# Manual reset (if needed)
./continue
# → Menu option 5: "Reset progress"
```

### Continue Script Not Working from Phase

**Problem:** `./continue` doesn't work in phase directory

**Solution:**
```bash
# Check symlink exists
ls -la continue

# Recreate symlink
ln -sf ../../scripts/run_from_phase.sh continue

# Or run directly
../../scripts/run_from_phase.sh
```

---

## Advanced Usage

### Custom Workflows

#### Validate Before Marking Complete

```bash
# Start phase
./scripts/start_phase.sh 5

# Run validation
cd phases/phase05/tests
python3 test_phase05.py

# If tests pass, mark complete
cd ../../..
./scripts/complete_phase.sh 5
```

#### Run Multiple Phases in Sequence

```bash
# Automated run (Phases 0-5)
for i in {0..5}; do
    echo "Starting Phase $i"
    ./scripts/start_phase.sh $i || break
    ./scripts/complete_phase.sh $i
    sleep 2
done
```

#### Background Execution with Progress Tracking

```bash
# Run phase in background
nohup ./scripts/start_phase.sh 5 > phase05.log 2>&1 &
PID=$!

# Monitor progress
tail -f phase05.log

# Check if still running
ps -p $PID

# When done
./scripts/complete_phase.sh 5
```

### Integration with CI/CD

```bash
# .github/workflows/phase-progress.yml
name: Phase Progress Tracker

on:
  push:
    paths:
      - 'phases/*/. state/**'
      - '.tracker/**'

jobs:
  update-progress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Sync trackers
        run: python3 scripts/sync_tracker.py sync-all
      - name: Generate progress report
        run: ./scripts/status.sh --detailed > PROGRESS.md
      - name: Commit updated progress
        run: |
          git config --global user.name "Progress Bot"
          git config --global user.email "bot@example.com"
          git add PROGRESS.md .tracker
          git commit -m "Update progress tracking"
          git push
```

### Custom Status Dashboard

```python
# custom_dashboard.py
import json
from pathlib import Path

def show_dashboard():
    with open('.tracker/state.json') as f:
        state = json.load(f)

    with open('.tracker/phase_manifest.json') as f:
        manifest = json.load(f)

    print("\n" + "="*70)
    print(f"  SWARMCARE DASHBOARD")
    print("="*70)
    print(f"  Progress: {state['progress_percentage']}%")
    print(f"  Completed: {len(state['completed_phases'])}/29 phases")
    print(f"  Story Points: {state['story_points_completed']}/1362")
    print(f"  Status: {state['status']}")
    print("="*70 + "\n")

    # Show phase breakdown
    for phase in manifest['phases'][:10]:  # First 10 phases
        phase_id = phase['phase_id']
        name = phase['name']
        sp = phase['story_points']
        status = "✅" if phase_id in state['completed_phases'] else "⏳"
        print(f"  {status} Phase {phase_id:02d}: {name} ({sp} SP)")

if __name__ == "__main__":
    show_dashboard()
```

```bash
python3 custom_dashboard.py
```

---

## Best Practices

### 1. Check Status Frequently

```bash
# Start of day
./scripts/status.sh

# After each phase
./scripts/status.sh

# End of day
./scripts/status.sh --detailed
```

### 2. Always Complete Phases

```bash
# Don't skip this!
./scripts/complete_phase.sh <phase_id>

# It updates:
# - Phase state ✅
# - Root tracker ✅
# - Progress percentage ✅
# - Story points ✅
```

### 3. Sync Regularly (Multi-Machine)

```bash
# After each phase
git add .tracker phases/*/. state
git commit -m "Phase X complete"
git push
```

### 4. Use Continue Commands

```bash
# At root
./continue

# At phase level
cd phases/phase05
./continue
```

### 5. Never Manually Edit State Files

```bash
# DON'T:
vi .tracker/state.json  # ❌ Can corrupt

# DO:
python3 scripts/sync_tracker.py complete 5  # ✅ Safe
./scripts/complete_phase.sh 5              # ✅ Safe
```

---

## Summary

### Root Level Commands
```bash
./continue                          # Interactive menu
./scripts/status.sh                 # Quick status
./scripts/status.sh --detailed      # All phases
./scripts/start_phase.sh <ID>       # Start phase
./scripts/complete_phase.sh <ID>    # Complete phase
```

### Phase Level Commands
```bash
cd phases/phase<ID>                 # Navigate
./continue                          # Run this phase
cat .state/phase_state.json         # Check state
```

### Sync Commands
```bash
python3 scripts/sync_tracker.py current        # Current phase
python3 scripts/sync_tracker.py sync <ID>      # Sync one
python3 scripts/sync_tracker.py sync-all       # Sync all
python3 scripts/sync_tracker.py start <ID>     # Mark started
python3 scripts/sync_tracker.py complete <ID>  # Mark complete
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  SWARMCARE TRACKER QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────┤
│  STATUS           ./scripts/status.sh                   │
│  START PHASE      ./scripts/start_phase.sh <ID>         │
│  COMPLETE PHASE   ./scripts/complete_phase.sh <ID>      │
│  INTERACTIVE      ./continue                            │
│  FROM PHASE DIR   cd phases/phaseXX && ./continue       │
│  SYNC ALL         python3 scripts/sync_tracker.py ...   │
└─────────────────────────────────────────────────────────┘
```

---

## You're Ready! 🚀

The tracker system is now your **best friend** for managing 1,362 story points across 29 phases.

**Key Takeaways:**
1. ✅ Always use tracker commands (not raw python3 implementation.py)
2. ✅ Can continue from where you left off anytime
3. ✅ Works at root or phase level
4. ✅ Survives shutdowns and breaks
5. ✅ Keeps everything in sync

**Next Steps:**
```bash
./scripts/status.sh                 # See current state
./scripts/start_phase.sh 0          # Start Phase 0
```

---

*Last Updated: October 27, 2025*
*Status: ✅ 100% PRODUCTION READY*
*Your Status: 🎯 READY TO TRACK PROGRESS*
