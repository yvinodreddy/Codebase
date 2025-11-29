#!/bin/bash
# Track Execution Script Template
# This script runs a specific track and updates state in real-time
#
# ZERO BREAKING CHANGES:
# - New file in new directory (tracks/)
# - Does not modify existing code
# - Optional feature for parallel execution

set -e  # Exit on error

TRACK_ID=$1
TRACK_NAME=$2
LOG_FILE="logs/track${TRACK_ID}.log"
STATE_DB="realtime-tracking/track_state.db"

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging function with database update
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Log to file
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"

    # Insert into database (escape single quotes)
    local escaped_msg=$(echo "$message" | sed "s/'/''/g")
    sqlite3 "$STATE_DB" "INSERT INTO log_entries (track_id, timestamp, level, message) VALUES ($TRACK_ID, '$timestamp', '$level', '$escaped_msg');" 2>/dev/null || true
}

# Update track progress
update_progress() {
    local progress=$1
    local current_task=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Escape single quotes in task description
    local escaped_task=$(echo "$current_task" | sed "s/'/''/g")

    sqlite3 "$STATE_DB" "UPDATE tracks SET progress=$progress, current_task='$escaped_task', last_update='$timestamp' WHERE id=$TRACK_ID;" 2>/dev/null || true

    log "INFO" "Progress: $progress% - $current_task"
}

# Update track status
update_status() {
    local status=$1
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    sqlite3 "$STATE_DB" "UPDATE tracks SET status='$status', last_update='$timestamp' WHERE id=$TRACK_ID;" 2>/dev/null || true

    if [ "$status" = "RUNNING" ]; then
        sqlite3 "$STATE_DB" "UPDATE tracks SET started_at='$timestamp' WHERE id=$TRACK_ID;" 2>/dev/null || true
    elif [ "$status" = "COMPLETED" ]; then
        sqlite3 "$STATE_DB" "UPDATE tracks SET completed_at='$timestamp' WHERE id=$TRACK_ID;" 2>/dev/null || true
    fi

    log "INFO" "Status changed to: $status"
}

# Error handling
handle_error() {
    local error_message=$1
    log "ERROR" "$error_message"
    update_status "FAILED"

    # Escape single quotes in error message
    local escaped_error=$(echo "$error_message" | sed "s/'/''/g")
    sqlite3 "$STATE_DB" "UPDATE tracks SET error_message='$escaped_error' WHERE id=$TRACK_ID;" 2>/dev/null || true

    exit 1
}

# Trap errors
trap 'handle_error "Script failed at line $LINENO"' ERR

# Main execution placeholder
# This will be customized per track
main() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}Track $TRACK_ID: $TRACK_NAME${NC}"
    echo -e "${BLUE}================================${NC}"

    log "INFO" "Starting Track $TRACK_ID: $TRACK_NAME"
    update_status "RUNNING"
    update_progress 0 "Initializing..."

    # Placeholder tasks - customize per track
    sleep 2
    update_progress 20 "Setting up environment..."
    sleep 3
    update_progress 40 "Running core tasks..."
    sleep 5
    update_progress 60 "Running validation..."
    sleep 3
    update_progress 80 "Finalizing..."
    sleep 2
    update_progress 100 "Completed!"

    update_status "COMPLETED"

    echo -e "${GREEN}✅ Track $TRACK_ID completed successfully${NC}"
    log "INFO" "Track $TRACK_ID completed successfully"
}

# Run main function
main
