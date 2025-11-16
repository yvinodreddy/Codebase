# SWARMCARE DISTRIBUTED DEVELOPMENT - COMPLETE SETUP GUIDE

**Version:** 1.0
**Date:** 2025-10-26
**Mode:** Step-by-Step Implementation

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Architecture Decision](#architecture-decision)
4. [Setup Development Machines](#setup-development-machines)
5. [Execute Phases on Each Machine](#execute-phases)
6. [Package and Transfer](#package-and-transfer)
7. [Setup Integration System](#setup-integration-system)
8. [Run Integration](#run-integration)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## OVERVIEW

This guide walks you through setting up a distributed development environment where **5-10 developers** work in parallel on different phases of the SwarmCare project, then integrate everything into a single production-ready codebase.

### Time Savings
- **Single System**: 8-11 weeks
- **5 Systems**: 2-3 days (82% faster)
- **10 Systems**: 1-2 days (91% faster)

### Process Flow
```
1. Setup (1 hour) → 2. Execute (1-3 days) → 3. Package (30 min) → 4. Integrate (2-4 hours)
```

---

## PREREQUISITES

### Each Development Machine Needs:
- Linux/macOS/WSL2 (Windows)
- Bash shell
- Python 3.8+
- Git
- At least 20GB free disk space
- Claude Code access (or similar AI coding assistant)

### Integration System Needs:
- All of the above, plus:
- Ability to receive files from all dev machines (USB, network, cloud)
- 50GB+ free disk space

### Team Coordination:
- Communication channel (Slack, Discord, Teams)
- File transfer method agreed upon (USB, scp, cloud storage)
- One person designated as Integration Manager

---

## ARCHITECTURE DECISION

First, choose your distribution strategy based on team size.

### Option A: 5 Machines (Recommended)
**Best for:** 3-5 developers, balanced workload
**Duration:** 2-3 days
**Complexity:** Medium

```bash
cd /home/user01/claude-test/SwarmCare/start
cat machine_configs/5_machine_distribution.json
```

### Option B: 10 Machines (Maximum Speed)
**Best for:** 7-10 developers, maximum parallelization
**Duration:** 1-2 days
**Complexity:** Higher

```bash
cat machine_configs/10_machine_distribution.json
```

### Decision Matrix

| Team Size | Machines | Strategy | Coordination |
|-----------|----------|----------|--------------|
| 2-3       | 3        | Simple   | Low          |
| 3-5       | 5        | Balanced | Medium       |
| 7-10      | 10       | Maximum  | High         |

**Choose your strategy now and note the machine assignments.**

---

## SETUP DEVELOPMENT MACHINES

### Step 1: Clone Repository on Each Machine

On **EACH development machine**, run:

```bash
# Clone the repository
cd /home/user01/claude-test
git clone <your-swarmcare-repo> SwarmCare
cd SwarmCare/start

# Verify files
ls -la
# You should see: DISTRIBUTED_EXECUTOR.sh, phases/, prompts/, etc.
```

### Step 2: Review Phase Assignments

Based on your chosen strategy, each developer should know their phases.

**For 5-Machine Setup:**
- Developer 1 (machine_01): Phases 0, 1, 11, 24, 28
- Developer 2 (machine_02): Phases 2, 3, 16, 18, 20, 21, 22
- Developer 3 (machine_03): Phases 4, 5, 9, 14, 25, 26, 27
- Developer 4 (machine_04): Phases 6, 7, 10, 12, 23
- Developer 5 (machine_05): Phases 8, 13, 15, 17, 19

**For 10-Machine Setup:**
- See `machine_configs/10_machine_distribution.json`

### Step 3: Initialize Each Machine

On **EACH development machine**, run the initialization:

```bash
# For machine_01 with 5-machine setup
./DISTRIBUTED_EXECUTOR.sh init --machine-id machine_01 --phases "0,1,11,24,28"

# For machine_02 with 5-machine setup
./DISTRIBUTED_EXECUTOR.sh init --machine-id machine_02 --phases "2,3,16,18,20,21,22"

# ... etc for each machine
```

**IMPORTANT**: Replace the `--phases` parameter with the actual phases assigned to each machine!

### Step 4: Verify Initialization

```bash
# Check configuration
cat machine_config.json

# Check execution plan
cat execution_plan.json

# Verify directories
ls -la output/
```

---

## EXECUTE PHASES

### CRITICAL: Phase 0 Must Complete First!

**Machine 01** (the one with Phase 0) must complete Phase 0 before others start.

#### On Machine 01:

```bash
# Start execution
./DISTRIBUTED_EXECUTOR.sh execute

# This will:
# 1. Show the prompt for Phase 0
# 2. Wait for you to complete it with Claude Code
# 3. Create MANIFEST.json when done
```

#### Using Claude Code for Phase Execution

When the script shows a prompt:

1. **Copy the entire prompt** from the terminal
2. **Open Claude Code** in your IDE
3. **Paste the prompt** and let Claude generate all code
4. **Save all files** to the `output/phase_XX/` directory shown
5. **Run tests** if any are generated
6. **Press ENTER** in the terminal to continue

#### Notify Team When Phase 0 is Done

Once Phase 0 is complete on Machine 01:

```bash
# Verify completion
./DISTRIBUTED_EXECUTOR.sh status

# Output should show Phase 0 as COMPLETED
```

**Send message to team:** "Phase 0 complete - all machines can start!"

### All Other Machines Can Now Start

Once Phase 0 is done, **ALL other machines** execute in parallel:

#### On Each Machine (02-05 or 02-10):

```bash
# Start execution
./DISTRIBUTED_EXECUTOR.sh execute

# Follow the same process:
# 1. Copy prompt
# 2. Use Claude Code to generate code
# 3. Save to output directory
# 4. Press ENTER to continue to next phase
```

### Monitor Progress

On any machine, check status:

```bash
./DISTRIBUTED_EXECUTOR.sh status
```

### Daily Standup (Recommended)

Each developer shares:
- Phases completed yesterday
- Current phase working on
- Any blockers

---

## PACKAGE AND TRANSFER

### Step 1: Validate Each Machine

Before packaging, **validate** on each machine:

```bash
./DISTRIBUTED_EXECUTOR.sh validate
```

This checks:
- All assigned phases completed
- All MANIFEST.json files created
- Files exist in output directories

### Step 2: Package Outputs

On **EACH machine**:

```bash
./DISTRIBUTED_EXECUTOR.sh package
```

This creates:
- `machine_XX_phases.tar.gz` (the package)
- `machine_XX_phases.tar.gz.sha256` (checksum for verification)

### Step 3: Transfer to Integration System

Choose your transfer method:

#### Option A: USB Drive

```bash
# On dev machine, copy to USB
cp machine_01_phases.tar.gz* /media/usb/

# On integration system, copy from USB
cp /media/usb/machine_01_phases.tar.gz* /home/user01/claude-test/SwarmCare/start/collected_packages/
```

#### Option B: Network Transfer (scp)

```bash
# From dev machine to integration system
scp machine_01_phases.tar.gz* integration-system:/home/user01/claude-test/SwarmCare/start/collected_packages/
```

#### Option C: Cloud Storage

```bash
# Upload to cloud
# Dropbox, Google Drive, OneDrive, etc.

# Download on integration system
# Use web interface or CLI tools
```

### Step 4: Verify All Packages Received

On the **integration system**, verify all packages:

```bash
cd /home/user01/claude-test/SwarmCare/start/collected_packages

# Should see all machine packages
ls -la

# Expected files:
# machine_01_phases.tar.gz
# machine_01_phases.tar.gz.sha256
# machine_02_phases.tar.gz
# machine_02_phases.tar.gz.sha256
# ... (for all machines)
```

---

## SETUP INTEGRATION SYSTEM

### Step 1: Verify Integration Scripts

On the **integration system**:

```bash
cd /home/user01/claude-test/SwarmCare/start

# Check scripts are present
ls -la COLLECT_PHASES.sh INTEGRATE_ALL.sh phase_validator.py integration_tester.py

# All should be executable
```

If scripts are not executable:

```bash
chmod +x COLLECT_PHASES.sh INTEGRATE_ALL.sh phase_validator.py integration_tester.py
```

### Step 2: Collect All Phases

Run the collection script:

```bash
./COLLECT_PHASES.sh --source collected_packages/
```

This will:
- Extract all packages
- Verify checksums
- Organize into `collected_phases/` directory
- Check for duplicates
- Generate collection report

### Step 3: Validate Collection

```bash
./COLLECT_PHASES.sh --validate
```

This validates:
- All 29 phases present
- Each has valid MANIFEST.json
- Ready for integration flags set

### Step 4: Check Status

```bash
./COLLECT_PHASES.sh --status
```

Expected output:
```
Collected: 29 / 29
Progress: 100%
```

---

## RUN INTEGRATION

### Step 1: Dry Run (Recommended)

First, simulate the integration:

```bash
./INTEGRATE_ALL.sh --dry-run
```

This shows what would happen without making changes.

### Step 2: Run Full Integration

When ready, run the real integration:

```bash
./INTEGRATE_ALL.sh
```

This performs:
1. ✅ **Validation** - Checks all 29 phases present
2. ✅ **Dependency Check** - Verifies dependency graph
3. ✅ **Backup** - Creates backup of current state
4. ✅ **Merge** - Integrates all phases into project
5. ✅ **Conflict Detection** - Checks for conflicts
6. ✅ **Integration Tests** - Runs test suite
7. ✅ **Report Generation** - Creates comprehensive report

**Expected Duration:** 30-60 minutes

### Step 3: Review Integration Report

After integration completes:

```bash
# View the report
cat integration_reports/INTEGRATION_REPORT_*.md

# Check test results
cat test_results.json

# Review logs
tail -100 integration_logs/integration_*.log
```

### Step 4: Verify Integration

```bash
# Check project structure
ls -la ../

# Expected directories:
# backend/ frontend/ tests/ docs/
```

### Step 5: Run Manual Tests (Optional)

```bash
cd ..

# Run backend tests (if applicable)
pytest tests/

# Run frontend tests (if applicable)
npm test

# Start development servers and test manually
```

---

## TROUBLESHOOTING

### Issue: Phase 0 Not Completing

**Symptom:** Machine 01 stuck on Phase 0

**Solution:**
1. Check the prompt is valid
2. Ensure Claude Code is generating files
3. Verify files are saved to `output/phase_00/`
4. Check MANIFEST.json was created

### Issue: Missing Phases During Collection

**Symptom:** `COLLECT_PHASES.sh --validate` shows missing phases

**Solution:**
1. Check which phases are missing
2. Contact the developer assigned to those phases
3. Request they re-package and send
4. Re-run collection after receiving

### Issue: Validation Errors

**Symptom:** `phase_validator.py` reports errors

**Solution:**
1. Review validation errors
2. Check specific phases mentioned
3. Verify MANIFEST.json files are valid JSON
4. Ensure `ready_for_integration` is set to `true`

### Issue: Integration Test Failures

**Symptom:** Tests fail during integration

**Solution:**
1. Check `test_results.json` for details
2. Identify which phase has issues
3. May need to fix that phase and re-integrate
4. Use `--skip-tests` only if you understand the risks

### Issue: File Conflicts

**Symptom:** Multiple phases have same file

**Solution:**
1. This is usually expected (e.g., shared utilities)
2. Review conflict report
3. Manual resolution may be needed
4. Check if files are actually identical

### Issue: Need to Rollback

**Symptom:** Integration went wrong

**Solution:**
```bash
./INTEGRATE_ALL.sh --rollback
```

This restores from the backup created before integration.

---

## FAQ

### Q: Can we run phases out of order?

**A:** Phase 0 must complete first. After that, most phases can run in parallel, except those with specific dependencies (see phase_validator.py for the dependency graph).

### Q: What if a developer makes a mistake?

**A:** They can re-run their phases, re-package, and re-send. The integration system will detect duplicates.

### Q: Can we add more developers mid-project?

**A:** Yes! Redistribute remaining phases and continue.

### Q: What if we only have 3 developers?

**A:** Use a 3-machine distribution. Each developer gets ~10 phases.

### Q: How do we handle phase dependencies?

**A:** The phase_validator.py script automatically checks dependencies. If a phase requires another phase that's missing, validation will fail.

### Q: Can developers work on different operating systems?

**A:** Yes! The scripts work on Linux, macOS, and WSL2 (Windows).

### Q: What if transfer takes too long?

**A:** Compress packages further, or use faster transfer method (direct network vs cloud).

### Q: Do we need to test each phase before packaging?

**A:** Yes! Run `./DISTRIBUTED_EXECUTOR.sh validate` before packaging.

### Q: Can we skip the integration tests?

**A:** Not recommended. Use `./INTEGRATE_ALL.sh --skip-tests` only if you're confident or will test manually.

### Q: What if integration fails?

**A:** Review the integration log, fix issues, and re-run. Use `--rollback` if needed.

---

## QUICK REFERENCE COMMANDS

### Development Machine Commands
```bash
# Initialize
./DISTRIBUTED_EXECUTOR.sh init --machine-id <id> --phases "<list>"

# Execute
./DISTRIBUTED_EXECUTOR.sh execute

# Check status
./DISTRIBUTED_EXECUTOR.sh status

# Validate
./DISTRIBUTED_EXECUTOR.sh validate

# Package
./DISTRIBUTED_EXECUTOR.sh package
```

### Integration System Commands
```bash
# Collect phases
./COLLECT_PHASES.sh --source <dir>

# Validate collection
./COLLECT_PHASES.sh --validate

# Check status
./COLLECT_PHASES.sh --status

# Dry run integration
./INTEGRATE_ALL.sh --dry-run

# Full integration
./INTEGRATE_ALL.sh

# Rollback
./INTEGRATE_ALL.sh --rollback
```

---

## SUCCESS CHECKLIST

### Before Starting
- [ ] All developers have repository cloned
- [ ] Phase assignments distributed
- [ ] Communication channel established
- [ ] Transfer method agreed upon

### During Execution
- [ ] Phase 0 completed first
- [ ] All other phases executing in parallel
- [ ] Daily status updates shared
- [ ] Blockers communicated immediately

### Before Integration
- [ ] All phases completed
- [ ] All machines validated successfully
- [ ] All packages transferred to integration system
- [ ] Collection validation passed

### After Integration
- [ ] Integration completed without errors
- [ ] All tests passing
- [ ] Integration report reviewed
- [ ] Manual testing performed
- [ ] Ready for deployment

---

## SUPPORT

**Issues?** Contact your Integration Manager or review:
- DISTRIBUTED_ARCHITECTURE.md (architecture details)
- Integration logs (in integration_logs/)
- Test results (test_results.json)

**Questions?** Check the FAQ above or troubleshooting section.

---

**Good luck with your distributed development! 🚀**

---
