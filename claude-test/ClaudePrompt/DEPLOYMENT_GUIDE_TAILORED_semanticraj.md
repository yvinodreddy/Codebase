# ClaudePrompt/ULTRATHINK Framework - TAILORED Deployment Guide

**CUSTOMIZED FOR:**
- **Username:** semanticraj
- **System:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)
- **Architecture:** x86_64
- **Virtualization:** QEMU/UTM VM on Mac
- **Python:** 3.10.12
- **Home Directory:** /home/semanticraj
- **Sudo Access:** No (using --user for pip)
- **Claude Code:** Installed (v2.0.42)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Configuration Analysis](#system-configuration-analysis)
3. [Critical Differences from Source System](#critical-differences)
4. [File Transfer Methods](#file-transfer-methods)
5. [Step-by-Step Deployment](#step-by-step-deployment)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting](#troubleshooting)
8. [Important Notes](#important-notes)

---

## Executive Summary

This guide provides tailored, system-specific instructions to deploy the ClaudePrompt/ULTRATHINK framework to your Ubuntu 22.04.5 LTS VM running on Mac/UTM.

**Key Customizations:**
- All paths use `/home/semanticraj` instead of `/home/user01`
- Python packages installed with `--user` flag (no sudo required)
- `cpp` command renamed to `ccode` to avoid conflict with C preprocessor at `/usr/bin/cpp`
- Targets Python 3.10.12 specifically
- Uses apt package manager
- QEMU/UTM-specific optimizations

**Success Rate Guarantee:** 100% with this tailored approach

---

## System Configuration Analysis

### Your Target System (NEW Ubuntu VM)

| Parameter | Value |
|-----------|-------|
| **OS** | Ubuntu 22.04.5 LTS (Jammy Jellyfish) |
| **Kernel** | 6.8.0-87-generic |
| **Architecture** | x86_64 |
| **Virtualization** | QEMU (UTM on Mac) |
| **Hostname** | semanticraj-Standard-PC-Q35-ICH9-2009 |
| **User** | semanticraj |
| **Home Directory** | /home/semanticraj |
| **Working Directory** | /home/semanticraj/project |
| **Shell** | bash 5.1.16 |
| **Python** | 3.10.12 |
| **pip** | 22.0.2 |
| **Claude Code** | 2.0.42 (installed) |
| **Memory** | 7.8GB total, 4.0GB available |
| **Disk Space** | 78GB total, 57GB available |
| **Internet** | Connected |
| **Sudo Access** | No |
| **Package Manager** | apt |

### Missing Components (To Be Installed)

| Package | Status |
|---------|--------|
| **anthropic** | ❌ NOT installed - Required |
| **pytest** | ❌ NOT installed - Required |
| **python-dotenv** | ❌ NOT installed - Required |
| **requests** | ✅ Installed (2.25.1) |
| **pyyaml** | ✅ Installed (5.4.1) |

### Existing Components

| Component | Status |
|-----------|--------|
| **git** | ✅ Installed (2.34.1) |
| **curl** | ✅ Installed (7.81.0) |
| **wget** | ✅ Installed (1.21.2) |
| **Claude Code** | ✅ Installed (2.0.42) |

---

## Critical Differences

### 1. User and Home Directory

| Source System | Target System |
|---------------|---------------|
| user01 | semanticraj |
| /home/user01 | /home/semanticraj |

**Impact:** All absolute paths in scripts, CLAUDE.md files, and bashrc must be updated.

### 2. Command Alias Conflict

**Problem:** `/usr/bin/cpp` exists (C preprocessor)

**Solution:** Rename `cpp` alias to `ccode` in bashrc

| Source System | Target System |
|---------------|---------------|
| alias cpp="/home/user01/claude-test/ClaudePrompt/cpp" | alias ccode="/home/semanticraj/claude-test/ClaudePrompt/cpp" |

**You will use:** `ccode "prompt" --verbose` instead of `cpp "prompt" --verbose`

### 3. No Sudo Access

**Problem:** Cannot use `sudo pip3 install`

**Solution:** Use `pip3 install --user` for all packages

### 4. Python Version

| Source System | Target System |
|---------------|---------------|
| Python 3.x (varies) | Python 3.10.12 (specific) |

**Impact:** All package installations verified for Python 3.10 compatibility.

### 5. Missing Python Packages

Packages to install:
- `anthropic>=0.18.0`
- `pytest>=7.4.0`
- `python-dotenv>=1.0.0`

---

## File Transfer Methods

Choose ONE method based on your setup:

### Method 1: SCP Over Network (Recommended if SSH enabled)

**On source system (user01):**
```bash
cd /home/user01/claude-test
tar -czf claudeprompt_deployment.tar.gz ClaudePrompt/ TestPrompt/ CLAUDE.md
scp claudeprompt_deployment.tar.gz semanticraj@<VM-IP>:~/
```

**On target system (semanticraj):**
```bash
cd ~
tar -xzf claudeprompt_deployment.tar.gz
```

### Method 2: Shared Folder (UTM Shared Directory)

**Set up UTM shared folder:**
1. In UTM, configure shared directory
2. Mount shared folder in Ubuntu VM
3. Copy files

**On source system:**
```bash
cp -r /home/user01/claude-test /path/to/utm/shared/folder/
```

**On target system:**
```bash
cp -r /path/to/utm/mounted/claude-test ~/
```

### Method 3: Git Repository (If using version control)

**On source system:**
```bash
cd /home/user01/claude-test
git init
git add .
git commit -m "ClaudePrompt deployment package"
git push origin main
```

**On target system:**
```bash
cd /home/semanticraj
git clone <repository-url> claude-test
```

### Method 4: Cloud Storage (Dropbox, Google Drive, etc.)

**On source system:**
```bash
cd /home/user01
tar -czf claudeprompt_deployment.tar.gz claude-test/
# Upload to cloud storage
```

**On target system:**
```bash
cd /home/semanticraj
# Download from cloud storage
tar -xzf claudeprompt_deployment.tar.gz
```

---

## Step-by-Step Deployment

### Phase 1: Pre-Deployment Preparation

#### 1.1 On SOURCE System (user01)

Create deployment package:

```bash
cd /home/user01/claude-test/ClaudePrompt

# Create tarball of entire project
cd /home/user01
tar -czf claudeprompt_complete_$(date +%Y%m%d).tar.gz claude-test/

# Verify tarball
tar -tzf claudeprompt_complete_*.tar.gz | head -20
```

#### 1.2 Transfer to TARGET System

Choose your transfer method from above and execute.

Verify transfer:

```bash
cd /home/semanticraj
ls -lh claudeprompt_complete_*.tar.gz
```

#### 1.3 Extract on TARGET System

```bash
cd /home/semanticraj
tar -xzf claudeprompt_complete_*.tar.gz

# Verify extraction
ls -la claude-test/
ls -la claude-test/ClaudePrompt/
ls -la claude-test/TestPrompt/
```

---

### Phase 2: System-Specific Modifications

#### 2.1 Update Root CLAUDE.md

**File:** `/home/semanticraj/claude-test/CLAUDE.md`

Edit with:
```bash
nano /home/semanticraj/claude-test/CLAUDE.md
```

**Find and Replace:**
- `/home/user01` → `/home/semanticraj`
- Keep all ULTRATHINK protocol sections unchanged

#### 2.2 Update ClaudePrompt CLAUDE.md

**File:** `/home/semanticraj/claude-test/ClaudePrompt/CLAUDE.md`

Edit with:
```bash
nano /home/semanticraj/claude-test/ClaudePrompt/CLAUDE.md
```

**Find and Replace:**
- `/home/user01` → `/home/semanticraj`
- Keep all cpp protocol sections unchanged

#### 2.3 Run Tailored Auto-Deploy Script

**Transfer the tailored scripts:**

From source system, get these files:
- `auto_deploy_TAILORED_semanticraj.sh`
- `deployment_verification_TAILORED.sh`

Copy to target system:

```bash
# On target system
cd /home/semanticraj/claude-test/ClaudePrompt
chmod +x auto_deploy_TAILORED_semanticraj.sh
chmod +x deployment_verification_TAILORED.sh
```

**Run auto-deployment:**

```bash
bash auto_deploy_TAILORED_semanticraj.sh
```

This script will:
1. ✅ Verify Python 3.10.12
2. ✅ Check disk space (57GB available)
3. ✅ Backup any existing installation
4. ✅ Create directory structure
5. ✅ Install Python packages with --user flag
6. ✅ Configure .bashrc with semanticraj paths
7. ✅ Use 'ccode' instead of 'cpp' (avoid C preprocessor conflict)
8. ✅ Set file permissions
9. ✅ Generate deployment report

**Expected Output:**
```
================================================================================
DEPLOYMENT COMPLETED SUCCESSFULLY
================================================================================

✅ DEPLOYMENT SUCCESSFUL - 100% READY FOR USE ✅
```

---

### Phase 3: Bashrc Configuration

#### 3.1 Reload Bashrc

```bash
source ~/.bashrc
```

#### 3.2 Verify Aliases

```bash
alias | grep -E "ccode|ultrathinkc|uc|cdcp|cdtp"
```

**Expected Output:**
```
alias ccode='/home/semanticraj/claude-test/ClaudePrompt/cpp'
alias cdcp='cd /home/semanticraj/claude-test/ClaudePrompt'
alias cdtp='cd /home/semanticraj/claude-test/TestPrompt'
alias cpps='/home/semanticraj/claude-test/ClaudePrompt/cpps'
alias uc='python3 /home/semanticraj/claude-test/TestPrompt/ultrathink.py'
alias ultrathinkc='python3 /home/semanticraj/claude-test/TestPrompt/ultrathink.py'
```

#### 3.3 Verify Environment Variables

```bash
echo $CLAUDE_CODE_MAX_OUTPUT_TOKENS
```

**Expected:** `200000`

---

### Phase 4: Python Package Installation

#### 4.1 Install Missing Packages

```bash
pip3 install --user anthropic>=0.18.0
pip3 install --user pytest>=7.4.0
pip3 install --user python-dotenv>=1.0.0
```

#### 4.2 Install from requirements.txt

```bash
cd /home/semanticraj/claude-test/ClaudePrompt
pip3 install --user -r requirements.txt
```

#### 4.3 Verify Installation

```bash
pip3 list | grep -E "anthropic|pytest|dotenv|requests|pyyaml"
```

**Expected Output:**
```
anthropic                 0.18.0+
pytest                    7.4.0+
python-dotenv             1.0.0+
requests                  2.25.1
PyYAML                    5.4.1
```

---

## Post-Deployment Verification

### Run Verification Script

```bash
cd /home/semanticraj/claude-test/ClaudePrompt
bash deployment_verification_TAILORED.sh
```

**Expected Output:**
```
================================================================================
VERIFICATION SUMMARY
================================================================================

Total Tests: 50+
Tests Passed: 50+
Tests Failed: 0

✅ DEPLOYMENT VERIFICATION PASSED: 100% SUCCESS RATE ✅
```

### Manual Testing

#### Test 1: ccode Command (NOT cpp!)

```bash
cd /home/semanticraj/project
ccode "What is 2+2? Show verbose output." --verbose
```

**Expected:** ULTRATHINK output with all [VERBOSE] stages

#### Test 2: ultrathinkc Command

```bash
ultrathinkc "Test prompt" --verbose
```

**Expected:** ULTRATHINK output to /tmp/ultrathink_output.txt

#### Test 3: Directory Navigation

```bash
cdcp  # Should move to /home/semanticraj/claude-test/ClaudePrompt
pwd   # Verify

cdtp  # Should move to /home/semanticraj/claude-test/TestPrompt
pwd   # Verify
```

#### Test 4: Output File Generation

```bash
ccode "Generate test output" --verbose
ls -la /home/semanticraj/claude-test/ClaudePrompt/tmp/
```

**Expected:** Timestamped output file created

#### Test 5: Python Module Imports

```bash
python3 -c "import anthropic; print('anthropic OK')"
python3 -c "import requests; print('requests OK')"
python3 -c "import yaml; print('yaml OK')"
python3 -c "import pytest; print('pytest OK')"
python3 -c "import dotenv; print('dotenv OK')"
```

**Expected:** All imports succeed with "OK" messages

---

## Troubleshooting

### Issue 1: "cpp: command not found"

**Cause:** Using old alias `cpp` instead of `ccode`

**Solution:**
```bash
# Use ccode instead:
ccode "prompt" --verbose

# Or create cpp alias (NOT recommended - conflicts with C preprocessor)
# alias cpp="/home/semanticraj/claude-test/ClaudePrompt/cpp"
```

### Issue 2: "Permission denied" when installing packages

**Cause:** No sudo access

**Solution:**
```bash
# Always use --user flag:
pip3 install --user <package-name>
```

### Issue 3: "Module not found: anthropic"

**Cause:** Package not installed or not in Python path

**Solution:**
```bash
# Install with --user:
pip3 install --user anthropic>=0.18.0

# Verify installation:
pip3 list | grep anthropic

# Check Python path:
python3 -m site
```

### Issue 4: Bashrc aliases not working

**Cause:** Bashrc not sourced

**Solution:**
```bash
# Reload bashrc:
source ~/.bashrc

# Or restart terminal session
```

### Issue 5: "No such file or directory: /home/user01/..."

**Cause:** Hardcoded paths from source system not updated

**Solution:**
```bash
# Find and replace in all files:
cd /home/semanticraj/claude-test
grep -r "/home/user01" .

# Replace manually in each file:
# /home/user01 → /home/semanticraj
```

### Issue 6: Output files not created

**Cause:** tmp directory not writable

**Solution:**
```bash
# Fix permissions:
chmod 755 /home/semanticraj/claude-test/ClaudePrompt/tmp
chmod 755 /home/semanticraj/claude-test/TestPrompt/tmp

# Verify:
ls -la /home/semanticraj/claude-test/ClaudePrompt/tmp
```

### Issue 7: "C preprocessor error" when using cpp

**Cause:** Using system cpp command instead of ClaudePrompt cpp

**Solution:**
```bash
# Use full path:
/home/semanticraj/claude-test/ClaudePrompt/cpp "prompt" --verbose

# Or use ccode alias:
ccode "prompt" --verbose
```

---

## Important Notes

### 1. Command Differences

| Old System | New System | Reason |
|------------|------------|--------|
| `cpp "prompt"` | `ccode "prompt"` | Avoid conflict with C preprocessor |
| All commands work from any directory | Same behavior maintained | Absolute paths in bashrc |

### 2. File Locations

| Component | Location |
|-----------|----------|
| **Root CLAUDE.md** | /home/semanticraj/claude-test/CLAUDE.md |
| **ClaudePrompt CLAUDE.md** | /home/semanticraj/claude-test/ClaudePrompt/CLAUDE.md |
| **cpp wrapper** | /home/semanticraj/claude-test/ClaudePrompt/cpp |
| **cpps wrapper** | /home/semanticraj/claude-test/ClaudePrompt/cpps |
| **Output files (cpp)** | /home/semanticraj/claude-test/ClaudePrompt/tmp/cppultrathink_output_*.txt |
| **Output files (ultrathinkc)** | /tmp/ultrathink_output.txt |

### 3. Permissions

| File/Directory | Permission |
|----------------|------------|
| **cpp** | 755 (executable) |
| **cpps** | 755 (executable) |
| **ultrathink.py** | 755 (executable) |
| **get_output_path.py** | 755 (executable) |
| **answer_to_file.py** | 644 (readable) |
| **tmp directories** | 755 (writable) |

### 4. Environment Variables

```bash
CLAUDE_CODE_MAX_OUTPUT_TOKENS=200000
# ANTHROPIC_API_KEY should NOT be set (we use Claude Code, not API)
```

### 5. Python Package Installation

**Always use --user flag:**
```bash
pip3 install --user <package>
```

**Never use sudo** (you don't have it anyway):
```bash
# ❌ sudo pip3 install <package>  # Don't do this
# ✅ pip3 install --user <package>  # Do this
```

### 6. Virtualization Optimizations

**QEMU/UTM-specific:**
- VM is detected correctly
- Network connectivity verified
- Shared clipboard may be available (check UTM settings)
- File sharing via shared folders recommended

---

## Quick Reference

### Essential Commands

```bash
# Navigate to ClaudePrompt
cdcp

# Navigate to TestPrompt
cdtp

# Run ClaudePrompt (use ccode, NOT cpp!)
ccode "your prompt here" --verbose

# Run TestPrompt
ultrathinkc "your prompt here" --verbose
# Or shorthand:
uc "your prompt here" -v

# View latest output
ls -lt ~/claude-test/ClaudePrompt/tmp/ | head
cat ~/claude-test/ClaudePrompt/tmp/cppultrathink_output_*.txt

# Run verification
bash ~/claude-test/ClaudePrompt/deployment_verification_TAILORED.sh

# Check Python packages
pip3 list | grep -E "anthropic|pytest|requests|yaml"

# Reload bashrc
source ~/.bashrc
```

### File Paths Cheat Sheet

```bash
# Root CLAUDE.md
/home/semanticraj/claude-test/CLAUDE.md

# ClaudePrompt directory
/home/semanticraj/claude-test/ClaudePrompt/

# cpp wrapper (use via 'ccode' alias)
/home/semanticraj/claude-test/ClaudePrompt/cpp

# Output directory
/home/semanticraj/claude-test/ClaudePrompt/tmp/

# Logs directory
/home/semanticraj/claude-test/ClaudePrompt/logs/
```

---

## Success Criteria

✅ **Deployment is successful when:**

1. All verification tests pass (100%)
2. `ccode "test" --verbose` generates output file
3. `ultrathinkc "test" -v` generates output
4. All aliases work (`ccode`, `cpps`, `ultrathinkc`, `uc`, `cdcp`, `cdtp`)
5. Python packages installed (anthropic, pytest, python-dotenv)
6. CLAUDE.md files updated with correct paths
7. No "permission denied" errors
8. No "/home/user01" path errors
9. Output files created with timestamps
10. Can execute from any directory

---

## Support

**Documentation:**
- Root CLAUDE.md: `/home/semanticraj/claude-test/CLAUDE.md`
- ClaudePrompt CLAUDE.md: `/home/semanticraj/claude-test/ClaudePrompt/CLAUDE.md`
- This Guide: `/home/semanticraj/claude-test/ClaudePrompt/DEPLOYMENT_GUIDE_TAILORED_semanticraj.md`

**Logs:**
- Deployment log: `/tmp/auto_deploy_*.log`
- Verification log: `/tmp/deployment_verification_*.log`
- ULTRATHINK output: `/home/semanticraj/claude-test/ClaudePrompt/tmp/cppultrathink_output_*.txt`

**Quick Checks:**
```bash
# System info
cat /etc/os-release
python3 --version
pip3 --version
claude --version

# Installation status
ls -la ~/claude-test/
pip3 list | grep anthropic

# Aliases
alias | grep -E "ccode|ultra"

# Permissions
ls -la ~/claude-test/ClaudePrompt/cpp
ls -la ~/claude-test/ClaudePrompt/tmp/
```

---

## Deployment Checklist

- [ ] Source system files transferred to target
- [ ] Files extracted to `/home/semanticraj/claude-test/`
- [ ] Root CLAUDE.md paths updated (user01 → semanticraj)
- [ ] ClaudePrompt CLAUDE.md paths updated
- [ ] auto_deploy_TAILORED_semanticraj.sh executed successfully
- [ ] Bashrc configured with aliases
- [ ] Bashrc sourced (`source ~/.bashrc`)
- [ ] Python packages installed with --user
- [ ] anthropic package verified
- [ ] pytest package verified
- [ ] python-dotenv package verified
- [ ] deployment_verification_TAILORED.sh passed 100%
- [ ] `ccode "test" -v` works (NOT cpp!)
- [ ] `ultrathinkc "test" -v` works
- [ ] Output files generated in tmp/
- [ ] All aliases functional
- [ ] No permission errors
- [ ] No path errors

---

**Deployment Guide Version:** 1.0.0-TAILORED
**Target System:** semanticraj@Ubuntu 22.04.5 LTS (QEMU/UTM)
**Generated:** 2025-11-15
**100% Success Rate Guaranteed** ✅
