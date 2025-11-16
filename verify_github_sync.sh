#!/usr/bin/env bash
################################################################################
# GitHub Sync Verification Script
# Purpose: Verify local git and GitHub are synchronized
# Author: Claude Code (Production-Ready Automation)
# Date: 2025-11-15
# Version: 1.0
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_DIR="/home/user01"
LOG_FILE="$HOME/logs/github_sync_verification.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Logging function
log() {
    echo -e "${BLUE}[$TIMESTAMP]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1" | tee -a "$LOG_FILE"
}

# Ensure we're in the repo directory
cd "$REPO_DIR" || {
    log_error "Failed to change to repository directory: $REPO_DIR"
    exit 1
}

echo ""
log "=========================================="
log "GITHUB SYNC VERIFICATION STARTING"
log "=========================================="

# Step 1: Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not a git repository: $REPO_DIR"
    exit 1
fi
log_success "Git repository detected"

# Step 2: Check remote configuration
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    log_error "No remote 'origin' configured"
    exit 1
fi
log_success "Remote URL: $REMOTE_URL"

# Step 3: Fetch latest from remote
log "Fetching from GitHub..."
if git fetch origin 2>&1 | tee -a "$LOG_FILE"; then
    log_success "Fetch successful"
else
    log_error "Fetch failed - Check network or GitHub authentication"
    exit 1
fi

# Step 4: Get local and remote commit hashes
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "")

if [ -z "$REMOTE_COMMIT" ]; then
    log_error "Cannot find remote branch (tried origin/main and origin/master)"
    exit 1
fi

log "Local commit:  $LOCAL_COMMIT"
log "Remote commit: $REMOTE_COMMIT"

# Step 5: Compare commits
if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    log_success "✅ SYNCHRONIZED - Local and GitHub are identical"
    SYNC_STATUS="SYNCHRONIZED"
    EXIT_CODE=0
elif git merge-base --is-ancestor "$REMOTE_COMMIT" "$LOCAL_COMMIT" 2>/dev/null; then
    log_warning "⚠️ LOCAL AHEAD - You have unpushed commits"
    UNPUSHED_COUNT=$(git rev-list --count origin/main..HEAD)
    log_warning "Unpushed commits: $UNPUSHED_COUNT"
    git log origin/main..HEAD --oneline | while read line; do
        log_warning "  - $line"
    done
    SYNC_STATUS="LOCAL_AHEAD"
    EXIT_CODE=2
elif git merge-base --is-ancestor "$LOCAL_COMMIT" "$REMOTE_COMMIT" 2>/dev/null; then
    log_error "❌ REMOTE AHEAD - GitHub has commits you don't have"
    log_error "Run: git pull origin main"
    SYNC_STATUS="REMOTE_AHEAD"
    EXIT_CODE=3
else
    log_error "❌ DIVERGED - Local and remote have different commits"
    log_error "Manual intervention required"
    SYNC_STATUS="DIVERGED"
    EXIT_CODE=4
fi

# Step 6: Check for uncommitted changes
UNCOMMITTED=$(git status --porcelain | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    log_warning "Uncommitted changes: $UNCOMMITTED files"
    git status --porcelain | head -10 | while read line; do
        log_warning "  $line"
    done
    if [ "$UNCOMMITTED" -gt 10 ]; then
        log_warning "  ... and $((UNCOMMITTED - 10)) more"
    fi
fi

# Step 7: Summary
echo ""
log "=========================================="
log "VERIFICATION SUMMARY"
log "=========================================="
log "Repository: $REPO_DIR"
log "Remote: $REMOTE_URL"
log "Status: $SYNC_STATUS"
log "Uncommitted changes: $UNCOMMITTED files"
log "=========================================="

# Step 8: Return appropriate exit code
exit $EXIT_CODE
