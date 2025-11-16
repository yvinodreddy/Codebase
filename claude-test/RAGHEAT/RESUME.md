# RAGHEAT - Resume Guide
## Continue Implementation From Where You Left Off

**Last Updated:** 2025-10-25
**Current Phase:** PHASE 0 - INITIALIZATION
**Progress:** 0.3% (1/339 tasks)

---

## QUICK RESUME COMMAND

```bash
# Navigate to project directory
cd /home/user01/claude-test/RAGHEAT

# Check current status
./scripts/check_status.sh

# Resume implementation
./scripts/resume_implementation.sh
```

---

## MANUAL RESUME PROCESS

### Step 1: Check Current State

```bash
# View current phase and progress
cat PROJECT_STATE.json | jq '.current_phase'

# View next actions
cat PROJECT_STATE.json | jq '.next_actions'

# View completed tasks
cat PROJECT_STATE.json | jq '.completed_tasks'
```

**Expected Output:**
```json
{
  "phase_number": 0,
  "phase_name": "INITIALIZATION",
  "status": "in_progress",
  "progress_percentage": 5
}
```

### Step 2: Review Implementation Plan

```bash
# Open implementation plan
cat IMPLEMENTATION_PLAN_WORLD_CLASS.md

# Check current phase details
grep -A 50 "PHASE 0:" IMPLEMENTATION_PLAN_WORLD_CLASS.md
```

### Step 3: Continue Execution

**Based on Current Phase:**

#### If in PHASE 0 (INITIALIZATION):
```bash
# Complete remaining initialization tasks:
# 1. Create directory structure
# 2. Initialize Git repository
# 3. Setup development environment
# 4. Configure project templates

# Next command to run:
claude-code "Continue RAGHEAT implementation from PHASE 0. Current task: Create complete directory structure."
```

#### If in PHASE 1 (FOUNDATION):
```bash
# Check which day of Phase 1
grep "Day.*COMPLETED" PROJECT_STATE.json

# Resume Phase 1
claude-code "Continue RAGHEAT Phase 1 implementation. Check PROJECT_STATE.json for current day and resume tasks."
```

#### If in PHASE 2-6:
```bash
# Same pattern for all phases
claude-code "Continue RAGHEAT implementation from [CURRENT_PHASE]. Check PROJECT_STATE.json and resume."
```

---

## STATE SYNCHRONIZATION (Multi-Instance)

If running multiple concurrent instances:

### Before Starting Work on an Instance

```bash
# Pull latest state from Git
git pull origin main

# Check for conflicts
git diff PROJECT_STATE.json

# Resolve conflicts if any
# Update your instance configuration
```

### After Completing Tasks

```bash
# Update PROJECT_STATE.json
# Commit changes
git add PROJECT_STATE.json
git commit -m "Update: Completed tasks for Phase X"
git push origin main

# Notify other instances
./scripts/notify_state_change.sh
```

---

## PHASE-SPECIFIC RESUME GUIDES

### PHASE 0: INITIALIZATION

**Current Status:** IN PROGRESS (5%)

**Remaining Tasks:**
1. ✅ Create PROJECT_STATE.json (COMPLETED)
2. ✅ Create USER_STORIES_COMPREHENSIVE.md (COMPLETED)
3. ✅ Create IMPLEMENTATION_PLAN_WORLD_CLASS.md (COMPLETED)
4. ⏳ Create complete directory structure (IN PROGRESS)
5. ⏳ Create RESUME.sh script
6. ⏳ Initialize Git repository
7. ⏳ Setup development environment guide

**Next Command:**
```bash
claude-code "Continue RAGHEAT PHASE 0. Next task: Create complete project directory structure with all folders and README files."
```

---

### PHASE 1: FOUNDATION & INFRASTRUCTURE

**Prerequisites:**
- Phase 0 complete
- Git repository initialized
- Development environment setup

**Start Command:**
```bash
# Day 1: Neo4j Setup
claude-code "Start RAGHEAT Phase 1, Day 1: Neo4j Database Infrastructure. Implement US-001, US-002, US-003 from USER_STORIES_COMPREHENSIVE.md"
```

**Daily Resume Pattern:**
```bash
# Check which day
cat PROJECT_STATE.json | jq '.phases.phase_1.current_day'

# Resume that day
claude-code "Resume RAGHEAT Phase 1, Day [X]. Check PROJECT_STATE.json for tasks."
```

---

### PHASE 2: CORE ALGORITHMS

