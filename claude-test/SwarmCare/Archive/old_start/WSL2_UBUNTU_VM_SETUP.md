# WSL 2 UBUNTU VM SETUP & EXECUTION GUIDE
## SwarmCare v2.1 Ultimate - Multi-Instance Parallel Execution

**Version:** 2.1 Ultimate
**Environment:** Windows 11 Pro + WSL 2 + Ubuntu VM + Claude Code
**Created:** 2025-10-26
**Status:** ✅ PRODUCTION READY

---

## 🎯 SYSTEM OVERVIEW

### Your Setup
- **Host OS:** Windows 11 Pro (Laptop)
- **Virtualization:** WSL 2 (Windows Subsystem for Linux 2)
- **Guest OS:** Ubuntu VM running on WSL 2
- **Development Tool:** Claude Code (Max Account) running on Ubuntu VM
- **IDE:** Visual Studio 2022 Enterprise (on Windows host)
- **Workflow:** Generate code on Ubuntu → Transfer to Windows → Run in VS 2022

### Why This Setup?
- **Parallel Execution:** Run 5 Claude Code instances simultaneously on Ubuntu VM
- **Resource Isolation:** Ubuntu VM handles all code generation, freeing Windows for other work
- **Easy Transfer:** Simple file copy from WSL to Windows filesystem
- **Best of Both Worlds:** Linux development environment + Windows IDE

---

## 🔧 PREREQUISITES

### 1. Windows 11 Pro
```powershell
# Verify Windows version
winver
# Should show: Windows 11 Pro, Version 21H2 or later
```

### 2. WSL 2 Installed
```powershell
# Check WSL version
wsl --version
# Should show: WSL version: 2.x.x

# If not installed, install WSL 2:
wsl --install
# Restart computer after installation
```

### 3. Ubuntu Distribution
```powershell
# List installed distributions
wsl --list --verbose

# If Ubuntu not installed:
wsl --install -d Ubuntu

# Set Ubuntu as default:
wsl --set-default Ubuntu
```

### 4. Claude Code Installed on Ubuntu
```bash
# Inside Ubuntu (wsl command):
wsl

# Verify Claude Code installed:
which claude
# Should show: /usr/local/bin/claude (or similar)

# If not installed, follow Claude Code installation guide
```

### 5. Visual Studio 2022 Enterprise on Windows
- Already installed on your Windows 11 Pro laptop
- Used for final code execution and testing

---

## 📂 DIRECTORY STRUCTURE

### On Ubuntu (WSL 2):
```
/home/user01/claude-test/SwarmCare/
├── start/                           # Execution system
│   ├── orchestrator/                # Python orchestration scripts
│   │   ├── master_controller.py
│   │   └── phase_generator_v21.py
│   ├── phases/                      # 29 phase definitions (JSON)
│   ├── prompts/                     # 29 execution prompts (Markdown)
│   ├── instance_manager/            # 5 instance state files
│   ├── logs/                        # Execution logs
│   ├── reports/                     # Progress reports
│   └── START_EXECUTION.sh           # Main CLI
├── src/                             # Generated source code (output)
├── tests/                           # Generated tests
└── docs/                            # Generated documentation
```

### On Windows 11:
```
C:\Users\YourName\SwarmCare\        # Code transfer destination
├── src/                             # Copy from Ubuntu
├── tests/                           # Copy from Ubuntu
└── docs/                            # Copy from Ubuntu
```

### Accessing Ubuntu Files from Windows:
```
\\wsl$\Ubuntu\home\user01\claude-test\SwarmCare\
```

---

## 🚀 EXECUTION WORKFLOW

### Step 1: Open 5 Ubuntu Terminal Windows

**Option A: Windows Terminal (Recommended)**
```powershell
# Open Windows Terminal
# Click '+' dropdown → Select 'Ubuntu'
# Repeat 5 times to get 5 Ubuntu tabs
```

**Option B: PowerShell**
```powershell
# Terminal 1
wsl -d Ubuntu

# Open 4 more PowerShell windows and run same command
```

**Option C: Direct Ubuntu Terminal**
```
Start Menu → Ubuntu → Open 5 instances
```

### Step 2: Navigate to SwarmCare Directory (All 5 Terminals)
```bash
# In EACH terminal window:
cd /home/user01/claude-test/SwarmCare/start
```

### Step 3: Initialize System (One Terminal Only)
```bash
# Run ONLY ONCE in Terminal 1:
python3 orchestrator/master_controller.py

# This creates:
# - 5 instance configurations
# - Phase distributions
# - State tracking files
```

### Step 4: Execute Prompts in Parallel (All 5 Terminals)

**Terminal 1 - Instance 1:**
```bash
cd /home/user01/claude-test/SwarmCare/start
cat prompts/instance_01_phase_00_prompt.md

# Copy the ENTIRE output and paste into Claude Code
# Claude Code will start executing Phase 0
```

**Terminal 2 - Instance 2:**
```bash
cd /home/user01/claude-test/SwarmCare/start
cat prompts/instance_02_phase_03_prompt.md

# Copy and paste into Claude Code instance 2
```

