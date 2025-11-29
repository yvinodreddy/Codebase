#!/bin/bash
# rollback_all_changes.sh
# Emergency rollback script - reverts ALL changes

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/rollback_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "EMERGENCY ROLLBACK - Reverting ALL Changes" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "⚠️  WARNING: This will revert all rebranding changes" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Confirmation
read -p "Are you sure you want to rollback? (type 'YES' to confirm): " CONFIRM
if [ "$CONFIRM" != "YES" ]; then
    echo "❌ Rollback cancelled" | tee -a "$LOG_FILE"
    exit 1
fi

echo "Starting rollback..." | tee -a "$LOG_FILE"

# Step 1: Restore from backup branch
cd /home/user01/claude-test
BACKUP_BRANCH=$(git branch | grep rebranding-backup | tail -n 1 | tr -d ' ')

if [ -n "$BACKUP_BRANCH" ]; then
    echo "Restoring from backup branch: $BACKUP_BRANCH" | tee -a "$LOG_FILE"
    git checkout "$BACKUP_BRANCH"
    echo "✅ Restored from Git backup" | tee -a "$LOG_FILE"
else
    echo "❌ No backup branch found" | tee -a "$LOG_FILE"

    # Alternative: Restore from tar.gz backup
    LATEST_BACKUP=$(ls -t ClaudePrompt_backup_*.tar.gz 2>/dev/null | head -n 1)
    if [ -n "$LATEST_BACKUP" ]; then
        echo "Restoring from tar backup: $LATEST_BACKUP" | tee -a "$LOG_FILE"
        tar -xzf "$LATEST_BACKUP"
        echo "✅ Restored from tar backup" | tee -a "$LOG_FILE"
    else
        echo "❌ No backups found - cannot rollback" | tee -a "$LOG_FILE"
        exit 1
    fi
fi

# Step 2: Restore .bashrc
if [ -f ~/.bashrc.prebrand.bak ]; then
    cp ~/.bashrc.prebrand.bak ~/.bashrc
    echo "✅ Restored ~/.bashrc" | tee -a "$LOG_FILE"
fi

# Step 3: Database rollback (if migrations were run)
echo "⚠️  Manual database rollback may be required" | tee -a "$LOG_FILE"
echo "   Review: migrations/rollback_*.sql" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "ROLLBACK COMPLETE" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "✅ System restored to pre-rebranding state" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"