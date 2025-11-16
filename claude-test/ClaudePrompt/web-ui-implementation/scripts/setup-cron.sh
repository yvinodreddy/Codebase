#!/bin/bash
################################################################################
# Setup Automated CVE Monitoring with Cron
#
# This script helps you set up weekly automated security scans
# Recommended schedule: Every Sunday at 2 AM
################################################################################

set -e

# Get the absolute path to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CVE_SCRIPT="$SCRIPT_DIR/cve-monitor.js"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}CVE Monitoring Cron Setup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if cron is available
if ! command -v crontab &> /dev/null; then
    echo -e "${YELLOW}⚠ Warning: crontab command not found${NC}"
    echo "This system may not support cron jobs."
    echo "You'll need to set up automated scanning manually."
    exit 1
fi

# Verify CVE script exists
if [ ! -f "$CVE_SCRIPT" ]; then
    echo -e "${YELLOW}⚠ Error: CVE monitoring script not found at:${NC}"
    echo "  $CVE_SCRIPT"
    exit 1
fi

# Create log directory
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

# Generate cron job entry
CRON_SCHEDULE="0 2 * * 0"  # Every Sunday at 2 AM
CRON_COMMAND="cd $PROJECT_DIR && node $CVE_SCRIPT >> $LOG_DIR/cve-monitor.log 2>&1"
CRON_ENTRY="$CRON_SCHEDULE $CRON_COMMAND"

echo "Proposed cron job:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$CRON_ENTRY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Schedule: Every Sunday at 2:00 AM"
echo "Log file: $LOG_DIR/cve-monitor.log"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "cve-monitor.js"; then
    echo -e "${YELLOW}⚠ Note: A CVE monitoring cron job already exists${NC}"
    echo ""
    echo "Current cron jobs:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    crontab -l 2>/dev/null | grep -A 1 -B 1 "cve-monitor"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    read -p "Replace existing cron job? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Remove existing CVE cron jobs
    crontab -l 2>/dev/null | grep -v "cve-monitor" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo -e "${GREEN}✓ Cron job installed successfully!${NC}"
echo ""
echo "Next steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Verify cron job: crontab -l"
echo "2. Test manually: node $CVE_SCRIPT"
echo "3. Check logs: tail -f $LOG_DIR/cve-monitor.log"
echo "4. Edit schedule: crontab -e"
echo ""
echo "Cron schedule format:"
echo "  0 2 * * 0  = Every Sunday at 2:00 AM"
echo "  0 2 * * 1  = Every Monday at 2:00 AM"
echo "  0 2 1 * *  = 1st of every month at 2:00 AM"
echo "  0 2 * * *  = Every day at 2:00 AM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}All set! CVE monitoring will run automatically.${NC}"
