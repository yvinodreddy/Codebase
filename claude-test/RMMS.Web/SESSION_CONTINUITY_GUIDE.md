# Session Continuity Guide
## How to Resume Work After Restart/Re-login

**Purpose:** This guide ensures you can seamlessly continue your work regardless of how long you've been away - whether 5 minutes, 5 hours, or 5 days.

---

## 🎯 THE PHILOSOPHY

Your work state is preserved across sessions through:

1. **`CURRENT_SESSION.md`** - Your exact position (which step you're on)
2. **`PROGRESS_TRACKER.md`** - Overall checklist (what's done/pending)
3. **`implementation_logs/YYYY-MM-DD.md`** - Daily work history
4. **Git commits** - Code state markers
5. **Database tracking tables** - Queryable progress

**Key Principle:** You should be able to close everything, restart your computer, and know EXACTLY where to resume in under 2 minutes.

---

## ⚡ QUICK RESUME (2 Minutes)

Use this when you just took a break (same day):

### Step 1: Navigate to Project (10 seconds)
```bash
cd /home/user01/claude-test/RMMS.Web
```

### Step 2: Check Current State (30 seconds)
```bash
# Read your current position
cat CURRENT_SESSION.md
```

**You'll see:**
- Current Step: X.X - [Step Name]
- Last Completed: X.X - [Previous Step]
- Next Action: Exactly what to do next
- Files to Open: Which files you need

### Step 3: Open Required Files (60 seconds)
```bash
# Based on "Files to Open" section in CURRENT_SESSION.md
# For example:
code IMPLEMENTATION_GUIDE_STEP_BY_STEP.md
code RMMS.DataAccess/Context/ApplicationDbContext.cs
# etc.
```

### Step 4: Continue Working (immediate)
- Follow the "Next Action" from CURRENT_SESSION.md
- Refer to IMPLEMENTATION_GUIDE_STEP_BY_STEP.md for detailed steps

**Total Time:** ~2 minutes to be fully back in context

---

## 🔄 STANDARD RESUME (10 Minutes)

Use this when starting a new day or after a longer break:

### Step 1: Navigate to Project (10 seconds)
```bash
cd /home/user01/claude-test/RMMS.Web
```

### Step 2: Check for Updates (30 seconds)
```bash
# If working in a team
git pull origin main

# If solo
git status  # See if you have uncommitted changes
```

### Step 3: Review Current State (60 seconds)
```bash
# Where am I?
cat CURRENT_SESSION.md

# Shows:
# - Current Step
# - Last Completed
# - Next Action
# - Today's Plan
# - Any Blockers
```

### Step 4: Review Yesterday's Work (2 minutes)
```bash
# What did I do yesterday?
cat implementation_logs/$(date -d "yesterday" +%Y-%m-%d).md

# Or on Mac/some systems:
cat implementation_logs/$(date -v-1d +%Y-%m-%d).md

# Or manually:
ls -lt implementation_logs/ | head -5  # Find recent logs
cat implementation_logs/2025-10-05.md  # Read specific date
```

**You'll see:**
- What you completed
- Any issues you faced
- What you planned to do next
- Time spent on each task

### Step 5: Check Overall Progress (1 minute)
```bash
# How much have I completed overall?
head -30 PROGRESS_TRACKER.md

# What's my current sprint status?
grep "Sprint 1" PROGRESS_TRACKER.md -A 50 | head -30
```

### Step 6: Review Recent Commits (1 minute)
```bash
# What are the last 10 things I did?
git log --oneline -10

# See what changed in last commit
git show HEAD --stat
```

### Step 7: Verify Application State (3 minutes)
```bash
# Build to ensure everything still works
dotnet build

# If there are errors:
# - Review last commit
# - Check if database is running
# - Verify dependencies

# Run the application
dotnet run

# Open browser: https://localhost:5001
# Verify it starts without errors
# Ctrl+C to stop
```

### Step 8: Start Today's Session Log (1 minute)
```bash
# Create or append to today's log
touch implementation_logs/$(date +%Y-%m-%d).md

# Add session header
cat >> implementation_logs/$(date +%Y-%m-%d).md << EOF
# Session Log: $(date +%Y-%m-%d)
## Start Time: $(date +%H:%M:%S)

## Plan for Today:
$(cat CURRENT_SESSION.md | grep "TODAY'S PLAN" -A 10)

## Starting with:
$(cat CURRENT_SESSION.md | grep "Next Action" -A 5)

---
EOF
```

### Step 9: Open Your Workspace (1 minute)
```bash
# Open VS Code with entire solution
code .

# Or open specific files from CURRENT_SESSION.md
```

### Step 10: Continue Working
- Follow "Next Action" from CURRENT_SESSION.md
- Refer to IMPLEMENTATION_GUIDE_STEP_BY_STEP.md for detailed steps
- Update PROGRESS_TRACKER.md as you complete tasks

**Total Time:** ~10 minutes to be fully back in context with complete understanding

---

## 🏥 DEEP RESUME (30 Minutes)

Use this when you've been away for several days/weeks:

### Phase 1: Orientation (10 minutes)

```bash
cd /home/user01/claude-test/RMMS.Web

# 1. Review executive summary to recall the big picture
cat EXECUTIVE_SUMMARY.md | head -100

# 2. Review what phase you're in
cat RMMS_IMPLEMENTATION_ROADMAP.md | grep "PHASE 1" -A 50 | head -50

# 3. Check current position
cat CURRENT_SESSION.md

# 4. Review overall progress
cat PROGRESS_TRACKER.md | head -50
```

### Phase 2: Review Recent History (10 minutes)

```bash
# 1. Review last 5 work sessions
ls -lt implementation_logs/ | head -6
cat implementation_logs/[most-recent-date].md
cat implementation_logs/[second-most-recent-date].md

# 2. Review last 20 commits
git log --oneline -20

# 3. Review last tagged milestone
git tag | sort -V | tail -5
git log $(git tag | sort -V | tail -1) -1

# 4. Check what's completed vs. pending
grep "✅" PROGRESS_TRACKER.md | tail -20  # Last 20 completed
grep "❌" PROGRESS_TRACKER.md | head -20  # Next 20 to do
```

### Phase 3: Verify System State (5 minutes)

```bash
# 1. Ensure database is accessible
sqlcmd -S localhost -d RMMS_Production -Q "SELECT TOP 5 * FROM ImplementationProgress ORDER BY Id DESC"

# 2. Build solution
dotnet build

# 3. Check for any pending migrations
cd RMMS.Web
dotnet ef migrations list --context ApplicationDbContext

# 4. Run application
dotnet run
# Open browser, verify basic functionality
# Ctrl+C to stop
```

### Phase 4: Plan Restart (5 minutes)

```bash
# 1. Read the next step in detail
grep "STEP $(cat CURRENT_SESSION.md | grep "Current Step" | cut -d: -f2 | xargs)" IMPLEMENTATION_GUIDE_STEP_BY_STEP.md -A 100 | head -100

# 2. Identify what you need to review
# - Any new concepts?
# - Any documentation to re-read?
# - Any skills to refresh?

# 3. Update today's session log with restart notes
cat >> implementation_logs/$(date +%Y-%m-%d).md << EOF
# Resuming After Break
## Last Active: [Date of last log]
## Days Away: [X days]

## Recap Completed:
- Reviewed last 5 session logs
- Reviewed 20 recent commits
- Verified database connectivity
- Verified application builds and runs

## Ready to Resume:
- Current Step: [from CURRENT_SESSION.md]
- Estimated Catch-up Time: 30 minutes
- Feeling: [Confident/Need Review/Need Help]

---
EOF
```

**Total Time:** ~30 minutes to be fully back in context after extended absence

---

## 📝 DAILY WORKFLOW ROUTINE

### 🌅 MORNING ROUTINE (Every Session Start)

#### 1. Open Terminal & Navigate (10 sec)
```bash
cd /home/user01/claude-test/RMMS.Web
```

#### 2. Quick System Check (30 sec)
```bash
# Check current state
cat CURRENT_SESSION.md | head -30

# Quick progress check
echo "Overall Progress:"
grep "Overall Progress" PROGRESS_TRACKER.md
```

#### 3. Create/Update Today's Log (1 min)
```bash
# Create today's log
touch implementation_logs/$(date +%Y-%m-%d).md

# Add session start
echo "# Session Log: $(date +%Y-%m-%d)" > implementation_logs/$(date +%Y-%m-%d).md
echo "## Start Time: $(date +%H:%M:%S)" >> implementation_logs/$(date +%Y-%m-%d).md
echo "" >> implementation_logs/$(date +%Y-%m-%d).md
echo "## Today's Goal: $(cat CURRENT_SESSION.md | grep 'Current Step' | cut -d: -f2-)" >> implementation_logs/$(date +%Y-%m-%d).md
echo "" >> implementation_logs/$(date +%Y-%m-%d).md
```

#### 4. Review Plan (1 min)
```bash
# What am I doing today?
cat CURRENT_SESSION.md | grep "TODAY'S PLAN" -A 15
```

#### 5. Open Workspace (1 min)
```bash
# Open VS Code
code .

# Open key files in tabs
# - CURRENT_SESSION.md
# - PROGRESS_TRACKER.md
# - IMPLEMENTATION_GUIDE_STEP_BY_STEP.md
```

**Morning Routine Total:** ~3 minutes

---

### 🎯 DURING WORK

#### After Completing Each Step:

**1. Update PROGRESS_TRACKER.md (30 sec)**
```markdown
Change:
- [ ] 1.3.1 ❌ Create Customer.cs model

To:
- [x] 1.3.1 ✅ Create Customer.cs model
```

**2. Commit Your Code (30 sec)**
```bash
git add .
git commit -m "STEP 1.3.1: Customer model created"
```

**3. Update CURRENT_SESSION.md (1 min)**
- Move completed step to "Last Completed"
- Update "Current Step" to next step
- Update "Next Action"
- Update timestamp

**4. Log in Daily Log (30 sec)**
```bash
echo "- ✅ $(date +%H:%M) Completed: Step 1.3.1 - Customer model created" >> implementation_logs/$(date +%Y-%m-%d).md
```

**5. Update Database Tracking (30 sec)**
```sql
UPDATE ImplementationProgress
SET Status = 'Completed', CompletedDate = GETDATE(), GitCommitHash = '[commit-hash]'
WHERE StepNumber = '1.3.1';
```

**Per-Step Overhead:** ~3 minutes (ensures you never lose your place)

---

### 🌙 EVENING ROUTINE (End of Session)

#### 1. Commit Any WIP (1 min)
```bash
# If you have work in progress
git add .
git commit -m "WIP: [description of what you're working on]"
```

#### 2. Update CURRENT_SESSION.md (2 min)
- Update "Next Action" with exactly what to do tomorrow
- Update "Blockers/Issues" if any
- Update "Today's Progress" summary
- Save and commit

#### 3. Complete Today's Log (3 min)
```bash
cat >> implementation_logs/$(date +%Y-%m-%d).md << EOF

## End Time: $(date +%H:%M:%S)

## Completed Today:
[List what you finished]

## In Progress:
[What you're currently working on]

## Blockers/Issues:
[Any problems faced]

## Tomorrow's Plan:
[What to start with tomorrow]

## Notes:
[Any important observations]

---
Total Time: [X hours]
EOF
```

#### 4. Final Session Commit (30 sec)
```bash
git add CURRENT_SESSION.md implementation_logs/$(date +%Y-%m-%d).md PROGRESS_TRACKER.md
git commit -m "SESSION END: $(date +%Y-%m-%d) - [brief summary]"

# Optional: Push if team environment
git push origin main
```

#### 5. Close Gracefully
- Close all applications
- No force-shutdowns
- Git state is clean and pushed

**Evening Routine Total:** ~7 minutes

---

## 🚨 EMERGENCY RECOVERY PROCEDURES

### If You Forgot to Update Tracking Files:

**1. Reconstruct from Git History:**
```bash
# See what you did
git log --oneline --since="3 days ago"

# See what changed
git diff HEAD~5 HEAD --stat

# Recreate session log
touch implementation_logs/$(date -d "yesterday" +%Y-%m-%d).md
echo "# Reconstructed from Git History" >> implementation_logs/$(date -d "yesterday" +%Y-%m-%d).md
git log --since="yesterday" --format="- %s (committed: %ar)" >> implementation_logs/$(date -d "yesterday" +%Y-%m-%d).md
```

**2. Update PROGRESS_TRACKER.md:**
- Review git commits
- Mark corresponding tasks as completed
- Update progress percentages

**3. Update CURRENT_SESSION.md:**
- Find last commit
- Set current step to next logical step
- Set next action

### If Git State is Messy:

```bash
# See what's uncommitted
git status

# Stash changes temporarily
git stash save "WIP - before cleanup"

# Return to clean state
git reset --hard HEAD

# Restore your changes
git stash pop

# Commit properly
git add .
git commit -m "RECOVERED: [description]"
```

### If Database is Out of Sync:

```sql
-- Check what database thinks is last completed
SELECT TOP 10 * FROM ImplementationProgress ORDER BY Id DESC;

-- Compare with Git
-- Update if needed
UPDATE ImplementationProgress
SET Status = 'Completed', CompletedDate = GETDATE()
WHERE StepNumber IN ('1.3.1', '1.3.2', /* etc */);
```

---

## 🎯 STATE FILES REFERENCE

| File | Purpose | Update Frequency | Use For |
|------|---------|------------------|---------|
| CURRENT_SESSION.md | Exact current position | After each step | "Where am I?" |
| PROGRESS_TRACKER.md | Overall checklist | After each step | "What's done?" |
| implementation_logs/*.md | Daily history | During work | "What did I do?" |
| Git commits | Code checkpoints | After each step | "Code state" |
| Database tables | Queryable progress | After each step | "Verifiable progress" |

---

## ✅ SESSION CONTINUITY CHECKLIST

### Before Taking a Break:
- [ ] All work committed to Git
- [ ] CURRENT_SESSION.md updated with next action
- [ ] PROGRESS_TRACKER.md updated with completed tasks
- [ ] Daily log updated with current status
- [ ] No compiler errors
- [ ] Database tracking tables updated

### When Resuming:
- [ ] Navigated to project directory
- [ ] Read CURRENT_SESSION.md
- [ ] Checked for git updates (if team)
- [ ] Reviewed yesterday's log (if new day)
- [ ] Checked overall progress
- [ ] Verified application builds
- [ ] Started today's session log
- [ ] Opened required files
- [ ] Ready to continue with "Next Action"

---

## 📞 QUICK HELP

**"Where do I start each morning?"**
→ Read CURRENT_SESSION.md, then follow "Next Action"

**"I forgot what I did yesterday"**
→ `cat implementation_logs/$(date -d "yesterday" +%Y-%m-%d).md`

**"I don't remember which phase I'm in"**
→ `cat PROGRESS_TRACKER.md | head -30`

**"What's my next milestone?"**
→ `cat PROGRESS_TRACKER.md | grep "Sprint" | head -5`

**"I need to see the big picture again"**
→ `cat EXECUTIVE_SUMMARY.md`

**"How do I implement the current step?"**
→ `grep "STEP $(cat CURRENT_SESSION.md | grep Current | cut -d: -f2)" IMPLEMENTATION_GUIDE_STEP_BY_STEP.md -A 50`

---

**Document Type:** Session Continuity Guide
**Purpose:** Never lose your place, regardless of interruptions
**Key Principle:** 2-minute resume time for any break length
