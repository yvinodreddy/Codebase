# SWARMCARE QUICK START GUIDE
## Get Started in 5 Minutes

**Version:** 2.1 Ultimate

---

## 🚀 THE ONE COMMAND YOU NEED

### After Every Login/Restart:

```bash
cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py resume
```

**This command:**
- Shows your current phase and progress
- Lists completed user stories
- Shows next steps
- Displays any blockers
- Tells you exactly what to do next

---

## 🎯 FIRST TIME SETUP (Do This Once)

```bash
# 1. Go to project directory
cd /home/user01/claude-test/SwarmCare

# 2. Initialize project (creates state files)
python scripts/swarmcare_cli.py init

# 3. Start Phase 0
python scripts/swarmcare_cli.py start-phase --phase 0

# 4. You're ready to code!
```

---

## 📋 DAILY WORKFLOW

### Morning (Start of Day)
```bash
# Resume from last checkpoint
python scripts/swarmcare_cli.py resume
```

### During Day (As You Work)
```bash
# Mark user stories complete as you finish them
python scripts/swarmcare_cli.py complete-story --story "1.1"
python scripts/swarmcare_cli.py complete-story --story "1.2"
# ... etc
```

### Evening (End of Day)
```bash
# Create checkpoint to save progress
python scripts/swarmcare_cli.py checkpoint --message "Completed Neo4j setup"

# Generate progress report
python scripts/swarmcare_cli.py report
```

---

## 📊 USEFUL COMMANDS

### Check Progress
```bash
# Show dashboard
python scripts/swarmcare_cli.py dashboard

# Generate detailed report
python scripts/swarmcare_cli.py report

# List all phases
python scripts/swarmcare_cli.py list-phases
```

### Manage Phases
```bash
# Start a specific phase
python scripts/swarmcare_cli.py start-phase --phase 0

# Start with force (skip prerequisites check)
python scripts/swarmcare_cli.py start-phase --phase 2 --force
```

### Track Work
```bash
# Complete a user story
python scripts/swarmcare_cli.py complete-story --story "2.3"

# Complete with notes
python scripts/swarmcare_cli.py complete-story --story "2.3" --notes "RAG pipeline working"

# Create manual checkpoint
python scripts/swarmcare_cli.py checkpoint --message "Your message here"
```

### Help
```bash
# Show all commands
python scripts/swarmcare_cli.py --help

# Show command-specific help
python scripts/swarmcare_cli.py start-phase --help
```

---

## 📖 WHERE TO FIND THINGS

### User Stories (What to Build)
```bash
# Open this file:
cat IMPLEMENTATION_MASTER_PLAN.md

# Or use your editor:
code IMPLEMENTATION_MASTER_PLAN.md
```

### Phase Tracking Info
```bash
cat PHASE_TRACKER.md
```

### Project Plan (Detailed Strategy)
```bash
ls ProjectPlan/
cat ProjectPlan/01_MASTER_PROJECT_PLAN.md
```

### Current State
```bash
# Your progress is stored here:
cat .phase_state/current_phase.json
cat .phase_state/completed_stories.json
```

---

## 🔄 RESUMING AFTER LOGOUT

```bash
# System restarted? Session ended? No problem!

cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py resume

# Output shows exactly where you left off:
# - Current phase
# - Completed stories
# - Next steps
# - Blockers
```

### Example Resume Output:
```
==================================================
SWARMCARE PROJECT RESUMPTION
==================================================

Current Phase: Phase 1 - RAG Heat System
Status: IN_PROGRESS
Progress: 35% (21/60 story points completed)

Last Updated: 2025-10-31 18:45:00

Completed User Stories:
  ✓ 2.1: Document Ingestion Pipeline
  ✓ 2.2: Medical NLP Entity Extraction

Next Steps:
  1. Complete User Story 2.3: RAG Query Pipeline
  2. Start User Story 2.4: Knowledge Graph Explorer UI

Blockers: None

Recommended Command:
$ python scripts/swarmcare_cli.py dashboard
==================================================
```

---

## 🎯 THE MAGIC OF STATE PERSISTENCE

### What Gets Saved Automatically

Every time you run a command, these files are updated:
- `.phase_state/current_phase.json` - Your current position
- `.phase_state/completed_stories.json` - All completed work
- `.phase_state/execution_log.json` - History of actions
- `.phase_state/checkpoints/` - Restore points

### Commit to Git!
```bash
# Save your progress to Git (do this daily!)
git add .phase_state/
git commit -m "Phase 2 progress: 50% complete"
git push origin main
```

**Why?**
- Never lose progress
- Team can see your work
- Resume on different machine
- Rollback if needed

---

## 🚀 PARALLEL EXECUTION (Advanced)

### Running Multiple Phases at Once

```bash
# Terminal 1: Work on RAG Heat (Phase 1)
cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py start-phase --phase 1

# Terminal 2: Work on SWARMCARE Agents (Phase 2)
cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py start-phase --phase 2 --parallel

# Terminal 3: Work on Frontend (Phase 4)
cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py start-phase --phase 4 --parallel
```

**Note:** Only run independent phases in parallel!

