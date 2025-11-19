#!/usr/bin/env bash
################################################################################
# CLEANUP SCRIPT: Old ULTRATHINK Output Files
#
# Purpose: Clean up output files older than 90 days to prevent disk space issues
# Location: /home/user01/claude-test/cleanup_old_outputs.sh
# Schedule: Monthly (1st of every month at midnight)
# Date: 2025-11-19
# Version: 1.0.0
#
# What this script does:
# 1. Finds output files older than 90 days
# 2. Creates backup before deletion
# 3. Deletes old files
# 4. Logs all operations
# 5. Sends summary report
#
# Add to crontab:
#   0 0 1 * * /home/user01/claude-test/cleanup_old_outputs.sh
#
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
RETENTION_DAYS=90
TESTPROMPT_TMP="/home/user01/claude-test/TestPrompt/tmp"
CLAUDEPROMPT_TMP="/home/user01/claude-test/ClaudePrompt/tmp"
BACKUP_DIR="/home/user01/claude-test/backups/cleanup_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$HOME/logs/cleanup_$(date +%Y%m%d).log"
DRY_RUN=false

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --days)
            RETENTION_DAYS="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--dry-run] [--days N]"
            echo "  --dry-run   Show what would be deleted without actually deleting"
            echo "  --days N    Set retention period (default: 90 days)"
            exit 1
            ;;
    esac
done

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
# Header
# ============================================================================

echo "================================================================================"
echo "              ULTRATHINK OUTPUT CLEANUP - $(date '+%Y-%m-%d')"
echo "================================================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    log_warning "DRY RUN MODE - No files will be deleted"
fi

log "Retention period: $RETENTION_DAYS days"
log "Files older than $(date -d "$RETENTION_DAYS days ago" '+%Y-%m-%d') will be removed"

# ============================================================================
# Phase 1: TestPrompt/tmp/ Cleanup
# ============================================================================

log "Analyzing TestPrompt output files..."

if [ -d "$TESTPROMPT_TMP" ]; then
    # Count files to delete
    TESTPROMPT_OLD_COUNT=$(find "$TESTPROMPT_TMP" -name "ultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS 2>/dev/null | wc -l)
    TESTPROMPT_TOTAL=$(find "$TESTPROMPT_TMP" -name "ultrathink_output_*.txt" -type f 2>/dev/null | wc -l)

    log "TestPrompt total files: $TESTPROMPT_TOTAL"
    log "TestPrompt old files: $TESTPROMPT_OLD_COUNT"

    if [ "$TESTPROMPT_OLD_COUNT" -gt 0 ]; then
        if [ "$DRY_RUN" = true ]; then
            log_warning "Would delete $TESTPROMPT_OLD_COUNT TestPrompt file(s):"
            find "$TESTPROMPT_TMP" -name "ultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -ls 2>/dev/null | head -10
        else
            # Create backup
            mkdir -p "$BACKUP_DIR/testprompt"

            log "Creating backup of TestPrompt files..."
            find "$TESTPROMPT_TMP" -name "ultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -exec cp -p {} "$BACKUP_DIR/testprompt/" \; 2>/dev/null || true

            # Delete old files
            log "Deleting old TestPrompt files..."
            find "$TESTPROMPT_TMP" -name "ultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -delete

            log_success "Deleted $TESTPROMPT_OLD_COUNT TestPrompt file(s)"
        fi
    else
        log_success "No old TestPrompt files to clean"
    fi
else
    log_warning "TestPrompt/tmp/ directory not found"
fi

# ============================================================================
# Phase 2: ClaudePrompt/tmp/ Cleanup
# ============================================================================

log "Analyzing ClaudePrompt output files..."

if [ -d "$CLAUDEPROMPT_TMP" ]; then
    # Count files to delete (excluding special files like statusline_state.json, etc.)
    CLAUDEPROMPT_OLD_COUNT=$(find "$CLAUDEPROMPT_TMP" -name "cppultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS 2>/dev/null | wc -l)
    CLAUDEPROMPT_TOTAL=$(find "$CLAUDEPROMPT_TMP" -name "cppultrathink_output_*.txt" -type f 2>/dev/null | wc -l)

    log "ClaudePrompt total files: $CLAUDEPROMPT_TOTAL"
    log "ClaudePrompt old files: $CLAUDEPROMPT_OLD_COUNT"

    if [ "$CLAUDEPROMPT_OLD_COUNT" -gt 0 ]; then
        if [ "$DRY_RUN" = true ]; then
            log_warning "Would delete $CLAUDEPROMPT_OLD_COUNT ClaudePrompt file(s):"
            find "$CLAUDEPROMPT_TMP" -name "cppultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -ls 2>/dev/null | head -10
        else
            # Create backup
            mkdir -p "$BACKUP_DIR/claudeprompt"

            log "Creating backup of ClaudePrompt files..."
            find "$CLAUDEPROMPT_TMP" -name "cppultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -exec cp -p {} "$BACKUP_DIR/claudeprompt/" \; 2>/dev/null || true

            # Delete old files
            log "Deleting old ClaudePrompt files..."
            find "$CLAUDEPROMPT_TMP" -name "cppultrathink_output_*.txt" -type f -mtime +$RETENTION_DAYS -delete

            log_success "Deleted $CLAUDEPROMPT_OLD_COUNT ClaudePrompt file(s)"
        fi
    else
        log_success "No old ClaudePrompt files to clean"
    fi
else
    log_warning "ClaudePrompt/tmp/ directory not found"
fi

# ============================================================================
# Phase 3: Calculate Space Saved
# ============================================================================

if [ "$DRY_RUN" = false ] && [ -d "$BACKUP_DIR" ]; then
    SPACE_SAVED=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
    log "Space reclaimed: $SPACE_SAVED"
    log "Backup location: $BACKUP_DIR"
fi

# ============================================================================
# Summary
# ============================================================================

echo ""
echo "================================================================================"
echo "                        CLEANUP SUMMARY"
echo "================================================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "🔍 DRY RUN MODE - No files were deleted"
    echo ""
    echo "TestPrompt files to delete:   $TESTPROMPT_OLD_COUNT"
    echo "ClaudePrompt files to delete: $CLAUDEPROMPT_OLD_COUNT"
    echo "Total files to delete:        $((TESTPROMPT_OLD_COUNT + CLAUDEPROMPT_OLD_COUNT))"
    echo ""
    echo "Run without --dry-run to actually delete these files"
else
    echo "✅ Retention period:          $RETENTION_DAYS days"
    echo "✅ TestPrompt files deleted:  ${TESTPROMPT_OLD_COUNT:-0}"
    echo "✅ ClaudePrompt files deleted: ${CLAUDEPROMPT_OLD_COUNT:-0}"
    echo "✅ Total files deleted:       $((${TESTPROMPT_OLD_COUNT:-0} + ${CLAUDEPROMPT_OLD_COUNT:-0}))"
    echo "📦 Backup location:           $BACKUP_DIR"
    echo "💾 Space reclaimed:           ${SPACE_SAVED:-unknown}"
fi

echo ""
echo "================================================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    log_warning "Dry run completed - no files were deleted"
    exit 0
else
    log_success "Cleanup completed successfully!"
    exit 0
fi