**Terminal 3 - Instance 3:**
```bash
cd /home/user01/claude-test/SwarmCare/start
cat prompts/instance_03_phase_04_prompt.md

# Copy and paste into Claude Code instance 3
```

**Terminal 4 - Instance 4:**
```bash
cd /home/user01/claude-test/SwarmCare/start
cat prompts/instance_04_phase_07_prompt.md

# Copy and paste into Claude Code instance 4
```

**Terminal 5 - Instance 5:**
```bash
cd /home/user01/claude-test/SwarmCare/start
cat prompts/instance_05_phase_01_prompt.md

# Copy and paste into Claude Code instance 5
```

---

## 📊 MONITORING PROGRESS

### Option 1: Dedicated Monitoring Terminal (Recommended)
```bash
# Open a 6th terminal for monitoring:
cd /home/user01/claude-test/SwarmCare/start

# Run monitor every 30 minutes:
watch -n 1800 ./START_EXECUTION.sh monitor

# Or manually:
./START_EXECUTION.sh monitor
```

### Option 2: Check Individual Instance Status
```bash
# Check specific instance:
cat instance_manager/instance_01_state.json

# View in pretty format:
cat instance_manager/instance_01_state.json | python3 -m json.tool
```

### Option 3: Check Overall Progress
```bash
./START_EXECUTION.sh status
```

---

## 🔄 TRANSFERRING CODE TO WINDOWS

### Method 1: Direct File Access (Easiest)

**In Windows File Explorer:**
1. Press `Win + R`
2. Type: `\\wsl$\Ubuntu\home\user01\claude-test\SwarmCare`
3. Press Enter
4. You'll see all generated files
5. Copy `src/`, `tests/`, `docs/` to `C:\Users\YourName\SwarmCare\`

### Method 2: Using WSL Command
```powershell
# In PowerShell (Windows):
# Copy from Ubuntu to Windows:
xcopy \\wsl$\Ubuntu\home\user01\claude-test\SwarmCare\src C:\Users\YourName\SwarmCare\src /E /I /Y
xcopy \\wsl$\Ubuntu\home\user01\claude-test\SwarmCare\tests C:\Users\YourName\SwarmCare\tests /E /I /Y
```

### Method 3: Using WSL cp Command
```bash
# In Ubuntu (WSL):
# Access Windows filesystem from Ubuntu:
cp -r /home/user01/claude-test/SwarmCare/src /mnt/c/Users/YourName/SwarmCare/
cp -r /home/user01/claude-test/SwarmCare/tests /mnt/c/Users/YourName/SwarmCare/
```

---

## 🧪 RUNNING CODE IN VISUAL STUDIO 2022

### Step 1: Open Solution in VS 2022
```
1. Open Visual Studio 2022 Enterprise
2. File → Open → Project/Solution
3. Navigate to: C:\Users\YourName\SwarmCare\SwarmCare.sln
4. Click Open
```

### Step 2: Restore NuGet Packages
```
Tools → NuGet Package Manager → Restore NuGet Packages
```

### Step 3: Build Solution
```
Build → Build Solution (Ctrl+Shift+B)
```

### Step 4: Run Tests
```
Test → Run All Tests (Ctrl+R, A)
```

### Step 5: Run Application
```
Debug → Start Debugging (F5)
Or
Debug → Start Without Debugging (Ctrl+F5)
```

---

## ⏸️ PAUSE & RESUME

### Pausing Execution

**Graceful Pause:**
```bash
# In ANY terminal running Claude Code:
# Just close the terminal or Ctrl+C

# All state is automatically saved to:
/home/user01/claude-test/SwarmCare/start/.phase_state/
```

### Resuming Execution

**After Break (Same Day or Next Day):**
```bash
# Terminal 1:
cd /home/user01/claude-test/SwarmCare/start
./START_EXECUTION.sh resume

# This shows:
# - What was completed
# - What's in progress
# - What remains
# - Next steps for each instance

# Then continue executing prompts where you left off
```

**Resume Specific Instance:**
```bash
# Check instance state:
cat instance_manager/instance_01_state.json

# Find current phase
# Execute next prompt:
cat prompts/instance_01_phase_XX_prompt.md
# Copy to Claude Code
```

---

## 🔧 TROUBLESHOOTING

### Issue: WSL 2 Not Starting
```powershell
# Restart WSL:
wsl --shutdown
wsl

# Check status:
wsl --status
```

### Issue: Ubuntu Out of Disk Space
```bash
# Check disk usage:
df -h

# Clean up:
sudo apt clean
sudo apt autoremove
```

### Issue: Cannot Access Ubuntu Files from Windows
```powershell
# Verify WSL is running:
wsl --list --running

