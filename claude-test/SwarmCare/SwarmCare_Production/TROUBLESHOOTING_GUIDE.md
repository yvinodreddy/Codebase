# 🔧 COMPREHENSIVE TROUBLESHOOTING GUIDE
## Your Emergency Handbook - Quick Solutions to Common Problems

**Purpose:** When something breaks, find the fix fast
**Format:** Problem → Cause → Solution

---

## 🆘 EMERGENCY: SYSTEM COMPLETELY BROKEN

### "Everything is broken, nothing works!"

**STOP. BREATHE. DO THIS:**

```bash
# Step 1: Stop all running processes
pkill -f "implementation.py"
pkill -f "python"

# Step 2: Go to safe location
cd /home/user01/claude-test/SwarmCare

# Step 3: Check if backup exists
ls -lh SwarmCare_BASELINE_*.tar.gz

# Step 4: Restore from backup
tar -xzf SwarmCare_BASELINE_YYYYMMDD.tar.gz -C SwarmCare_Production_RESTORED

# Step 5: Verify restored version
cd SwarmCare_Production_RESTORED
python3 comprehensive_validation_tests.py

# If validation passes, you're back to working state!
```

**If no backup exists:**
```bash
# Re-clone from Git (if you pushed to GitHub)
cd /home/user01/claude-test/SwarmCare
git clone <your-repo-url> SwarmCare_Production_RESTORED
```

---

## 📚 TABLE OF CONTENTS