---

## 📈 TRACKING SUCCESS

### Story Points
- **Total:** 1,362 story points
- **Epic 1 (Phase 0):** 37 points
- **Epic 2 (Phase 1):** 60 points
- ... etc

### Estimated Timeline
- **Aggressive:** 11 weeks (50 points/week)
- **Standard:** 19 weeks (30 points/week)
- **Ultra-Aggressive:** 8 weeks (70 points/week)

### Check Your Velocity
```bash
python scripts/swarmcare_cli.py dashboard

# Shows:
# - Overall progress
# - Completed vs. total story points
# - Current velocity (points/week)
# - Estimated completion date
```

---

## 🆘 TROUBLESHOOTING

### Command Not Found
```bash
# Make sure you're in the right directory
cd /home/user01/claude-test/SwarmCare

# Make sure script is executable
chmod +x scripts/swarmcare_cli.py
```

### State Files Missing
```bash
# Reinitialize (safe, won't overwrite existing files)
python scripts/swarmcare_cli.py init
```

### Wrong Phase Showing
```bash
# Check current state
cat .phase_state/current_phase.json

# If needed, start the correct phase
python scripts/swarmcare_cli.py start-phase --phase X --force
```

### Lost Progress
```bash
# Restore from Git (if you committed)
git checkout .phase_state/

# Or restore from checkpoint
ls .phase_state/checkpoints/
# Manually restore from checkpoint_YYYYMMDD_HHMMSS.json
```

---

## 🎓 LEARNING THE SYSTEM

### 5-Minute Read
1. **README.md** - Project overview
2. **This file** - Quick start

### 30-Minute Read
1. **IMPLEMENTATION_MASTER_PLAN.md** - All user stories
2. **PHASE_TRACKER.md** - Execution system

### 2-Hour Deep Dive
1. All of the above
2. **ProjectPlan/01_MASTER_PROJECT_PLAN.md**
3. **ProjectPlan/04_TECHNICAL_ARCHITECTURE_INFRASTRUCTURE.md**
4. **ProjectPlan/11_AGGRESSIVE_ONE_MONTH_MVP_PLAN.md** (if doing 30-day sprint)

---

## 💡 PRO TIPS

### Tip 1: Resume Every Time
```bash
# Make this muscle memory:
cd /home/user01/claude-test/SwarmCare && python scripts/swarmcare_cli.py resume
```

### Tip 2: Checkpoint Often
```bash
# After every major accomplishment:
python scripts/swarmcare_cli.py checkpoint --message "Completed RAG pipeline"
```

### Tip 3: Commit State Files
```bash
# Daily Git commit ritual:
git add .phase_state/
git commit -m "Progress update"
git push
```

### Tip 4: Check Dashboard Daily
```bash
# Start your day with:
python scripts/swarmcare_cli.py dashboard
```

### Tip 5: Read User Stories
```bash
# Before starting work each day:
grep -A 20 "User Story X.Y" IMPLEMENTATION_MASTER_PLAN.md
```

---

## 🎯 YOUR FIRST DAY

### Step-by-Step First Day Guide

```bash
# 1. Initialize (first time only)
cd /home/user01/claude-test/SwarmCare
python scripts/swarmcare_cli.py init

# 2. Start Phase 0
python scripts/swarmcare_cli.py start-phase --phase 0

# 3. Read Phase 0 user stories
grep -A 50 "Epic 1: Foundation" IMPLEMENTATION_MASTER_PLAN.md

# 4. Work on User Story 1.1: Development Environment Setup
# ... set up Python, Node.js, Docker, etc ...

# 5. Mark complete when done
python scripts/swarmcare_cli.py complete-story --story "1.1"

# 6. Work on User Story 1.2: Cloud Infrastructure
# ... set up GCP/AWS, Kubernetes, etc ...

# 7. Mark complete
python scripts/swarmcare_cli.py complete-story --story "1.2"

# 8. End of day checkpoint
python scripts/swarmcare_cli.py checkpoint --message "Day 1: Dev env and cloud infra"

# 9. Commit to Git
git add .phase_state/
git commit -m "Day 1 complete"
git push
```

### Day 2 and Beyond
```bash
# Start of day
python scripts/swarmcare_cli.py resume

# ... work on next user stories ...

# End of day
python scripts/swarmcare_cli.py checkpoint --message "Day 2 complete"
git add .phase_state/ && git commit -m "Day 2 progress" && git push
```

---

## 🎉 YOU'RE READY!

### The Essential Command (Memorize This!)

```bash
cd /home/user01/claude-test/SwarmCare && python scripts/swarmcare_cli.py resume
```

**Use it:**
- After every login
- After every restart
- When you forget where you were
- When starting your day
- When showing progress to team

### Success Formula

1. **Resume** → See where you are
2. **Work** → Implement user stories
3. **Complete** → Mark stories done
4. **Checkpoint** → Save progress
5. **Commit** → Push to Git
6. **Repeat** → Until all 1,362 points done

---

**You have everything you need for 100% success. Let's build! 🚀**

---

**Document Version:** 1.0
**Last Updated:** 2025-10-31
