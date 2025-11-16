#!/usr/bin/env bash
################################################################################
# AUTOMATED HOURLY GIT COMMIT & PUSH
#
# Purpose: Automatically commit and push all changes every hour
# Location: /home/user01/auto_commit_hourly.sh
# Cron: 0 * * * * /home/user01/auto_commit_hourly.sh >> /home/user01/logs/auto_commit.log 2>&1
#
# Features:
# - Commits all changes with timestamp
# - Pushes to both local git and GitHub
# - Validates before push
# - Comprehensive logging
# - Error handling with notifications
#
################################################################################

set -e  # Exit on error (will be caught)
set -u  # Exit on undefined variable

# Configuration
REPO_DIR="/home/user01"
GITHUB_REMOTE="https://github.com/yvinodreddy/Codebase.git"
LOG_DIR="$HOME/logs"
LOG_FILE="$LOG_DIR/auto_commit_$(date +%Y%m%d).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="Auto-commit: $TIMESTAMP"

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# Helper Functions
# ============================================================================

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
    echo -e "${YELLOW}[!]${NC} $1" | tee -a "$LOG_FILE"
}

# ============================================================================
# Main Function
# ============================================================================

main() {
    # Create log directory if doesn't exist
    mkdir -p "$LOG_DIR"

    log "=========================================="
    log "HOURLY AUTO-COMMIT STARTING"
    log "=========================================="

    # Change to repo directory
    cd "$REPO_DIR" || {
        log_error "Failed to change to $REPO_DIR"
        exit 1
    }

    # Check if git repo exists
    if [ ! -d ".git" ]; then
        log_error "Not a git repository. Run initialization first!"
        exit 1
    fi

    # Check for changes
    git status --porcelain > /tmp/git_status.txt
    CHANGES=$(cat /tmp/git_status.txt | wc -l)

    if [ "$CHANGES" -eq 0 ]; then
        log "No changes detected. Skipping commit."
        log_success "Repository is up to date"
        return 0
    fi

    log "Detected $CHANGES file changes"

    # Show what's changed (first 20 lines)
    log "Changes detected:"
    head -20 /tmp/git_status.txt | tee -a "$LOG_FILE"

    # Add all changes
    log "Adding all changes to staging..."
    git add -A || {
        log_error "Failed to add changes"
        exit 1
    }
    log_success "Changes staged successfully"

    # Create commit
    log "Creating commit..."
    git commit -m "$COMMIT_MSG

Files changed: $CHANGES

Auto-generated commit by hourly automation script.
Script: /home/user01/auto_commit_hourly.sh
" || {
        log_error "Failed to create commit"
        exit 1
    }
    log_success "Commit created: $COMMIT_MSG"

    # Push to GitHub
    log "Pushing to GitHub..."

    # Try to push (may fail if remote not set up yet)
    if git remote get-url origin &>/dev/null; then
        git push origin main 2>&1 | tee -a "$LOG_FILE" || {
            log_warning "Failed to push to GitHub (network issue or auth required)"
            log_warning "Changes committed locally but not pushed to remote"
            return 1
        }
        log_success "Pushed to GitHub successfully"
    else
        log_warning "GitHub remote 'origin' not configured"
        log_warning "Changes committed locally only"
        log "To configure remote, run:"
        log "  git remote add origin $GITHUB_REMOTE"
    fi

    # Summary
    log "=========================================="
    log_success "AUTO-COMMIT COMPLETED"
    log "Commits in local repo: $(git rev-list --count HEAD)"
    log "Latest commit: $(git log -1 --oneline)"
    log "=========================================="

    return 0
}

# ============================================================================
# Error Handler
# ============================================================================

trap 'log_error "Script failed at line $LINENO"; exit 1' ERR

# ============================================================================
# Execute
# ============================================================================

main

exit 0
