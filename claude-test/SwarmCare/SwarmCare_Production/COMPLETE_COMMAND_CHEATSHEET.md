# 🚀 SWARMCARE COMPLETE COMMAND CHEATSHEET
## From Beginner to Expert - Your Survival Guide

**Version:** 1.0
**Last Updated:** October 27, 2025
**Purpose:** Complete reference for running, monitoring, and troubleshooting SwarmCare

---

## 📋 TABLE OF CONTENTS

0. [**⭐ TRACKER COMMANDS (MOST IMPORTANT!)**](#tracker-commands) ← **START HERE**
1. [Quick Start (I'm New!)](#quick-start)
2. [Basic Commands](#basic-commands)
3. [Running at Root Level](#root-level-execution)
4. [Running Individual Phases](#phase-level-execution)
5. [Multi-Instance (Same System)](#multi-instance-execution)
6. [Multi-System (Distributed)](#multi-system-execution)
7. [Checking Logs](#log-management)
8. [Verifying Code Generation](#code-verification)
9. [Monitoring Agent Framework](#agent-framework-monitoring)
10. [Checking Guardrails](#guardrails-monitoring)
11. [MCP Servers](#mcp-server-management)
12. [Running Tests](#test-execution)
13. [Troubleshooting](#troubleshooting)
14. [Integration Commands](#integration-commands)
15. [Emergency Commands](#emergency-commands)

---

## ⭐ 0. TRACKER COMMANDS (MOST IMPORTANT!)

### Why Use the Tracker?

**THE #1 RULE: Always use tracker commands to run phases!**

Benefits:
- ✅ Continue from where you left off (survives shutdowns)
- ✅ Track progress (1,362 story points)
- ✅ Never lose your place
- ✅ Real-time status and progress bars
- ✅ Auto-sync between root and phase levels

**Read this section FIRST before anything else!**

### Core Tracker Commands

```bash
# Check current status
./scripts/status.sh                    # Quick overview
./scripts/status.sh --detailed         # All 29 phases

# Start a phase (updates tracker)
./scripts/start_phase.sh <phase_id>    # Example: ./scripts/start_phase.sh 0

# Complete a phase (updates tracker + moves to next)
./scripts/complete_phase.sh <phase_id> # Example: ./scripts/complete_phase.sh 0

# Interactive menu
./continue                              # Shows status + menu options
```

### At Root Level

```bash
# Navigate to project root
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Check where you are
./scripts/status.sh

# Continue from current phase
CURRENT=$(python3 scripts/sync_tracker.py current)
./scripts/start_phase.sh $CURRENT

# Or just use the interactive menu
./continue
```

### At Phase Level

```bash
# Navigate to any phase
cd phases/phase05    # Example: Phase 5

# Run that phase (auto-detects phase number)
./continue

# Or explicit
../../scripts/run_from_phase.sh

# Go back and check status
cd ../../
./scripts/status.sh
```

### Complete Workflow Example

```bash
# Day 1: Run Phase 0-2
./scripts/status.sh                    # See current state
./scripts/start_phase.sh 0             # Start Phase 0
./scripts/complete_phase.sh 0          # Mark complete
./scripts/start_phase.sh 1             # Phase 1
./scripts/complete_phase.sh 1          # Complete
./scripts/start_phase.sh 2             # Phase 2
./scripts/complete_phase.sh 2          # Complete
./scripts/status.sh                    # Check progress

# Shutdown overnight...

# Day 2: Continue from where you left off
./scripts/status.sh                    # Shows Phase 3 next
./scripts/start_phase.sh 3             # Resume!
```

### Sync Commands (Advanced)

```bash
# Get current phase number
python3 scripts/sync_tracker.py current

# Sync specific phase to root
python3 scripts/sync_tracker.py sync <phase_id>

# Sync all phases
python3 scripts/sync_tracker.py sync-all

# Manually mark phase started
python3 scripts/sync_tracker.py start <phase_id>

# Manually mark phase completed
python3 scripts/sync_tracker.py complete <phase_id>
```

### Status Output Example

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

### Tracker Troubleshooting

```bash
# Tracker out of sync?
python3 scripts/sync_tracker.py sync-all

# Lost current phase?
python3 scripts/sync_tracker.py current

# Phase state missing?
# See TROUBLESHOOTING_GUIDE.md Section: "Phase State File Missing"

# Root tracker corrupted?
./continue    # Menu option 5: Reset progress (CAUTION!)
```

### Multi-Machine Tracker Sync

```bash
# Machine 1: After completing phases
git add .tracker phases/*/. state
git commit -m "Completed Phase 5"
git push

# Machine 2: Resume from different machine
git pull
./scripts/status.sh                    # See where Machine 1 left off
./scripts/start_phase.sh 6             # Continue!
```

### Key Points

**ALWAYS:**
- ✅ Use `./scripts/start_phase.sh <ID>` NOT `python3 implementation.py`
- ✅ Use `./scripts/complete_phase.sh <ID>` after phase success
- ✅ Check `./scripts/status.sh` frequently
- ✅ From phase dir, use `./continue`

**NEVER:**
- ❌ Run `python3 implementation.py` directly (bypasses tracker!)
- ❌ Manually edit `.tracker/state.json` (can corrupt!)
- ❌ Skip completing phases (loses progress!)

**For complete tracker documentation, see:** `TRACKER_USAGE_GUIDE.md`

---

## 🎯 QUICK START (I'm New!)

### First Time Setup (Run Once)

```bash
# 1. Navigate to project
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# 2. Install ALL dependencies
pip3 install -r requirements.txt --break-system-packages

# 3. Verify installation
python3 comprehensive_validation_tests.py

# 4. Check tracker status
./scripts/status.sh

# 5. Run your first phase THROUGH TRACKER
./scripts/start_phase.sh 0

# 6. Mark it complete
./scripts/complete_phase.sh 0

# 7. Check updated progress
./scripts/status.sh
```

**Expected Output:**
```
✅ Phase 00: Foundation & Infrastructure
✅ Story Points: 37
RESULT: SUCCESS
```

---

## 📚 BASIC COMMANDS

### Navigation

```bash
# Go to project root
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Go to specific phase
cd phases/phase00      # Phase 0
cd phases/phase15      # Phase 15
cd phases/phase28      # Phase 28

# Go back to root from anywhere
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production
```

### Check What's Installed

```bash
# Python version (should be 3.8+)
python3 --version

# Check all installed packages
pip3 list

# Check specific package
pip3 show crewai
pip3 show tenacity
pip3 show python-dotenv
```

### File Structure Overview

```bash
# See all files
ls -la

# See only directories
ls -d */

# See all phases
ls phases/

# Count total Python files
find . -name "*.py" | wc -l

# See file sizes
du -sh *
```

---

## 🏢 ROOT LEVEL EXECUTION

### Run System-Wide Validation

```bash
# From project root
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Full system validation
python3 comprehensive_validation_tests.py

# Full system audit
python3 comprehensive_audit.py

# Verify story points
python3 verify_story_points.py
```

### Run All Phases Sequentially

```bash
# Create master execution script
cat > run_all_phases.sh << 'EOF'
#!/bin/bash
for i in {00..28}; do
    echo "Running Phase $i..."
    cd phases/phase$i/code
    python3 implementation.py > ../../../logs/phase${i}.log 2>&1
    cd ../../..
    echo "Phase $i complete"
done
EOF

chmod +x run_all_phases.sh
./run_all_phases.sh
```

### Monitor System Health

```bash
# Check CPU and memory
top

# Check disk space
df -h

# Check running Python processes
ps aux | grep python
```

---

## 🎯 PHASE LEVEL EXECUTION

### Run Single Phase

```bash
# Basic execution
cd phases/phase00/code
python3 implementation.py

# With output logging
cd phases/phase00/code
python3 implementation.py 2>&1 | tee ../logs/execution.log

# With specific task
cd phases/phase00/code
python3 implementation.py --task "setup_infrastructure"
```

### Run Multiple Phases

```bash
# Phases 0-5
for i in {00..05}; do
    cd phases/phase$i/code
    python3 implementation.py
    cd ../../..
done

# Specific phases (0, 5, 10, 15)
for i in 00 05 10 15; do
    cd phases/phase$i/code
    python3 implementation.py
    cd ../../..
done
```

### Run Phase with Custom Parameters

```bash
# Example: Phase 00 with verbose output
cd phases/phase00/code
python3 -c "
from implementation import Phase00Implementation
impl = Phase00Implementation()
task = {'goal': 'Setup cloud infrastructure', 'verbose': True}
result = impl.execute(task)
print(f'Success: {result.success}')
"
```

---

## 🔄 MULTI-INSTANCE EXECUTION (Same System)

### Run 3 Phases in Parallel

```bash
# Terminal 1
cd phases/phase00/code && python3 implementation.py &

# Terminal 2
cd phases/phase01/code && python3 implementation.py &

# Terminal 3
cd phases/phase02/code && python3 implementation.py &

# Wait for all to complete
wait
```

### Using Background Jobs

```bash
# Start 5 phases in background
for i in {00..04}; do
    (cd phases/phase$i/code && python3 implementation.py > ../logs/run.log 2>&1) &
done

# Check running jobs
jobs -l

# Monitor all background processes
ps aux | grep "implementation.py"

# Wait for all to finish
wait
```

### Using GNU Parallel (Advanced)

```bash
# Install parallel if not present
sudo apt-get install parallel

# Run 4 phases in parallel
parallel -j 4 'cd phases/phase{}/code && python3 implementation.py > ../logs/run.log 2>&1' ::: {00..28}

# Run with progress bar
parallel --progress -j 4 'cd phases/phase{}/code && python3 implementation.py' ::: {00..28}
```

---

## 🌐 MULTI-SYSTEM EXECUTION (Distributed)

### Setup SSH Keys (One Time)

```bash
# On main system, generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/swarmcare_key

# Copy to remote systems
ssh-copy-id -i ~/.ssh/swarmcare_key.pub user@server1
ssh-copy-id -i ~/.ssh/swarmcare_key.pub user@server2
```

### Distribute Code to Remote Systems

```bash
# Copy entire project to remote servers
rsync -avz --progress /home/user01/claude-test/SwarmCare/SwarmCare_Production/ \
    user@server1:/home/user/SwarmCare_Production/

rsync -avz --progress /home/user01/claude-test/SwarmCare/SwarmCare_Production/ \
    user@server2:/home/user/SwarmCare_Production/
```

### Run Phases on Different Systems

```bash
# Create distributed execution script
cat > run_distributed.sh << 'EOF'
#!/bin/bash

# Server 1: Phases 0-9
ssh user@server1 'cd /home/user/SwarmCare_Production && for i in {00..09}; do cd phases/phase$i/code && python3 implementation.py; cd ../../..; done' &

# Server 2: Phases 10-19
ssh user@server2 'cd /home/user/SwarmCare_Production && for i in {10..19}; do cd phases/phase$i/code && python3 implementation.py; cd ../../..; done' &

# Local: Phases 20-28
for i in {20..28}; do
    cd phases/phase$i/code
    python3 implementation.py
    cd ../../..
done

wait
echo "All distributed phases complete!"
EOF

chmod +x run_distributed.sh
./run_distributed.sh
```

### Monitor Remote Execution

```bash
# Check running processes on remote
ssh user@server1 'ps aux | grep python'

# Check logs on remote
ssh user@server1 'tail -f /home/user/SwarmCare_Production/logs/phase00.log'

# Check system resources on remote
ssh user@server1 'top -b -n 1 | head -20'
```

---

## 📊 LOG MANAGEMENT

### Where Are Logs?

```bash
# Create logs directory if needed
mkdir -p logs

# Phase-specific logs (create in each phase)
mkdir -p phases/phase00/logs
mkdir -p phases/phase01/logs
# ... etc
```

### View Logs in Real-Time

```bash
# Watch main execution log
tail -f logs/execution.log

# Watch specific phase
tail -f phases/phase00/logs/execution.log

# Watch last 50 lines
tail -50 logs/execution.log

# Watch and search for errors
tail -f logs/execution.log | grep -i error
```

### Search Logs

```bash
# Find all errors
grep -r "ERROR" logs/

# Find all warnings
grep -r "WARNING" logs/

# Find specific phase errors
grep -r "Phase 00" logs/ | grep ERROR

# Count errors per phase
for i in {00..28}; do
    echo "Phase $i errors: $(grep -c ERROR logs/phase${i}.log 2>/dev/null || echo 0)"
done
```

### Log Analysis

```bash
# Get execution summary
cat > analyze_logs.sh << 'EOF'
#!/bin/bash
echo "=== LOG ANALYSIS ==="
echo "Total Errors: $(grep -r "ERROR" logs/ | wc -l)"
echo "Total Warnings: $(grep -r "WARNING" logs/ | wc -l)"
echo "Successful Phases: $(grep -r "SUCCESS" logs/ | wc -l)"
echo "Failed Phases: $(grep -r "FAILED" logs/ | wc -l)"
EOF

chmod +x analyze_logs.sh
./analyze_logs.sh
```

---

## ✅ CODE VERIFICATION

### Verify All Python Files

```bash
# Check syntax of all Python files
python3 comprehensive_validation_tests.py

# Manual syntax check for specific file
python3 -m py_compile phases/phase00/code/implementation.py

# Check all files in a phase
for file in phases/phase00/code/*.py; do
    python3 -m py_compile "$file" && echo "✅ $file" || echo "❌ $file"
done
```

### Verify Imports Work

```bash
# Test agent framework imports
python3 -c "
import sys
sys.path.insert(0, 'agent_framework')
from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager
from subagent_orchestrator import SubagentOrchestrator
print('✅ Agent framework imports work!')
"

# Test guardrails imports
python3 -c "
import sys
sys.path.insert(0, 'guardrails')
from multi_layer_system import MultiLayerGuardrailSystem
from medical_guardrails import MedicalGuardrails
print('✅ Guardrail imports work!')
"
```

### Verify Story Points

```bash
# Run verification script
python3 verify_story_points.py

# Expected output: Total Story Points: 1362
```

### Check Code Quality

```bash
# Count lines of code
find . -name "*.py" -exec wc -l {} + | tail -1

# Find large files (>500 lines)
find . -name "*.py" -exec wc -l {} + | awk '$1 > 500'

# Check for TODO comments
grep -r "TODO" --include="*.py"

# Check for FIXME comments
grep -r "FIXME" --include="*.py"
```

---

## 🤖 AGENT FRAMEWORK MONITORING

### Check Framework Status

```bash
# Verify all components exist
python3 -c "
from pathlib import Path
components = [
    'feedback_loop.py', 'feedback_loop_enhanced.py',
    'context_manager.py', 'subagent_orchestrator.py',
    'agentic_search.py', 'code_generator.py',
    'verification_system.py', 'mcp_integration.py'
]
for comp in components:
    exists = (Path('agent_framework') / comp).exists()
    print(f'{"✅" if exists else "❌"} {comp}')
"
```

### Monitor Feedback Loop

```bash
# Run phase with feedback loop monitoring
cd phases/phase00/code
python3 -c "
from implementation import Phase00Implementation
import logging
logging.basicConfig(level=logging.DEBUG)

impl = Phase00Implementation()
task = {'goal': 'Test feedback loop', 'monitor': True}
result = impl.execute(task)

print(f'Iterations: {result.iterations}')
print(f'Duration: {result.total_duration_seconds}s')
print(f'Success: {result.success}')
"
```

### Check Context Management

```bash
# Monitor context usage
python3 -c "
from agent_framework.context_manager import ContextManager

context = ContextManager(max_tokens=100000)
context.add_context('test', 'This is test context' * 1000)
print(f'Current tokens: {context.estimate_tokens()}')
print(f'At capacity: {context.estimate_tokens() / context.max_tokens * 100:.1f}%')
"
```

### Monitor Subagent Execution

```bash
# Check subagent orchestrator
python3 -c "
from agent_framework.subagent_orchestrator import SubagentOrchestrator

orchestrator = SubagentOrchestrator(max_parallel=5)
stats = orchestrator.get_statistics()
print(f'Max parallel: {stats[\"max_parallel\"]}')
print(f'Tasks executed: {stats[\"total_tasks_executed\"]}')
"
```

---

## 🛡️ GUARDRAILS MONITORING

### Check Guardrail Status

```bash
# Verify guardrails are active
python3 -c "
import sys
sys.path.insert(0, 'guardrails')
from multi_layer_system import MultiLayerGuardrailSystem

guardrails = MultiLayerGuardrailSystem()
print('✅ Guardrail system initialized')
print(f'Layers: {len(guardrails.validators) if hasattr(guardrails, \"validators\") else \"Unknown\"}')
"
```

### Test Medical Guardrails

```bash
# Test PHI detection
python3 -c "
import sys
sys.path.insert(0, 'guardrails')
from medical_guardrails import PHIDetector

detector = PHIDetector()
test_text = 'Patient John Doe, SSN 123-45-6789'
result = detector.detect(test_text)
print(f'PHI Detected: {result.detected}')
print(f'Confidence: {result.confidence}')
"
```

### Monitor Guardrail Logs

```bash
# Watch guardrail events
tail -f logs/guardrails.log | grep -E "(BLOCKED|WARNING|PHI_DETECTED)"

# Count guardrail interventions
grep -c "BLOCKED" logs/guardrails.log
```

---

## 🔌 MCP SERVER MANAGEMENT

### Start MCP Servers

```bash
# Start all MCP servers
cd mcp_servers

# Start individual server
python3 server_name.py &

# Check running servers
ps aux | grep "mcp_servers"
```

### Check MCP Server Health

```bash
# Test MCP connection
python3 -c "
from agent_framework.mcp_integration import MCPIntegration

mcp = MCPIntegration()
status = mcp.check_connection()
print(f'MCP Status: {status}')
"
```

### Stop MCP Servers

```bash
# Kill all MCP servers
pkill -f "mcp_servers"

# Kill specific server
pkill -f "server_name.py"
```

---

## 🧪 TEST EXECUTION

### Run All Tests

```bash
# Run comprehensive test suite
python3 comprehensive_validation_tests.py

# Run with pytest (if available)
pytest tests/ -v

# Run specific test file
pytest tests/test_agent_framework.py -v
```

### Run Phase-Specific Tests

```bash
# Test phase 00
cd phases/phase00/tests
python3 test_phase00.py

# Test all phases
for i in {00..28}; do
    echo "Testing Phase $i..."
    cd phases/phase$i/tests
    python3 test_phase${i}.py
    cd ../../..
done
```

### Test Coverage

```bash
# Install coverage tool
pip3 install coverage --break-system-packages

# Run with coverage
coverage run comprehensive_validation_tests.py
coverage report
coverage html

# Open HTML report
firefox htmlcov/index.html
```

---

## 🔧 TROUBLESHOOTING

### "Import Error" - Module Not Found

```bash
# Problem: from X import Y fails
# Solution 1: Check if file exists
ls agent_framework/X.py

# Solution 2: Add to Python path
export PYTHONPATH=/home/user01/claude-test/SwarmCare/SwarmCare_Production:$PYTHONPATH

# Solution 3: Install missing dependency
pip3 install <package-name> --break-system-packages
```

### "Permission Denied"

```bash
# Problem: Can't execute script
# Solution: Add execute permission
chmod +x script_name.sh
chmod +x script_name.py
```

### "Module has no attribute"

```bash
# Problem: AttributeError: module 'X' has no attribute 'Y'
# Solution 1: Check Python file syntax
python3 -m py_compile agent_framework/X.py

# Solution 2: Restart Python (clear cache)
python3 -c "import sys; sys.exit(0)"

# Solution 3: Remove .pyc files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### "Port Already in Use"

```bash
# Problem: Address already in use
# Solution: Find and kill process
lsof -i :PORT_NUMBER
kill -9 PID

# Example: Port 8000
lsof -i :8000
kill -9 <PID>
```

### Phase Execution Fails

```bash
# 1. Check logs
tail -50 phases/phase00/logs/execution.log

# 2. Run with debug
cd phases/phase00/code
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from implementation import Phase00Implementation
impl = Phase00Implementation()
# ... rest of execution
"

# 3. Verify dependencies
pip3 install -r ../../../requirements.txt
```

---

## 🔗 INTEGRATION COMMANDS

### Integrate with External System

```bash
# Step 1: Check integration directory
ls integration/

# Step 2: Configure integration
cd integration
cp config.example.json config.json
nano config.json  # Edit with your settings

# Step 3: Test integration
python3 test_integration.py

# Step 4: Run integration
python3 run_integration.py
```

### API Integration

```bash
# Test API endpoint
curl -X POST http://localhost:8000/api/phase/00/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "setup_infrastructure"}'

# Check API health
curl http://localhost:8000/health
```

---

## 🚨 EMERGENCY COMMANDS

### Kill All Python Processes

```bash
# WARNING: Kills ALL Python processes
pkill -9 python3

# Kill only SwarmCare processes
pkill -9 -f "SwarmCare"
```

### Reset Everything

```bash
# Stop all processes
pkill -f "implementation.py"

# Remove all logs
rm -rf logs/*
rm -rf phases/*/logs/*

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Reinstall dependencies
pip3 install -r requirements.txt --break-system-packages --force-reinstall
```

### Backup Before Changes

```bash
# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf ../SwarmCare_backup_$TIMESTAMP.tar.gz .
echo "Backup created: SwarmCare_backup_$TIMESTAMP.tar.gz"
```

### Restore from Backup

```bash
# List backups
ls -lh ../SwarmCare_backup_*.tar.gz

# Restore specific backup
cd ..
tar -xzf SwarmCare_backup_TIMESTAMP.tar.gz -C SwarmCare_Production_restored
```

---

## 📖 QUICK REFERENCE

### Daily Commands

```bash
# Morning checklist
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production
git pull  # If using git
python3 comprehensive_validation_tests.py
python3 verify_story_points.py

# Run your work
cd phases/phaseXX/code
python3 implementation.py

# Evening checklist
./analyze_logs.sh
tar -czf ../backup_$(date +%Y%m%d).tar.gz .
```

### Most Common Commands

```bash
# Navigate
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production

# Validate
python3 comprehensive_validation_tests.py

# Run phase
cd phases/phase00/code && python3 implementation.py

# Check logs
tail -f logs/execution.log

# Check processes
ps aux | grep python
```

---

## 💡 PRO TIPS

1. **Always validate before running**: `python3 comprehensive_validation_tests.py`
2. **Always log output**: `2>&1 | tee logs/run.log`
3. **Always backup before changes**: `tar -czf backup.tar.gz .`
4. **Always check logs after execution**: `tail -50 logs/execution.log`
5. **Always verify story points**: `python3 verify_story_points.py`

---

**Questions? Issues? Check:**
- `FINAL_100_PERCENT_COMPLETE_REPORT.md` - Complete system status
- `TROUBLESHOOTING_GUIDE.md` - Detailed troubleshooting
- `logs/` - Execution logs

**Emergency Contact:** Check documentation in `docs/`