**Prerequisites:**
- Phase 1 complete (all infrastructure working)
- Neo4j operational
- FastAPI running
- CI/CD pipeline active

**Start Command:**
```bash
# Week 1, Day 8: Heat Diffusion Engine
claude-code "Start RAGHEAT Phase 2, Week 1, Day 8: Implement heat diffusion engine (US-011)"
```

---

### PHASE 3: MULTI-AGENT SYSTEM

**Prerequisites:**
- Phase 2 complete (heat diffusion engine working)
- Data pipelines operational

**Start Command:**
```bash
# Week 1, Day 22: Fundamental Analyst Agent
claude-code "Start RAGHEAT Phase 3, Week 1, Day 22: Implement fundamental analyst agent (US-018)"
```

---

### PHASE 4: FRONTEND

**Prerequisites:**
- Phase 3 complete (all agents working)
- Backend APIs functional

**Start Command:**
```bash
# Day 36: React Dashboard
claude-code "Start RAGHEAT Phase 4, Day 36: Build React dashboard foundation"
```

---

### PHASE 5: INTEGRATION & TESTING

**Prerequisites:**
- Phases 1-4 complete
- All components implemented

**Start Command:**
```bash
# Day 46: End-to-End Integration
claude-code "Start RAGHEAT Phase 5, Day 46: End-to-end system integration testing"
```

---

### PHASE 6: PRODUCTION DEPLOYMENT

**Prerequisites:**
- All testing complete
- No critical bugs
- Security audit passed

**Start Command:**
```bash
# Day 56: Production Infrastructure
claude-code "Start RAGHEAT Phase 6, Day 56: Setup production infrastructure"
```

---

## TROUBLESHOOTING RESUME ISSUES

### Issue: "I don't know what phase I'm in"

**Solution:**
```bash
# Check project state
cat PROJECT_STATE.json | jq '.current_phase'

# Check implementation plan
grep "Status:.*IN PROGRESS" IMPLEMENTATION_PLAN_WORLD_CLASS.md
```

### Issue: "PROJECT_STATE.json is corrupted"

**Solution:**
```bash
# Restore from Git history
git checkout HEAD~1 PROJECT_STATE.json

# Or restore from backup
cp .backups/PROJECT_STATE.json.backup PROJECT_STATE.json
```

### Issue: "Multiple instances out of sync"

**Solution:**
```bash
# Force pull latest state
git fetch origin main
git reset --hard origin/main

# Or use merge strategy
git pull --rebase origin main
```

### Issue: "Task marked complete but not actually done"

**Solution:**
```bash
# Edit PROJECT_STATE.json manually
vim PROJECT_STATE.json

# Or use update script
./scripts/update_task_status.sh TASK_ID incomplete
```

---

## CHECKPOINTS & BACKUPS

### Automatic Checkpoints

The system automatically creates checkpoints every 4 hours:
- Location: `.backups/PROJECT_STATE_[timestamp].json`
- Retention: Last 10 checkpoints

### Manual Checkpoint

```bash
# Create manual checkpoint
./scripts/create_checkpoint.sh "Before starting Phase X"

# List checkpoints
ls -ltr .backups/
```

### Restore from Checkpoint

```bash
# List available checkpoints
./scripts/list_checkpoints.sh

# Restore specific checkpoint
./scripts/restore_checkpoint.sh 2025-10-25_20-00-00
```

---

## PROGRESS TRACKING

### View Overall Progress

```bash
# Simple progress
cat PROJECT_STATE.json | jq '.overall_progress_percentage'

# Detailed breakdown
./scripts/show_progress.sh

# Progress chart (ASCII)
./scripts/progress_chart.sh
```

**Expected Output:**
```
RAGHEAT Implementation Progress
================================
Overall: 0.3% (1/339 tasks)

Phase 0: ████░░░░░░░░░░░░░░░░ 5%   (1/15 tasks)
Phase 1: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/45 tasks)
Phase 2: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/67 tasks)
Phase 3: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/89 tasks)
Phase 4: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/52 tasks)
Phase 5: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/43 tasks)
Phase 6: ░░░░░░░░░░░░░░░░░░░░ 0%   (0/28 tasks)
```

---

## CONCURRENT INSTANCE COORDINATION

### Setup New Instance

```bash
# Clone repository
git clone [repo-url] ragheat-instance-2
cd ragheat-instance-2

# Register instance
./scripts/register_instance.sh "backend-team" "phase_2"

# Check instance assignment
cat PROJECT_STATE.json | jq '.concurrent_instances.current_instances'
```

