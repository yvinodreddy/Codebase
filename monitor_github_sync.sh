#!/usr/bin/env bash
################################################################################
# GitHub Sync Monitoring & Auto-Recovery Script
# Purpose: Monitor sync status and automatically recover from failures
# Author: Claude Code (Production-Ready Automation)
# Date: 2025-11-15
# Version: 1.0
################################################################################

set -euo pipefail

# Configuration
REPO_DIR="/home/user01"
LOG_FILE="$HOME/logs/github_sync_monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
MAX_RETRY_ATTEMPTS=3
RETRY_DELAY=60  # seconds

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Ensure log directory exists
mkdir -p "$HOME/logs"

log "=========================================="
log "GITHUB SYNC MONITORING STARTING"
log "=========================================="

cd "$REPO_DIR" || exit 1

# Run verification script
if /home/user01/verify_github_sync.sh; then
    log_success "Sync verification PASSED"
    exit 0
fi

VERIFY_EXIT_CODE=$?

case $VERIFY_EXIT_CODE in
    2)
        log_warning "LOCAL AHEAD - Attempting auto-push"

        # Attempt to push with retries
        for attempt in $(seq 1 $MAX_RETRY_ATTEMPTS); do
            log "Push attempt $attempt of $MAX_RETRY_ATTEMPTS..."

            if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
                log_success "✅ AUTO-RECOVERY SUCCESSFUL - Push completed"

                # Verify sync after push
                if /home/user01/verify_github_sync.sh > /dev/null 2>&1; then
                    log_success "✅ VERIFICATION PASSED - Sync confirmed"
                    exit 0
                else
                    log_warning "Push succeeded but verification failed - manual check recommended"
                    exit 1
                fi
            else
                log_error "Push attempt $attempt failed"

                if [ $attempt -lt $MAX_RETRY_ATTEMPTS ]; then
                    log "Retrying in ${RETRY_DELAY}s..."
                    sleep $RETRY_DELAY
                fi
            fi
        done

        log_error "❌ AUTO-RECOVERY FAILED - All push attempts failed"
        log_error "Manual intervention required"
        exit 1
        ;;

    3)
        log_error "❌ REMOTE AHEAD - Cannot auto-recover"
        log_error "Manual action required: git pull origin main"
        exit 1
        ;;

    4)
        log_error "❌ DIVERGED - Cannot auto-recover"
        log_error "Manual action required: git rebase or git merge"
        exit 1
        ;;

    *)
        log_error "❌ UNKNOWN ERROR - Exit code: $VERIFY_EXIT_CODE"
        exit 1
        ;;
esac
