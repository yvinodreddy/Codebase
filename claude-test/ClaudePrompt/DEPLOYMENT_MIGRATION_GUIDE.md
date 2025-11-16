# ClaudePrompt/ULTRATHINK Framework - Complete Deployment Migration Guide

**Version:** 1.0.0
**Date:** 2025-11-15
**Target Success Rate:** 100%
**Deployment Type:** New Laptop Migration

================================================================================

## 📋 TABLE OF CONTENTS

1. [System Overview & Architecture](#system-overview)
2. [Current System Audit](#current-system-audit)
3. [Claims Verification](#claims-verification)
4. [Pre-Migration Checklist](#pre-migration-checklist)
5. [Step-by-Step Deployment Guide](#deployment-guide)
6. [Automated Deployment Scripts](#automated-scripts)
7. [Verification & Testing](#verification-testing)
8. [Rollback Procedures](#rollback-procedures)
9. [Troubleshooting Guide](#troubleshooting)

================================================================================

## 🎯 SYSTEM OVERVIEW & ARCHITECTURE

### The ULTRATHINK Ecosystem

The ClaudePrompt/ULTRATHINK framework consists of TWO isolated systems:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ULTRATHINK ECOSYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────────┐  │
│  │   TestPrompt System    │    │  ClaudePrompt System       │  │
│  │   (Legacy/Stable)      │    │  (Enhanced/Production)     │  │
│  ├────────────────────────┤    ├────────────────────────────┤  │
│  │ Commands:              │    │ Command:                   │  │
│  │  - ultrathinkc         │    │  - cpp                     │  │
│  │  - uc                  │    │                            │  │
│  │                        │    │                            │  │
│  │ Output:                │    │ Output:                    │  │
│  │  /tmp/ultrathink_      │    │  ClaudePrompt/tmp/         │  │
│  │  output.txt            │    │  cppultrathink_output_     │  │
│  │                        │    │  {timestamp}.txt           │  │
│  │                        │    │                            │  │
│  │ answer_to_file.py:     │    │ answer_to_file.py:         │  │
│  │  TestPrompt/           │    │  ClaudePrompt/             │  │
│  └────────────────────────┘    └────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
/home/user01/
└── claude-test/
    ├── CLAUDE.md                          ← Global rules (root level)
    ├── TestPrompt/                        ← Legacy ULTRATHINK system
    │   ├── ultrathink.py
    │   ├── answer_to_file.py
    │   └── CLAUDE.md
    └── ClaudePrompt/                      ← Primary deployment target
        ├── CLAUDE.md                      ← Project-specific rules
        ├── cpp                            ← Main wrapper script
        ├── ultrathink.py                  ← Core orchestrator
        ├── get_output_path.py             ← Timestamp generator
        ├── answer_to_file.py              ← Answer appender
        ├── master_orchestrator.py         ← Orchestration engine
        ├── config.py                      ← Configuration
        ├── requirements.txt               ← Python dependencies
        ├── agent_framework/               ← 12 agent components
        ├── guardrails/                    ← 8-layer validation
        ├── security/                      ← 7 security modules
        ├── tmp/                           ← Timestamped outputs
        └── web-ui-implementation/         ← Next.js WebUI
            ├── package.json
            └── .env.local

```

================================================================================

## ✅ CURRENT SYSTEM AUDIT - VERIFIED CONFIGURATION

### 1. Bashrc Aliases & Environment Variables

**Location:** `~/.bashrc`

```bash
# Claude Code Configuration
alias cc="claude --dangerously-skip-permissions"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=200000

# ULTRATHINK - TestPrompt System
alias ultrathinkc="python3 /home/user01/claude-test/TestPrompt/ultrathink.py"
alias uc="python3 /home/user01/claude-test/TestPrompt/ultrathink.py"

# ClaudePrompt - Primary ULTRATHINK Instance
alias cpp="/home/user01/claude-test/ClaudePrompt/cpp"

# Quick Navigation Aliases
alias cdtp='cd /home/user01/claude-test/TestPrompt'
alias cdcp='cd /home/user01/claude-test/ClaudePrompt'

# PATH Configuration
export PATH="$HOME/bin:$PATH"
```

### 2. File Permissions

```
File                          Permissions   Owner        Executable
────────────────────────────  ───────────   ──────────   ──────────
cpp                           755           user01       YES
ultrathink.py                 755           user01       YES
get_output_path.py            755           user01       YES
answer_to_file.py             644           user01       NO
master_orchestrator.py        644           user01       NO
config.py                     644           user01       NO
```

### 3. Python Dependencies (requirements.txt)

**Core Dependencies:**
- anthropic >= 0.18.0
- python-dotenv >= 1.0.0
- pyyaml >= 6.0.1
- requests >= 2.31.0
- tenacity >= 8.2.3
- dataclasses-json >= 0.6.0

**Testing:**
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- pytest-asyncio >= 0.21.0
- pytest-mock >= 3.11.1

**Code Quality:**
- black >= 23.7.0
- flake8 >= 6.1.0
- mypy >= 1.5.0
- pylint >= 2.17.5

**Optional:**
- crewai >= 0.1.0
- numpy >= 1.24.0
- scipy >= 1.11.0

### 4. WebUI Dependencies (package.json)

**Runtime:**
- next: ^14.0.4
- react: ^18.2.0
- @anthropic-ai/sdk: ^0.9.1
- next-auth: ^4.24.5
- axios: ^1.6.2

**Security:**
- isomorphic-dompurify: ^2.32.0
- validator: ^13.15.23
- zod: ^3.22.4

### 5. System Requirements

**Python:**
- Version: 3.12.3
- Location: /usr/bin/python3

**Node.js (for WebUI):**
- Required: v18+ or v20+
- Package Manager: npm or pnpm

**System Tools:**
- bash >= 4.0
- git
- curl
- dos2unix (optional, for line endings)

================================================================================

## ✅ CLAIMS VERIFICATION REPORT

**User Claim Verification Results:**

### ✅ CLAIM 1: Folder-level modifications
**Status:** VERIFIED - 100% Accurate

**Evidence:**
- ClaudePrompt/CLAUDE.md: Custom project rules defined
- ClaudePrompt/tmp/: Custom output directory created
- ClaudePrompt/web-ui-implementation/: WebUI framework integrated

### ✅ CLAIM 2: System-level modifications (bashrc)
**Status:** VERIFIED - 100% Accurate

**Evidence:**
```bash
# From ~/.bashrc
alias cpp="/home/user01/claude-test/ClaudePrompt/cpp"
alias ultrathinkc="python3 /home/user01/claude-test/TestPrompt/ultrathink.py"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=200000
```

**Functionality:** Execute from ANY directory using absolute paths

### ✅ CLAIM 3: Root-level CLAUDE.md configuration
**Status:** VERIFIED - 100% Accurate

**Evidence:**
- File exists: /home/user01/claude-test/CLAUDE.md
- Contains: Global ULTRATHINK execution protocol
- Contains: Time limit policy (no time constraints)
- Contains: API usage prohibition (Claude Code only)

### ✅ CLAIM 4: Full access permissions (root & temp)
**Status:** VERIFIED - 100% Accurate

**Evidence:**
- Root access: Read/write to /home/user01/claude-test/
- Temp access: Write to /tmp/ and ClaudePrompt/tmp/
- Execution from any folder: Enabled via bashrc aliases

### ✅ CLAIM 5: Multiple CLAUDE.md files with different purposes
**Status:** VERIFIED - 100% Accurate

**Files:**
1. `/home/user01/claude-test/CLAUDE.md` → Global rules
2. `/home/user01/claude-test/ClaudePrompt/CLAUDE.md` → Project rules
3. `/home/user01/claude-test/TestPrompt/CLAUDE.md` → Legacy system rules

**All claims verified. Current system architecture is correctly documented.**

================================================================================

## 📦 PRE-MIGRATION CHECKLIST

### Phase 1: Source System (Current Laptop)

- [ ] Backup entire claude-test directory
- [ ] Export ~/.bashrc configuration
- [ ] Document Python version (python3 --version)
- [ ] Export pip3 package list (pip3 freeze > requirements_full.txt)
- [ ] Test all commands (cpp, ultrathinkc, uc)
- [ ] Verify WebUI builds successfully
- [ ] Create migration package

### Phase 2: Target System (New Laptop)

- [ ] Install Python 3.12+
- [ ] Install Node.js 18+ (for WebUI)
- [ ] Install git
- [ ] Create user directory structure
- [ ] Verify shell is bash

### Phase 3: Validation

- [ ] Checksum verification of transferred files
- [ ] Permission verification
- [ ] Dependency installation
- [ ] End-to-end testing

================================================================================

## 🚀 STEP-BY-STEP DEPLOYMENT GUIDE

### STEP 1: Prepare Migration Package on Source System

```bash
# 1.1. Navigate to claude-test parent directory
cd /home/user01

# 1.2. Create migration package
tar -czf claudeprompt_migration_$(date +%Y%m%d).tar.gz \
    claude-test/ClaudePrompt \
    claude-test/TestPrompt \
    claude-test/CLAUDE.md

# 1.3. Export bashrc configuration
grep -A 20 "Claude Code\|ULTRATHINK\|ClaudePrompt" ~/.bashrc > claudeprompt_bashrc_config.txt

# 1.4. Export full Python dependencies
pip3 freeze > claudeprompt_python_deps.txt

# 1.5. Create checksum
sha256sum claudeprompt_migration_$(date +%Y%m%d).tar.gz > migration_checksum.txt

# 1.6. Package everything
mkdir claudeprompt_deployment
mv claudeprompt_migration_*.tar.gz claudeprompt_deployment/
mv claudeprompt_bashrc_config.txt claudeprompt_deployment/
mv claudeprompt_python_deps.txt claudeprompt_deployment/
mv migration_checksum.txt claudeprompt_deployment/
```

### STEP 2: Transfer to New Laptop

```bash
# Option A: USB Drive
cp -r claudeprompt_deployment /media/usb/

# Option B: Network Transfer
scp -r claudeprompt_deployment user@new-laptop:/home/user/

# Option C: Cloud Storage
# Upload to Dropbox/Google Drive/OneDrive
```

### STEP 3: Install Prerequisites on New Laptop

```bash
# 3.1. Update system
sudo apt update && sudo apt upgrade -y

# 3.2. Install Python 3.12+ (if not present)
sudo apt install python3 python3-pip python3-venv -y

# 3.3. Install Node.js 18+ (for WebUI)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 3.4. Install system tools
sudo apt install git curl dos2unix -y

# 3.5. Verify installations
python3 --version  # Should show 3.12+
node --version     # Should show v18+ or v20+
npm --version
```

### STEP 4: Extract and Deploy

```bash
# 4.1. Create directory structure
mkdir -p /home/user01/claude-test
cd /home/user01

# 4.2. Extract migration package
tar -xzf claudeprompt_deployment/claudeprompt_migration_*.tar.gz

# 4.3. Verify checksum
sha256sum -c claudeprompt_deployment/migration_checksum.txt

# 4.4. Set correct permissions
chmod 755 claude-test/ClaudePrompt/cpp
chmod 755 claude-test/ClaudePrompt/ultrathink.py
chmod 755 claude-test/ClaudePrompt/get_output_path.py
chmod 755 claude-test/TestPrompt/ultrathink.py
chmod 644 claude-test/ClaudePrompt/answer_to_file.py
chmod 644 claude-test/TestPrompt/answer_to_file.py

# 4.5. Create tmp directories
mkdir -p claude-test/ClaudePrompt/tmp
mkdir -p claude-test/TestPrompt/tmp
chmod 755 claude-test/ClaudePrompt/tmp
chmod 755 claude-test/TestPrompt/tmp
```

### STEP 5: Configure Bashrc

```bash
# 5.1. Backup existing bashrc
cp ~/.bashrc ~/.bashrc.backup

# 5.2. Add ULTRATHINK configuration
cat >> ~/.bashrc << 'EOF'

# ============================================================================
# CLAUDE CODE & ULTRATHINK CONFIGURATION
# ============================================================================

# Claude Code Aliases
alias cc="claude --dangerously-skip-permissions"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=200000  # Claude Max $200/month - 200K token limit

# CRITICAL: NEVER USE API - NO CHARGES ALLOWED
# export ANTHROPIC_API_KEY=""  # NEVER UNCOMMENT THIS LINE

# ULTRATHINKC - TestPrompt System (Legacy/Stable)
alias ultrathinkc="python3 /home/user01/claude-test/TestPrompt/ultrathink.py"
alias uc="python3 /home/user01/claude-test/TestPrompt/ultrathink.py"

# ClaudePrompt - Primary ULTRATHINK Instance (Production)
alias cpp="/home/user01/claude-test/ClaudePrompt/cpp"

# Quick Navigation Aliases
alias cdtp='cd /home/user01/claude-test/TestPrompt'
alias cdcp='cd /home/user01/claude-test/ClaudePrompt'

# PATH Configuration
export PATH="$HOME/bin:$PATH"

# ============================================================================
EOF

# 5.3. Reload bashrc
source ~/.bashrc

# 5.4. Verify aliases
alias | grep -E "cpp|ultrathink|uc"
```

### STEP 6: Install Python Dependencies

```bash
# 6.1. Navigate to ClaudePrompt
cd /home/user01/claude-test/ClaudePrompt

# 6.2. Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 6.3. Install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 6.4. Verify critical packages
pip3 list | grep -E "anthropic|requests|pytest"

# 6.5. Install TestPrompt dependencies (if different)
cd /home/user01/claude-test/TestPrompt
pip3 install -r requirements.txt  # If exists
```

### STEP 7: Install WebUI Dependencies (Optional)

```bash
# 7.1. Navigate to WebUI
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation

# 7.2. Install Node modules
npm install

# Or use pnpm for faster installation
# npm install -g pnpm
# pnpm install

# 7.3. Copy environment template
cp .env.example .env.local

# 7.4. Test build
npm run build
```

### STEP 8: Verification & Testing

```bash
# Run the automated verification script (see next section)
bash /home/user01/claude-test/ClaudePrompt/deployment_verification.sh
```

================================================================================

## 🤖 AUTOMATED DEPLOYMENT SCRIPTS

**Note:** Automated scripts will be created in next step.

================================================================================

## ✅ VERIFICATION & TESTING

### Quick Verification Commands

```bash
# Test 1: Verify cpp command
cpp "test: Hello World" --verbose

# Test 2: Verify ultrathinkc command
ultrathinkc "test: 2+2" --verbose

# Test 3: Check output files
ls -la /home/user01/claude-test/ClaudePrompt/tmp/
ls -la /tmp/ultrathink_output.txt

# Test 4: Verify Python imports
python3 -c "import anthropic; print('anthropic OK')"
python3 -c "from claude_test.ClaudePrompt import config; print('config OK')"

# Test 5: Verify permissions
ls -la /home/user01/claude-test/ClaudePrompt/cpp
ls -la /home/user01/claude-test/ClaudePrompt/ultrathink.py
```

### End-to-End Test

```bash
# Test full ULTRATHINK workflow
cpp "Analyze the number 42 and explain its significance in mathematics, computer science, and popular culture. Provide a comprehensive answer with multiple verification methods." --verbose

# Check the output file
OUTPUT_FILE=$(ls -t /home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_*.txt | head -1)
cat "$OUTPUT_FILE"
```

================================================================================

## 🔄 ROLLBACK PROCEDURES

### If Deployment Fails

```bash
# 1. Restore bashrc
cp ~/.bashrc.backup ~/.bashrc
source ~/.bashrc

# 2. Remove deployed files
rm -rf /home/user01/claude-test

# 3. Review logs
cat /tmp/deployment_verification.log

# 4. Check Python errors
python3 /home/user01/claude-test/ClaudePrompt/ultrathink.py --help
```

### Common Issues & Fixes

**Issue 1: Permission Denied on cpp**
```bash
chmod 755 /home/user01/claude-test/ClaudePrompt/cpp
```

**Issue 2: Python Module Not Found**
```bash
pip3 install -r /home/user01/claude-test/ClaudePrompt/requirements.txt
```

**Issue 3: Alias Not Found**
```bash
source ~/.bashrc
```

================================================================================

## 🔧 TROUBLESHOOTING GUIDE

### Problem: "cpp: command not found"

**Solution:**
```bash
# Check if alias is defined
alias | grep cpp

# If not, reload bashrc
source ~/.bashrc

# Verify path
ls -la /home/user01/claude-test/ClaudePrompt/cpp
```

### Problem: "Permission denied when executing cpp"

**Solution:**
```bash
chmod 755 /home/user01/claude-test/ClaudePrompt/cpp
```

### Problem: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:**
```bash
pip3 install anthropic
# Or install all dependencies
pip3 install -r /home/user01/claude-test/ClaudePrompt/requirements.txt
```

### Problem: "Output file not created"

**Solution:**
```bash
# Check tmp directory exists
mkdir -p /home/user01/claude-test/ClaudePrompt/tmp

# Check permissions
chmod 755 /home/user01/claude-test/ClaudePrompt/tmp

# Verify get_output_path.py is executable
chmod 755 /home/user01/claude-test/ClaudePrompt/get_output_path.py
```

================================================================================

## 📊 SUCCESS CRITERIA

Deployment is 100% successful when ALL of the following are TRUE:

- [ ] ✅ All aliases work from any directory
- [ ] ✅ cpp command executes without errors
- [ ] ✅ ultrathinkc command executes without errors
- [ ] ✅ Output files are created with timestamps
- [ ] ✅ answer_to_file.py appends answers correctly
- [ ] ✅ All Python dependencies installed
- [ ] ✅ WebUI builds successfully (if deployed)
- [ ] ✅ End-to-end test produces valid output
- [ ] ✅ All 8 guardrail layers active
- [ ] ✅ Permissions are correct (755 for executables, 644 for data)

================================================================================

## 📝 POST-DEPLOYMENT CHECKLIST

After successful deployment:

- [ ] Run comprehensive test suite
- [ ] Document new laptop hostname/IP
- [ ] Update any hardcoded paths (if any)
- [ ] Test from different directories
- [ ] Verify WebUI accessibility (if deployed)
- [ ] Create backup of new system
- [ ] Test rollback procedure
- [ ] Archive migration package

================================================================================

**Deployment Guide Version:** 1.0.0
**Last Updated:** 2025-11-15
**Maintainer:** ULTRATHINK Framework Team
**Support:** See CLAUDE.md for framework documentation

================================================================================
