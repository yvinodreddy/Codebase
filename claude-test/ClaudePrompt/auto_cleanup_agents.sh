#!/bin/bash
# auto_cleanup_agents.sh - Automatic agent cleanup
#
# PRODUCTION-READY AUTO-CLEANUP (2025-11-21)
# ==========================================
#
# PURPOSE:
# - Automatically clean stuck/completed agents every hour
# - Prevent agent count from growing indefinitely
# - Run silently in background
#
# SETUP:
#   Add to crontab: */15 * * * * /home/user01/claude-test/ClaudePrompt/auto_cleanup_agents.sh
#   Or run manually: ./auto_cleanup_agents.sh
#
# FEATURES:
# - Clears completed agents older than 5 minutes
# - Clears stuck running agents older than 1 hour
# - Logs cleanup activity
# - Silent operation (no output unless error)

SCRIPT_DIR="/home/user01/claude-test/ClaudePrompt"
LOG_FILE="$SCRIPT_DIR/logs/agent_cleanup.log"

# Create log directory
mkdir -p "$SCRIPT_DIR/logs"

# Log timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Running agent cleanup" >> "$LOG_FILE"

# Run cleanup
python3 "$SCRIPT_DIR/fix_stuck_agents.py" >> "$LOG_FILE" 2>&1

# Check result
if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleanup successful" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleanup failed" >> "$LOG_FILE"
fi

# Keep log file under 1MB (rotate if needed)
if [ -f "$LOG_FILE" ]; then
    SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt 1048576 ]; then
        mv "$LOG_FILE" "$LOG_FILE.old"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Log rotated" > "$LOG_FILE"
    fi
fi