### Daily Sync Between Instances

```bash
# Morning sync (before starting work)
./scripts/sync_instances.sh pull

# Evening sync (after completing work)
./scripts/sync_instances.sh push
```

### Resolve Instance Conflicts

```bash
# If two instances edited same file
./scripts/resolve_instance_conflict.sh

# Or manual resolution
git mergetool
```

---

## DAILY WORKFLOW

### Morning Routine

```bash
# 1. Navigate to project
cd /home/user01/claude-test/RAGHEAT

# 2. Pull latest changes (if multi-instance)
git pull origin main

# 3. Check current status
./scripts/check_status.sh

# 4. Review today's tasks
cat PROJECT_STATE.json | jq '.next_actions'

# 5. Start work
claude-code "Resume RAGHEAT implementation. Check PROJECT_STATE.json and continue."
```

### End of Day Routine

```bash
# 1. Update task status
./scripts/update_progress.sh

# 2. Commit changes
git add .
git commit -m "Day X progress: [summary]"
git push origin main

# 3. Create checkpoint
./scripts/create_checkpoint.sh "End of Day X"

# 4. Review tomorrow's tasks
cat IMPLEMENTATION_PLAN_WORLD_CLASS.md | grep "Day $(expr $(date +%d) + 1):"
```

---

## EMERGENCY PROCEDURES

### Critical Bug Found

```bash
# 1. Stop all work
./scripts/pause_all_instances.sh

# 2. Create bug report
./scripts/create_bug_report.sh "Critical bug description"

# 3. Fix bug
# ... implementation ...

# 4. Resume work
./scripts/resume_all_instances.sh
```

### System Rollback Needed

```bash
# 1. Identify last good state
./scripts/list_checkpoints.sh

# 2. Restore
./scripts/restore_checkpoint.sh [timestamp]

# 3. Verify
./scripts/verify_system.sh

# 4. Resume
claude-code "Resume from restored checkpoint"
```

---

## CLAUDE CODE INTEGRATION

### Optimal Resume Prompt

```
I need to continue the RAGHEAT implementation project.

Current state:
- Phase: [check PROJECT_STATE.json]
- Progress: [X]%
- Last completed: [task]

Please:
1. Read PROJECT_STATE.json to understand current status
2. Read IMPLEMENTATION_PLAN_WORLD_CLASS.md for next steps
3. Check USER_STORIES_COMPREHENSIVE.md for task details
4. Continue implementation from where we left off
5. Update PROJECT_STATE.json as you complete tasks

Let me know what you'll work on next.
```

### Context Files for Claude

Always provide these files to Claude Code:
1. `PROJECT_STATE.json` - Current status
2. `IMPLEMENTATION_PLAN_WORLD_CLASS.md` - Overall plan
3. `USER_STORIES_COMPREHENSIVE.md` - Task details
4. `Agents/agents.yaml` - Agent specifications
5. `Agents/tasks.yaml` - Task definitions

---

## COMPLETION CRITERIA

### How to Know When Done

**Phase Complete:**
```bash
# Check phase completion
cat PROJECT_STATE.json | jq '.phases.phase_X.status'
# Should return: "completed"

# All tasks done
cat PROJECT_STATE.json | jq '.phases.phase_X.tasks_completed == .phases.phase_X.tasks_total'
# Should return: true
```

**Project Complete:**
```bash
# Check overall completion
cat PROJECT_STATE.json | jq '.overall_progress_percentage'
# Should return: 100

# All phases completed
./scripts/verify_completion.sh
# Should show all green checkmarks
```

---

## SUPPORT & HELP

### Getting Unstuck

1. **Check documentation:**
   - README.md
   - IMPLEMENTATION_PLAN_WORLD_CLASS.md
   - USER_STORIES_COMPREHENSIVE.md

2. **Check project state:**
   ```bash
   ./scripts/check_status.sh
   ```

3. **Ask Claude Code:**
   ```
   I'm stuck on RAGHEAT implementation.
   Current issue: [describe]
   Files to check: PROJECT_STATE.json, [relevant files]
   Please help me resume.
   ```

---

**Last Updated:** 2025-10-25
**Version:** 1.0.0

**Ready to resume? Run:**
```bash
./scripts/resume_implementation.sh
```

**Or start fresh from current phase:**
```bash
claude-code "Continue RAGHEAT implementation from current phase. Check PROJECT_STATE.json."
```
