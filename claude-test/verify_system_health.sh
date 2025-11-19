#!/usr/bin/env bash
################################################################################
# SYSTEM HEALTH CHECK: ULTRATHINK Systems
#
# Purpose: Verify health and integrity of TestPrompt and ClaudePrompt systems
# Location: /home/user01/claude-test/verify_system_health.sh
# Date: 2025-11-19
# Version: 1.0.0
#
# What this script checks:
# 1. Directory structure integrity
# 2. File count and disk usage
# 3. Git synchronization status
# 4. Script executability
# 5. Python dependencies
# 6. Recent activity
# 7. System cleanup status
#
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
TESTPROMPT_DIR="/home/user01/claude-test/TestPrompt"
CLAUDEPROMPT_DIR="/home/user01/claude-test/ClaudePrompt"
LOG_FILE="$HOME/logs/health_check_$(date +%Y%m%d).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Logging functions
log() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

pass() {
    echo -e "${GREEN}[✓ PASS]${NC} $1" | tee -a "$LOG_FILE"
    ((PASSED++))
}

fail() {
    echo -e "${RED}[✗ FAIL]${NC} $1" | tee -a "$LOG_FILE"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}[⚠ WARN]${NC} $1" | tee -a "$LOG_FILE"
    ((WARNINGS++))
}

section() {
    echo "" | tee -a "$LOG_FILE"
    echo -e "${CYAN}$1${NC}" | tee -a "$LOG_FILE"
    echo "$(printf '=%.0s' {1..80})" | tee -a "$LOG_FILE"
}

# Create log directory
mkdir -p "$HOME/logs"

# ============================================================================
# Header
# ============================================================================

echo "================================================================================"
echo "              ULTRATHINK SYSTEM HEALTH CHECK - $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================================"
echo ""

# ============================================================================
# Phase 1: Directory Structure
# ============================================================================

section "Phase 1: Directory Structure"

# Check TestPrompt
if [ -d "$TESTPROMPT_DIR" ]; then
    pass "TestPrompt directory exists"
else
    fail "TestPrompt directory not found"
fi

if [ -d "$TESTPROMPT_DIR/tmp" ]; then
    pass "TestPrompt/tmp/ directory exists"
else
    fail "TestPrompt/tmp/ directory not found"
fi

# Check ClaudePrompt
if [ -d "$CLAUDEPROMPT_DIR" ]; then
    pass "ClaudePrompt directory exists"
else
    fail "ClaudePrompt directory not found"
fi

if [ -d "$CLAUDEPROMPT_DIR/tmp" ]; then
    pass "ClaudePrompt/tmp/ directory exists"
else
    fail "ClaudePrompt/tmp/ directory not found"
fi

# ============================================================================
# Phase 2: File Counts and Disk Usage
# ============================================================================

section "Phase 2: File Counts and Disk Usage"

# TestPrompt
if [ -d "$TESTPROMPT_DIR/tmp" ]; then
    TESTPROMPT_COUNT=$(find "$TESTPROMPT_DIR/tmp" -name "ultrathink_output_*.txt" -type f 2>/dev/null | wc -l)
    TESTPROMPT_SIZE=$(du -sh "$TESTPROMPT_DIR/tmp" 2>/dev/null | cut -f1)

    log "TestPrompt files: $TESTPROMPT_COUNT"
    log "TestPrompt disk usage: $TESTPROMPT_SIZE"

    if [ "$TESTPROMPT_COUNT" -ge 0 ]; then
        pass "TestPrompt file count: $TESTPROMPT_COUNT"
    fi

    # Check for recent activity (files modified in last 7 days)
    RECENT_COUNT=$(find "$TESTPROMPT_DIR/tmp" -name "ultrathink_output_*.txt" -type f -mtime -7 2>/dev/null | wc -l)
    if [ "$RECENT_COUNT" -gt 0 ]; then
        pass "TestPrompt recent activity: $RECENT_COUNT files in last 7 days"
    else
        warn "TestPrompt no recent activity (no files in last 7 days)"
    fi
fi