0. [**Tracker Issues**](#tracker-issues) ⭐ **NEW - MOST COMMON!**
1. [Import Errors](#import-errors)
2. [Permission Errors](#permission-errors)
3. [Python Errors](#python-errors)
4. [Validation Failures](#validation-failures)
5. [Phase Execution Errors](#phase-execution-errors)
6. [Agent Framework Issues](#agent-framework-issues)
7. [Guardrail Problems](#guardrail-problems)
8. [File System Issues](#file-system-issues)
9. [Performance Problems](#performance-problems)
10. [VS 2022 Issues](#vs-2022-issues)
11. [Docker/Container Issues](#docker-container-issues)
12. [Network/API Issues](#network-api-issues)

---

## 0️⃣ TRACKER ISSUES ⭐

**Most common issues with the progress tracking system**

### Problem: "Tracker state file not found"

**Symptoms:**
```
Error: Tracker state file not found
Expected: /home/user01/claude-test/SwarmCare/SwarmCare_Production/.tracker/state.json
```

**Cause:** `.tracker` directory missing or corrupted

**Solution:**
```bash
# Check if directory exists
ls -la .tracker/

# If missing, verify you're in the right directory
pwd
# Should be: /home/user01/claude-test/SwarmCare/SwarmCare_Production

# If you're in the right place, check if backup exists
ls ../SwarmCare_BASELINE_*.tar.gz

# Restore from backup
cd ..
tar -xzf SwarmCare_BASELINE_*.tar.gz
cd SwarmCare_Production

# Verify tracker restored
./scripts/status.sh
```

### Problem: "Tracker out of sync - phase state doesn't match"

**Symptoms:**
```
Phase 5 shows COMPLETED in .state but NOT_STARTED in root tracker
OR
Root tracker shows Phase 10 but you only completed Phase 5
```

**Cause:** Phase state and root tracker not synced

**Solution:**
```bash
# Re-sync all phases to root tracker
python3 scripts/sync_tracker.py sync-all

# Or sync specific phase
python3 scripts/sync_tracker.py sync 5

# Verify sync worked
./scripts/status.sh --detailed
```

### Problem: "Lost my place - don't know which phase I'm on"

**Symptoms:**
```
Worked on project yesterday, forgot which phase I was on
```

**Cause:** Forgot to check tracker before shutting down

**Solution:**
```bash
# Check current phase
python3 scripts/sync_tracker.py current
# Output: 5

# Check detailed status
./scripts/status.sh --detailed
# Shows all phases, marks current with 🔄

# Continue from there
./scripts/start_phase.sh 5
```

### Problem: "Phase state file missing for a phase"

**Symptoms:**
```
phases/phase05/.state/phase_state.json not found
```

**Cause:** `.state` directory or file was deleted

**Solution:**
```bash
# Recreate phase state file
python3 << 'EOF'
import json
from pathlib import Path

phase_id = 5  # ← Change to your phase
phase_dir = Path(f"phases/phase{phase_id:02d}")
state_dir = phase_dir / ".state"
state_dir.mkdir(exist_ok=True)

# Read phase info from manifest
with open('.tracker/phase_manifest.json') as f:
    manifest = json.load(f)
    phase_info = next(p for p in manifest['phases'] if p['phase_id'] == phase_id)

state = {
    "phase_id": phase_id,
    "phase_name": phase_info['name'],
    "story_points": phase_info['story_points'],
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

### Problem: "Continue script doesn't work from phase directory"

**Symptoms:**
```
cd phases/phase05
./continue
bash: ./continue: No such file or directory
```

**Cause:** Symlink not created for that phase

**Solution:**
```bash
# Recreate symlink for one phase
cd phases/phase05
ln -sf ../../scripts/run_from_phase.sh continue

# Or recreate for ALL phases
cd ../../
for i in {0..28}; do
    ln -sf ../../scripts/run_from_phase.sh phases/phase$(printf "%02d" $i)/continue
done
```

### Problem: "Tracker shows wrong progress percentage"

**Symptoms:**
```
Completed 3 phases (131 points) but progress shows 5%
```

**Cause:** Root tracker not updated after phase completion

**Solution:**
```bash
# Manually mark phases as complete
python3 scripts/sync_tracker.py complete 0
python3 scripts/sync_tracker.py complete 1
python3 scripts/sync_tracker.py complete 2

# Or resync all
python3 scripts/sync_tracker.py sync-all

# Check corrected progress
./scripts/status.sh
```

### Problem: "Multi-machine sync issues"

**Symptoms:**
```
Worked on Machine 1, pulled to Machine 2, tracker shows old state
```

**Cause:** Forgot to commit/push tracker changes

**Solution:**

**Machine 1 (after working):**
```bash
# Commit tracker state
git add .tracker phases/*/. state
git commit -m "Progress: Completed Phase 5"
git push
```

**Machine 2 (before working):**
```bash
# Pull latest tracker state
git pull

# Verify sync
./scripts/status.sh

# Continue
./scripts/start_phase.sh 6
```

### Problem: "Accidentally reset tracker progress"

**Symptoms:**
```
Used ./continue menu option 5 "Reset progress" by mistake
All progress lost!
```

**Cause:** Accidentally reset tracker

**Solution:**
```bash
# Restore from git (if committed)
git checkout .tracker/state.json
git checkout phases/*/. state/phase_state.json

# Or restore from backup
cd ..
tar -xzf SwarmCare_BASELINE_*.tar.gz --wildcards '*.tracker/*' '*/.state/*'

# Verify restored
cd SwarmCare_Production
./scripts/status.sh
```

### Problem: "Scripts not executable"

**Symptoms:**
```
./scripts/status.sh
bash: ./scripts/status.sh: Permission denied
```

**Cause:** Scripts lost execute permission

**Solution:**
```bash
# Make all scripts executable
chmod +x scripts/*.sh scripts/*.py
chmod +x continue
chmod +x phases/*/continue

# Verify
ls -la scripts/status.sh
# Should show: -rwxr-xr-x
```

### Problem: "Python script errors in sync_tracker.py"

**Symptoms:**
```
python3 scripts/sync_tracker.py current
Traceback (most recent call last):
  ...
KeyError: 'current_phase'
```

**Cause:** Root tracker JSON corrupted or malformed

**Solution:**
```bash
# Backup current (corrupted) tracker
cp .tracker/state.json .tracker/state.json.backup

# Restore from git
git checkout .tracker/state.json

# Or manually fix JSON
vi .tracker/state.json
# Fix JSON syntax errors

# Or reset (CAUTION: loses progress!)
./continue
# Menu option 5: Reset progress
```

**For complete tracker documentation:** See `TRACKER_USAGE_GUIDE.md`

---

## 1️⃣ IMPORT ERRORS

### "ModuleNotFoundError: No module named 'X'"

**Problem:**
```python
ModuleNotFoundError: No module named 'crewai'
```

**Cause:** Package not installed

**Solution:**
```bash
# Quick fix
pip3 install crewai --break-system-packages

# Better: Install all dependencies
pip3 install -r requirements.txt --break-system-packages

# Verify
pip3 list | grep crewai
```

---

### "ImportError: cannot import name 'X' from 'Y'"

**Problem:**
```python
ImportError: cannot import name 'AgentFeedbackLoop' from 'feedback_loop'
```

**Cause:** File doesn't have that class/function, or syntax error in file

**Solution:**
```bash
# Step 1: Check if file exists
ls agent_framework/feedback_loop.py

# Step 2: Check syntax
python3 -m py_compile agent_framework/feedback_loop.py

# Step 3: Check if class exists
grep -n "class AgentFeedbackLoop" agent_framework/feedback_loop.py

# Step 4: If missing, restore from backup or git
```

---

### "attempted relative import with no known parent package"

**Problem:**
```python
ImportError: attempted relative import with no known parent package
```

**Cause:** Trying to use relative import (`from .module`) when running file directly

**Solution - Already Fixed!**
This was fixed in your codebase. All files now have:
```python
try:
    from .module import Class  # Try relative
except ImportError:
    from module import Class   # Fallback to absolute
```

**If you still see it:**
```bash
# Run comprehensive audit (should be 0 issues)
python3 comprehensive_audit.py

# If issues found, restore from backup
```

---

### "No module named 'dotenv' / 'tenacity' / etc."

**Problem:**
```python
ModuleNotFoundError: No module named 'dotenv'
```

**Cause:** Specific dependency missing

**Solution:**
```bash
# Install missing package
pip3 install python-dotenv --break-system-packages
pip3 install tenacity --break-system-packages

# Or install everything
pip3 install -r requirements.txt --break-system-packages

# Verify
python3 -c "import dotenv; import tenacity; print('✅ Installed!')"
```

---

## 2️⃣ PERMISSION ERRORS

### "Permission denied" when running scripts

**Problem:**
```bash
bash: ./run_all_phases.sh: Permission denied
```

**Cause:** File not executable

**Solution:**
```bash
# Make executable
chmod +x run_all_phases.sh

# Or run with bash
bash run_all_phases.sh

# Or with python
python3 script.py
```

---

### "Permission denied" accessing files

**Problem:**
```bash
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**Cause:** Don't have write permission

**Solution:**
```bash
# Check current permissions
ls -l /path/to/file

# Fix permissions (make writable)
chmod u+w /path/to/file

# For directory
chmod u+w /path/to/directory
```

---

### "Cannot access WSL files from Windows"

**Problem:**
```
Access denied when opening \\wsl$\Ubuntu\...
```

**Cause:** WSL/Windows permission mismatch

**Solution A - Copy to Windows:**
```bash
# In WSL
cp -r /home/user01/claude-test/SwarmCare/SwarmCare_Production /mnt/c/Users/YourName/Documents/SwarmCare
```

**Solution B - Fix WSL permissions:**
```bash
# In WSL
sudo chmod -R 755 /home/user01/claude-test/SwarmCare
```

---

## 3️⃣ PYTHON ERRORS

### "SyntaxError: invalid syntax"

**Problem:**
```python
  File "implementation.py", line 42
    def execute(self, task)
                           ^
SyntaxError: invalid syntax
```

**Cause:** Missing colon, parenthesis, or other syntax issue

**Solution:**
```bash
# Check line 42 - it's missing a colon
# Should be: def execute(self, task):

# Validate syntax before running
python3 -m py_compile implementation.py

# Auto-fix with black (if installed)
pip3 install black --break-system-packages
black implementation.py
```

---

### "IndentationError: unexpected indent"

**Problem:**
```python
IndentationError: unexpected indent
```

**Cause:** Mixed tabs and spaces, or wrong indentation

**Solution:**
```bash
# Check indentation
cat -A implementation.py | head -50
# Look for ^I (tabs) vs spaces

# Fix with autopep8
pip3 install autopep8 --break-system-packages
autopep8 --in-place --aggressive implementation.py

# Or manually fix in editor
```

---

### "NameError: name 'X' is not defined"

**Problem:**
```python
NameError: name 'FRAMEWORK_AVAILABLE' is not defined
```

**Cause:** Variable used before defined, or scope issue

**Solution - Already Fixed!**
This was the scope bug we fixed. Should not occur.

**If you see it:**
```bash
# Re-run the fix script
python3 fix_all_phases_scope_bug.py

# Or restore from backup
```

---

### "AttributeError: 'NoneType' object has no attribute 'X'"

**Problem:**
```python
AttributeError: 'NoneType' object has no attribute 'execute'
```

**Cause:** Variable is None (function returned None or initialization failed)

**Solution:**
```python
# Add None checks
if obj is not None:
    obj.execute()

# Or check initialization
print(f"Object type: {type(obj)}")  # Should not be <class 'NoneType'>
```

**Debug:**
```bash
# Run with debug logging
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from implementation import Phase00Implementation
# ... rest of code
"
```

---

## 4️⃣ VALIDATION FAILURES

### "Validation tests failing"

**Problem:**
```
❌ FAIL: 2 import errors
```

**Solution:**
```bash
# Step 1: Read error details
python3 comprehensive_validation_tests.py 2>&1 | tee validation_error.log

# Step 2: Check specific errors
cat validation_error.log | grep "FAIL" -A 5

# Step 3: Fix based on error type
# - Import errors: Install missing packages
# - Syntax errors: Fix Python syntax
# - File errors: Restore missing files
```

---

### "Story points don't match (not 1,362)"

**Problem:**
```
Total Story Points: 1139  # Wrong!
Expected: 1362
```

**Solution:**
```bash
# This was already fixed!
# Run verification
python3 verify_story_points.py

# Should show: Total Story Points: 1362

# If not, restore from backup
```

---

### "100/120 Python files have valid syntax"

**Problem:**
```
✅ PASS: 100/120 Python files have valid syntax  # 20 files broken!
```

**Cause:** 20 files have syntax errors

**Solution:**
```bash
# Find broken files
for file in $(find . -name "*.py"); do
    python3 -m py_compile "$file" 2>&1 | grep -q "SyntaxError" && echo "❌ $file"
done

# Fix each file or restore from backup
```

---

## 5️⃣ PHASE EXECUTION ERRORS

### "Phase fails immediately"

**Problem:**
```bash
$ python3 implementation.py
Traceback (most recent call last):
  File "implementation.py", line 1, in <module>
    ...error...
```

**Debug steps:**
```bash
# 1. Check Python version (need 3.8+)
python3 --version

# 2. Check dependencies
pip3 install -r ../../../requirements.txt

# 3. Check path
pwd  # Should be in phases/phaseXX/code

# 4. Run with verbose errors
python3 -u implementation.py 2>&1 | tee error.log

# 5. Check error.log for details
```

---

### "Phase runs but fails with error"

**Problem:**
```
RESULT: FAILED
Error: [some error]
```

**Solution:**
```bash
# Check logs
tail -50 logs/execution.log

# Run with debug
cd phases/phase00/code
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from implementation import Phase00Implementation

impl = Phase00Implementation()
task = {'goal': 'test', 'verbose': True}
result = impl.execute(task)
print(f'Error: {result.error if hasattr(result, \"error\") else \"Unknown\"}')
"
```

---

### "Phase hangs/never completes"

**Problem:**
Phase starts but never finishes

**Cause:** Infinite loop, waiting for input, or deadlock

**Solution:**
```bash
# 1. Stop it
Ctrl+C

# 2. Check what it's doing
# Add timeout
timeout 60 python3 implementation.py

# If hangs again, check code for:
# - input() calls (shouldn't exist)
# - while True without break
# - waiting for network response
```

---

### "Cannot access local variable 'FRAMEWORK_AVAILABLE'"

**Problem:**
```python
UnboundLocalError: cannot access local variable 'FRAMEWORK_AVAILABLE' where it is not associated with a value
```

**Solution - Already Fixed!**
```bash
# This was the scope bug we fixed
# Should not occur after running:
python3 fix_all_phases_scope_bug.py

# If still happening, restore from backup
```

---

## 6️⃣ AGENT FRAMEWORK ISSUES

### "Agent framework not loading"

**Problem:**
```
⚠️  Agent framework import warning: ...
```

**Cause:** Import error in agent framework files

**Solution:**
```bash
# Test imports
python3 -c "
import sys
sys.path.insert(0, 'agent_framework')
from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager
print('✅ Agent framework works!')
"

# If fails, check specific error and fix
```

---

### "Feedback loop iterations exceed limit"

**Problem:**
```
WARNING: Exceeded maximum iterations (10)
```

**Cause:** Task not completing, feedback loop retrying

**Solution:**
```python
# Increase iteration limit
feedback_loop = AdaptiveFeedbackLoop(
    max_iterations=20,  # Increase from default 10
    adaptive_limits=True
)
```

**Or check why task is failing:**
```bash
# Enable detailed logging
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# ... rest of execution
"
```

---

### "Context manager overflow"

**Problem:**
```
WARNING: Context approaching token limit
```

**Cause:** Too much context accumulated

**Solution:**
```python
# Automatic compaction should handle this
# If not, reduce context manually:
context_manager = ContextManager(
    max_tokens=50000,  # Reduce from 100000
    compact_threshold=0.70  # Compact earlier
)
```

---

## 7️⃣ GUARDRAIL PROBLEMS

### "Guardrails blocking valid content"

**Problem:**
```
BLOCKED: Content flagged by medical guardrails
```

**Cause:** False positive from guardrail system

**Solution:**
```bash
# Check what was flagged
tail -50 logs/guardrails.log

# Adjust sensitivity (if needed)
guardrails = MultiLayerGuardrailSystem(
    phi_sensitivity=0.8,  # Default 0.9 (lower = less strict)
    medical_fact_check=False  # Disable specific check
)
```

---

### "Guardrails not initializing"

**Problem:**
```
WARNING: MultiLayerGuardrailSystem not available
```

**Cause:** Missing dependencies or configuration

**Solution:**
```bash
# Install guardrail dependencies
pip3 install python-dotenv --break-system-packages
pip3 install tenacity --break-system-packages

# Check environment variables
cat .env  # Should have Azure keys

# Test directly
python3 -c "
import sys
sys.path.insert(0, 'guardrails')
from multi_layer_system import MultiLayerGuardrailSystem
print('✅ Guardrails work!')
"
```

---

## 8️⃣ FILE SYSTEM ISSUES

### "No space left on device"

**Problem:**
```
OSError: [Errno 28] No space left on device
```

**Cause:** Disk full

**Solution:**
```bash
# Check disk space
df -h

# Find large files
du -sh * | sort -h | tail -10

# Clean up
rm -rf logs/*.log.old  # Old logs
find . -name "*.pyc" -delete  # Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +

# Check again
df -h
```

---

### "File not found"

**Problem:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config.json'
```

**Cause:** File doesn't exist or wrong path

**Solution:**
```bash
# Check if file exists
ls -la config.json

# Check current directory
pwd

# If in wrong directory, navigate to correct one
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# If file missing, restore from backup or create it
```

---

### "Too many open files"

**Problem:**
```
OSError: [Errno 24] Too many open files
```

**Cause:** Process opened too many files without closing

**Solution:**
```bash
# Quick fix: Increase limit
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
echo "* soft nofile 4096" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 8192" | sudo tee -a /etc/security/limits.conf

# Or fix code to close files properly
# Use context managers:
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed
```

---

## 9️⃣ PERFORMANCE PROBLEMS

### "Phase running very slow"

**Problem:**
Phase takes forever to complete

**Diagnostic:**
```bash
# Check CPU usage
top  # Look for Python processes using 100% CPU

# Check memory
free -h  # Look for swap usage (bad sign)

# Check disk I/O
iostat 1 10  # If available

# Check network (if phase uses API)
netstat -an | grep ESTABLISHED
```

**Solutions:**
```bash
# 1. Reduce parallel operations
orchestrator = SubagentOrchestrator(max_parallel=2)  # Reduce from 5

# 2. Reduce context size
context = ContextManager(max_tokens=50000)  # Reduce from 100000

# 3. Add progress logging
print(f"Progress: {completed}/{total}")
```

---

### "System running out of memory"

**Problem:**
```
MemoryError
# Or system becomes unresponsive
```

**Solution:**
```bash
# Check memory usage
free -h

# Kill memory-heavy processes
top  # Press 'M' to sort by memory
# Find process using lots of RAM, note PID
kill -9 PID

# Restart with memory limits
python3 -c "
import resource
resource.setrlimit(resource.RLIMIT_AS, (4*1024*1024*1024, 4*1024*1024*1024))  # 4GB limit
# ... rest of code
"
```

---

### "Processes not cleaning up"

**Problem:**
```bash
$ ps aux | grep python
# Shows 50+ python processes still running
```

**Solution:**
```bash
# Kill all Python processes
pkill -9 python3

# Or specific pattern
pkill -9 -f "implementation.py"

# Verify
ps aux | grep python  # Should show minimal/no results
```

---

## 🔟 VS 2022 ISSUES

### "IntelliSense not working"

**Problem:**
No auto-complete, no parameter hints

**Solution:**
1. Wait 2-3 minutes (IntelliSense indexes files)
2. Reload project: Close VS, reopen
3. Clear IntelliSense cache:
   ```
   Tools → Options → Python → Advanced
   Click "Reset IntelliSense Database"
   ```
4. Check Python environment is activated

---

### "Can't debug - breakpoints not hit"

**Problem:**
Set breakpoints but execution doesn't stop

**Solution:**
1. Check you're running with debug (`F5` not `Ctrl+F5`)
2. Verify breakpoint is red (not hollow)
3. Check "Debug" configuration is set
4. Try rebuilding: `Build → Rebuild Solution`
5. Set breakpoint on simpler line (not import, not comment)

---

### "Python environment not found"

**Problem:**
```
Error: Python environment not configured
```

**Solution:**
```
1. View → Other Windows → Python Environments
2. Check if environment exists
3. If missing:
   - Click "+ Add Environment"
   - Select "Virtual Environment"
   - Choose Python 3.10+
   - Create
4. Activate environment (right-click → Activate)
```

---

## 1️⃣1️⃣ DOCKER/CONTAINER ISSUES

### "Docker build fails"

**Problem:**
```
ERROR: failed to solve: process "/bin/sh -c ..." did not complete successfully
```

**Solution:**
```bash
# Build with verbose output
docker build --progress=plain -t swarmcare .

# Check Dockerfile syntax
cat Dockerfile

# Build without cache (fresh start)
docker build --no-cache -t swarmcare .

# Check Docker daemon running
docker info
```

---

### "Container exits immediately"

**Problem:**
```bash
$ docker run swarmcare
# Container starts and stops immediately
```

**Solution:**
```bash
# Check logs
docker logs <container-id>

# Run interactively
docker run -it swarmcare /bin/bash

# Check what command is running
docker inspect swarmcare | grep Cmd

# Make sure CMD in Dockerfile is correct
```

---

## 1️⃣2️⃣ NETWORK/API ISSUES

### "Connection refused"

**Problem:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Cause:** Service not running or port blocked

**Solution:**
```bash
# Check if port is open
netstat -an | grep 8000

# Check if service is running
ps aux | grep service_name

# Start service
python3 service.py &

# Check firewall
sudo ufw status  # If using firewall
```

---

### "Timeout errors"

**Problem:**
```
requests.exceptions.Timeout: ...
```

**Solution:**
```python
# Increase timeout
import requests
response = requests.get(url, timeout=60)  # Increase from default 30

# Or retry with tenacity
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def call_api():
    return requests.get(url)
```

---

## 🔍 DIAGNOSTIC COMMANDS

### Quick Health Check

```bash
# Run all these, should all pass
python3 --version  # 3.8+
pip3 list | grep crewai  # Should show version
python3 comprehensive_validation_tests.py  # 100% pass
python3 verify_story_points.py  # 1362
df -h  # Check disk space
free -h  # Check memory
```

### Full System Diagnostic

```bash
cat > diagnostic.sh << 'EOF'
#!/bin/bash
echo "=== SYSTEM DIAGNOSTIC ==="
echo "1. Python version:"
python3 --version

echo -e "\n2. Disk space:"
df -h | head -5

echo -e "\n3. Memory:"
free -h

echo -e "\n4. Running Python processes:"
ps aux | grep python | wc -l

echo -e "\n5. Package check:"
pip3 list | grep -E "(crewai|tenacity|dotenv)" || echo "Missing packages!"

echo -e "\n6. File structure:"
ls -la | head -15

echo -e "\n7. Validation status:"
python3 comprehensive_validation_tests.py 2>&1 | tail -5

echo -e "\n=== DIAGNOSTIC COMPLETE ==="
EOF

chmod +x diagnostic.sh
./diagnostic.sh
```

---

## 🆘 STILL STUCK?

If after trying all solutions above, you're still stuck:

1. **Create diagnostic report:**
   ```bash
   ./diagnostic.sh > diagnostic_report.txt
   tail -100 logs/execution.log >> diagnostic_report.txt
   ```

2. **Document your issue:**
   - What were you trying to do?
   - What command did you run?
   - What error did you get?
   - What have you tried?

3. **Restore from backup:**
   ```bash
   # Sometimes starting fresh is fastest solution
   tar -xzf backup_TIMESTAMP.tar.gz
   ```

4. **Check documentation:**
   - `COMPLETE_COMMAND_CHEATSHEET.md`
   - `PROJECT_SUCCESS_GUIDE.md`
   - Phase-specific READMEs

---

## 📝 ERROR LOG TEMPLATE

When asking for help, provide this:

```
**What I was trying to do:**
[e.g., Run Phase 00]

**What I ran:**
```bash
cd phases/phase00/code
python3 implementation.py
```

**What happened:**
[paste error message]

**What I tried:**
1. Checked logs: [what you found]
2. Ran validation: [result]
3. Restored backup: [result]

**System info:**
- Python version: [python3 --version]
- OS: [uname -a]
- Disk space: [df -h]

**Diagnostic report:**
[paste diagnostic.sh output]
```

---

**Remember:** 95% of issues are:
1. Missing package (install it)
2. Wrong directory (navigate to correct one)
3. Syntax error (check the line number)
4. File doesn't exist (restore from backup)
5. No permissions (chmod +x)

**Always try the simple solutions first!**