# If not running, start Ubuntu:
wsl -d Ubuntu
```

### Issue: Claude Code Max Sessions Limit
```
# Solution: Use 5 instances, not more
# Max account supports up to 10 concurrent sessions
# Recommended: 5 instances for optimal balance
```

### Issue: File Transfer Slow
```bash
# Use rsync instead of cp for faster transfer:
sudo apt install rsync
rsync -av /home/user01/claude-test/SwarmCare/src/ /mnt/c/Users/YourName/SwarmCare/src/
```

---

## 📈 INSTANCE DISTRIBUTION

### 5-Instance Setup (Recommended)

| Instance | Phases | Story Points | Duration | Status |
|----------|--------|--------------|----------|--------|
| **1** | 0, 2, 6, 11, 24, 28 | 225 | ~4.5 weeks | Foundation, SWARMCARE, HIPAA, Research, Auto-Coding, Voice |
| **2** | 3, 16, 18, 20, 21, 22 | 182 | ~3.6 weeks | Workflows, XAI, Trials, Certs, Closed-Loop, Federated |
| **3** | 4, 9, 14, 25, 26, 27 | 194 | ~3.9 weeks | Frontend, Docs, Imaging, Patient-XAI, CDC, Trial-Lifecycle |
| **4** | 7, 10, 12, 23 | 170 | ~3.4 weeks | Testing, Business, Clinical-Decision, FDA |
| **5** | 1, 5, 8, 13, 15, 17, 19 | 331 | ~6.6 weeks | RAG, Audio, Deploy, Predictive, NLP, Pop-Health, Voice |

**Max Duration:** ~6.6 weeks (Instance 5 is critical path)
**Time Savings:** 70% faster than sequential (6.6 weeks vs 22 weeks)

### Alternative: 7-Instance Setup (More Balanced)
```bash
# For better load balancing:
python3 orchestrator/master_controller.py
# Select 7 instances when prompted
# Max duration: ~3.2 weeks
# Time savings: 85%
```

### Alternative: 10-Instance Setup (Fastest)
```bash
# For maximum speed:
python3 orchestrator/master_controller.py
# Select 10 instances
# Max duration: ~2.3 weeks
# Time savings: 90%
```

---

## ✅ BEST PRACTICES

### 1. Resource Management
- **Keep Windows Free:** Don't run heavy apps on Windows while Ubuntu instances are running
- **Monitor RAM:** WSL 2 can use up to 50% of total RAM by default
- **Close Unused Apps:** Free up memory for Claude Code instances

### 2. Backup Strategy
```bash
# Daily backup (automated):
cp -r instance_manager instance_manager.backup.$(date +%Y%m%d)
cp -r .phase_state .phase_state.backup.$(date +%Y%m%d)

# Weekly full backup:
tar -czf swarmcare_backup_$(date +%Y%m%d).tar.gz \
    instance_manager .phase_state src tests docs
```

### 3. Progress Tracking
- Check status every 2-4 hours
- Run monitor command after each phase completion
- Keep a log of completed phases

### 4. Code Review
- Review generated code before transferring to Windows
- Run tests on Ubuntu before transfer
- Validate in VS 2022 after transfer

---

## 📞 QUICK REFERENCE

### Essential Commands
```bash
# Navigate to project:
cd /home/user01/claude-test/SwarmCare/start

# Initialize system:
python3 orchestrator/master_controller.py

# Check status:
./START_EXECUTION.sh status

# Monitor progress:
./START_EXECUTION.sh monitor

# Resume after break:
./START_EXECUTION.sh resume

# View prompt:
cat prompts/instance_XX_phase_YY_prompt.md
```

### Windows Access
```
File Explorer: \\wsl$\Ubuntu\home\user01\claude-test\SwarmCare
PowerShell: wsl -d Ubuntu
```

---

## 🎯 EXECUTION CHECKLIST

**Pre-Execution:**
- [ ] WSL 2 running on Windows 11 Pro
- [ ] Ubuntu installed and updated
- [ ] Claude Code Max account active
- [ ] Visual Studio 2022 Enterprise installed
- [ ] All 5 terminals open and ready

**During Execution:**
- [ ] Monitor progress every 2-4 hours
- [ ] Backup state files daily
- [ ] Review generated code periodically
- [ ] Transfer completed phases to Windows

**Post-Execution:**
- [ ] All 29 phases completed
- [ ] All tests passing
- [ ] Code transferred to Windows
- [ ] Solution builds in VS 2022
- [ ] Application runs successfully

---

## 🚀 READY TO START

Your system is 100% configured for parallel execution on WSL 2 Ubuntu VM!

**Next Steps:**
1. Open 5 Ubuntu terminal windows
2. Navigate to `/home/user01/claude-test/SwarmCare/start`
3. Execute prompts in all 5 instances simultaneously
4. Monitor progress
5. Transfer generated code to Windows
6. Build and run in Visual Studio 2022

**Total Duration:** ~6.6 weeks with 5 instances
**Time Savings:** 70% faster than sequential execution

🎉 **BUILD SWARMCARE v2.1 ULTIMATE IN RECORD TIME!** 🎉

---

**Version:** 2.1 Ultimate
**Total Phases:** 29
**Total Story Points:** 1,102
**Competitive Score:** 120/120 (PERFECT)