# ClaudePrompt
if [ -d "$CLAUDEPROMPT_DIR/tmp" ]; then
    CLAUDEPROMPT_COUNT=$(find "$CLAUDEPROMPT_DIR/tmp" -name "cppultrathink_output_*.txt" -type f 2>/dev/null | wc -l)
    CLAUDEPROMPT_SIZE=$(du -sh "$CLAUDEPROMPT_DIR/tmp" 2>/dev/null | cut -f1)

    log "ClaudePrompt files: $CLAUDEPROMPT_COUNT"
    log "ClaudePrompt disk usage: $CLAUDEPROMPT_SIZE"

    if [ "$CLAUDEPROMPT_COUNT" -ge 0 ]; then
        pass "ClaudePrompt file count: $CLAUDEPROMPT_COUNT"
    fi

    # Check for recent activity
    RECENT_COUNT=$(find "$CLAUDEPROMPT_DIR/tmp" -name "cppultrathink_output_*.txt" -type f -mtime -7 2>/dev/null | wc -l)
    if [ "$RECENT_COUNT" -gt 0 ]; then
        pass "ClaudePrompt recent activity: $RECENT_COUNT files in last 7 days"
    else
        warn "ClaudePrompt no recent activity (no files in last 7 days)"
    fi
fi

# ============================================================================
# Phase 3: Git Status
# ============================================================================

section "Phase 3: Git Synchronization"

cd /home/user01

# Check git status
if git rev-parse --git-dir > /dev/null 2>&1; then
    pass "Git repository detected"

    # Fetch latest changes
    git fetch origin > /dev/null 2>&1 || warn "Could not fetch from remote"

    # Compare local vs remote
    LOCAL=$(git rev-parse HEAD 2>/dev/null)
    REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)

    if [ "$LOCAL" = "$REMOTE" ]; then
        pass "Git in sync (local == remote)"
    else
        warn "Git out of sync (local != remote)"
        log "Local commit: ${LOCAL:0:7}"
        log "Remote commit: ${REMOTE:0:7}"
    fi

    # Check for uncommitted changes
    if git diff-index --quiet HEAD --; then
        pass "No uncommitted changes"
    else
        warn "Uncommitted changes detected"
        git status --short | head -5
    fi
else
    fail "Not a git repository"
fi

# ============================================================================
# Phase 4: Script Executability
# ============================================================================

section "Phase 4: Script Executability"

# Check TestPrompt scripts
if [ -x "$TESTPROMPT_DIR/ultrathinkc" ]; then
    pass "ultrathinkc is executable"
else
    fail "ultrathinkc is not executable or not found"
fi

if [ -f "$TESTPROMPT_DIR/get_output_path.py" ]; then
    if [ -x "$TESTPROMPT_DIR/get_output_path.py" ]; then
        pass "TestPrompt/get_output_path.py is executable"
    else
        warn "TestPrompt/get_output_path.py exists but not executable"
    fi
else
    fail "TestPrompt/get_output_path.py not found"
fi

if [ -f "$TESTPROMPT_DIR/answer_to_file.py" ]; then
    pass "TestPrompt/answer_to_file.py exists"
else
    fail "TestPrompt/answer_to_file.py not found"
fi

# Check ClaudePrompt scripts
if [ -x "$CLAUDEPROMPT_DIR/cpp" ]; then
    pass "cpp is executable"
else
    fail "cpp is not executable or not found"
fi

if [ -f "$CLAUDEPROMPT_DIR/get_output_path.py" ]; then
    if [ -x "$CLAUDEPROMPT_DIR/get_output_path.py" ]; then
        pass "ClaudePrompt/get_output_path.py is executable"
    else
        warn "ClaudePrompt/get_output_path.py exists but not executable"
    fi
else
    fail "ClaudePrompt/get_output_path.py not found"
fi

if [ -f "$CLAUDEPROMPT_DIR/answer_to_file.py" ]; then
    pass "ClaudePrompt/answer_to_file.py exists"
else
    fail "ClaudePrompt/answer_to_file.py not found"
fi

# ============================================================================
# Phase 5: Python Dependencies
# ============================================================================

section "Phase 5: Python Dependencies"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
log "Python version: $PYTHON_VERSION"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)"; then
    pass "Python version >= 3.7"
else
    fail "Python version < 3.7"
fi

# Test get_output_path.py scripts
if [ -f "$TESTPROMPT_DIR/get_output_path.py" ]; then
    if python3 "$TESTPROMPT_DIR/get_output_path.py" > /dev/null 2>&1; then
        pass "TestPrompt/get_output_path.py runs successfully"
    else
        fail "TestPrompt/get_output_path.py has errors"
    fi
fi

