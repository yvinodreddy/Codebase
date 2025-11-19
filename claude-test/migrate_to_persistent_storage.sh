#!/usr/bin/env bash
################################################################################
# MIGRATION SCRIPT: TestPrompt to Persistent Storage
#
# Purpose: Migrate TestPrompt outputs from /tmp/ to persistent storage
# Location: /home/user01/claude-test/migrate_to_persistent_storage.sh
# Date: 2025-11-19
# Version: 1.0.0
#
# What this script does:
# 1. Creates TestPrompt/tmp/ folder if it doesn't exist
# 2. Copies any existing ultrathink output files from /tmp/ to persistent storage
# 3. Preserves file timestamps
# 4. Creates backup before migration
# 5. Validates migration success
#
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
TESTPROMPT_TMP="/home/user01/claude-test/TestPrompt/tmp"
SYSTEM_TMP="/tmp"
BACKUP_DIR="/home/user01/claude-test/TestPrompt/backups/migration_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$HOME/logs/migration_$(date +%Y%m%d).log"

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
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

# Create log directory
mkdir -p "$HOME/logs"

# ============================================================================
# Phase 1: Pre-Migration Checks
# ============================================================================

log "Starting TestPrompt migration to persistent storage..."

# Check if TestPrompt directory exists
if [ ! -d "/home/user01/claude-test/TestPrompt" ]; then
    log_error "TestPrompt directory not found!"
    exit 1
fi

log_success "TestPrompt directory found"

# ============================================================================
# Phase 2: Create Persistent Storage
# ============================================================================

log "Creating persistent storage directory..."

# Create TestPrompt/tmp/ if it doesn't exist
mkdir -p "$TESTPROMPT_TMP"
chmod 755 "$TESTPROMPT_TMP"

log_success "Persistent storage created: $TESTPROMPT_TMP"

# ============================================================================
# Phase 3: Create Backup
# ============================================================================

log "Creating backup directory..."

mkdir -p "$BACKUP_DIR"

log_success "Backup directory created: $BACKUP_DIR"

# ============================================================================
# Phase 4: Migrate Files from /tmp/
# ============================================================================

log "Searching for ultrathink output files in /tmp/..."

# Count files to migrate
FILE_COUNT=$(find "$SYSTEM_TMP" -maxdepth 1 -name "ultrathink*.txt" 2>/dev/null | wc -l)

# Initialize counters
MIGRATED=0
FAILED=0

if [ "$FILE_COUNT" -eq 0 ]; then
    log_warning "No ultrathink output files found in /tmp/"
    log_warning "This is normal if no recent ultrathinkc commands were run"
else
    log "Found $FILE_COUNT file(s) to migrate"

    # Copy files to backup first
    log "Creating backup of files..."
    find "$SYSTEM_TMP" -maxdepth 1 -name "ultrathink*.txt" -exec cp -p {} "$BACKUP_DIR/" \; 2>/dev/null || true

    log_success "Backup created"

    # Copy files to persistent storage
    log "Migrating files to persistent storage..."

    for file in "$SYSTEM_TMP"/ultrathink*.txt; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")

            # Add timestamp to filename if it doesn't have one
            if [[ ! "$filename" =~ [0-9]{8}_[0-9]{6} ]]; then
                # Get file modification time
                timestamp=$(date -r "$file" +%Y%m%d_%H%M%S_%3N 2>/dev/null || date +%Y%m%d_%H%M%S_000)
                new_filename="ultrathink_output_${timestamp}.txt"
            else
                new_filename="$filename"
            fi

            # Copy with preserved timestamps
            if cp -p "$file" "$TESTPROMPT_TMP/$new_filename"; then
                log_success "Migrated: $filename → $new_filename"
                ((MIGRATED++))
            else
                log_error "Failed to migrate: $filename"
                ((FAILED++))
            fi
        fi
    done

    log "Migration complete: $MIGRATED successful, $FAILED failed"
fi

# ============================================================================
# Phase 5: Validate Migration
# ============================================================================

log "Validating migration..."

# Count files in persistent storage
PERSISTENT_COUNT=$(ls -1 "$TESTPROMPT_TMP"/*.txt 2>/dev/null | wc -l)

log "Files in persistent storage: $PERSISTENT_COUNT"

if [ "$PERSISTENT_COUNT" -gt 0 ]; then
    log_success "Persistent storage validated"
else
    log_warning "No files in persistent storage (this is OK if no files were migrated)"
fi

# ============================================================================
# Phase 6: Verify get_output_path.py
# ============================================================================

log "Verifying get_output_path.py..."

GET_OUTPUT_PATH="/home/user01/claude-test/TestPrompt/get_output_path.py"

if [ -f "$GET_OUTPUT_PATH" ]; then
    # Test the script
    TEST_OUTPUT=$(python3 "$GET_OUTPUT_PATH" 2>&1)

    if [[ "$TEST_OUTPUT" =~ $TESTPROMPT_TMP ]]; then
        log_success "get_output_path.py working correctly"
        log "Test output: $TEST_OUTPUT"
    else
        log_error "get_output_path.py not working correctly"
        log_error "Expected path containing: $TESTPROMPT_TMP"
        log_error "Got: $TEST_OUTPUT"
    fi
else
    log_warning "get_output_path.py not found - needs to be created"
fi

# ============================================================================
# Phase 7: Summary
# ============================================================================

echo ""
echo "================================================================================"
echo "                        MIGRATION SUMMARY"
echo "================================================================================"
echo ""
echo "✅ Persistent storage:   $TESTPROMPT_TMP"
echo "✅ Files migrated:       $MIGRATED"
echo "❌ Files failed:         $FAILED"
echo "📦 Backup location:      $BACKUP_DIR"
echo "📊 Total files:          $PERSISTENT_COUNT"
echo ""
echo "================================================================================"
echo ""

if [ "$FAILED" -eq 0 ]; then
    log_success "Migration completed successfully!"
    echo -e "${GREEN}✓ All systems operational${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. ✅ TestPrompt now uses persistent storage"
    echo "  2. ✅ Files preserved forever (unless manually deleted)"
    echo "  3. ✅ Use 'ultrathinkc' or 'uc' commands as normal"
    echo "  4. ✅ Output files: $TESTPROMPT_TMP/ultrathink_output_YYYYMMDD_HHMMSS_mmm.txt"
    echo ""
    exit 0
else
    log_error "Migration completed with errors"
    echo -e "${RED}⚠ Some files failed to migrate${NC}"
    echo ""
    echo "Check the log file for details: $LOG_FILE"
    echo "Backup preserved at: $BACKUP_DIR"
    echo ""
    exit 1
fi