if [ -f "$CLAUDEPROMPT_DIR/get_output_path.py" ]; then
    if python3 "$CLAUDEPROMPT_DIR/get_output_path.py" > /dev/null 2>&1; then
        pass "ClaudePrompt/get_output_path.py runs successfully"
    else
        fail "ClaudePrompt/get_output_path.py has errors"
    fi
fi

# ============================================================================
# Phase 6: System Cleanup Status
# ============================================================================

section "Phase 6: System Cleanup Status"

# Check for very old files (90+ days)
OLD_TESTPROMPT=$(find "$TESTPROMPT_DIR/tmp" -name "ultrathink_output_*.txt" -type f -mtime +90 2>/dev/null | wc -l)
OLD_CLAUDEPROMPT=$(find "$CLAUDEPROMPT_DIR/tmp" -name "cppultrathink_output_*.txt" -type f -mtime +90 2>/dev/null | wc -l)

if [ "$OLD_TESTPROMPT" -eq 0 ]; then
    pass "TestPrompt: No files older than 90 days"
else
    warn "TestPrompt: $OLD_TESTPROMPT files older than 90 days (consider cleanup)"
fi

if [ "$OLD_CLAUDEPROMPT" -eq 0 ]; then
    pass "ClaudePrompt: No files older than 90 days"
else
    warn "ClaudePrompt: $OLD_CLAUDEPROMPT files older than 90 days (consider cleanup)"
fi

# Check /tmp/ for stray files
TMP_ULTRATHINK=$(find /tmp -maxdepth 1 -name "ultrathink*.txt" 2>/dev/null | wc -l)
TMP_CPP=$(find /tmp -maxdepth 1 -name "cpp*output*.txt" 2>/dev/null | wc -l)

if [ "$TMP_ULTRATHINK" -gt 0 ]; then
    warn "/tmp/ contains $TMP_ULTRATHINK ultrathink output files (should use persistent storage)"
else
    pass "/tmp/ has no stray ultrathink files"
fi

if [ "$TMP_CPP" -gt 0 ]; then
    warn "/tmp/ contains $TMP_CPP cpp output files (should use persistent storage)"
else
    pass "/tmp/ has no stray cpp files"
fi

# ============================================================================
# Phase 7: systemd-tmpfiles-clean Status
# ============================================================================

section "Phase 7: System Cleanup Service"

if systemctl list-timers systemd-tmpfiles-clean.timer > /dev/null 2>&1; then
    pass "systemd-tmpfiles-clean.timer is active"

    LAST_RUN=$(systemctl list-timers systemd-tmpfiles-clean.timer --no-pager | grep "systemd-tmpfiles-clean" | awk '{print $4, $5, $6}')
    log "Last run: $LAST_RUN"
else
    warn "Could not check systemd-tmpfiles-clean.timer status"
fi

# ============================================================================
# Summary
# ============================================================================

echo ""
echo "================================================================================"
echo "                        HEALTH CHECK SUMMARY"
echo "================================================================================"
echo ""

# Calculate score
TOTAL=$((PASSED + FAILED + WARNINGS))
SCORE=$((PASSED * 100 / TOTAL))

echo -e "${GREEN}✓ PASSED:${NC}   $PASSED"
echo -e "${RED}✗ FAILED:${NC}   $FAILED"
echo -e "${YELLOW}⚠ WARNINGS:${NC} $WARNINGS"
echo ""
echo -e "Score: ${CYAN}$SCORE%${NC} ($PASSED/$TOTAL checks passed)"
echo ""

if [ "$FAILED" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo -e "${GREEN}🎉 System Health: EXCELLENT${NC}"
    echo "All systems operational. No issues detected."
elif [ "$FAILED" -eq 0 ]; then
    echo -e "${YELLOW}✓ System Health: GOOD${NC}"
    echo "All critical checks passed. Minor warnings detected."
elif [ "$FAILED" -le 2 ]; then
    echo -e "${YELLOW}⚠ System Health: FAIR${NC}"
    echo "Some issues detected. Review failures above."
else
    echo -e "${RED}✗ System Health: POOR${NC}"
    echo "Multiple failures detected. Immediate attention required."
fi

echo ""
echo "================================================================================"
echo ""

# Log summary
log "Health check completed: $PASSED passed, $FAILED failed, $WARNINGS warnings"

# Exit with appropriate code
if [ "$FAILED" -eq 0 ]; then
    exit 0
else
    exit 1
fi
