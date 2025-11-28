#!/bin/bash
# phase8_package_json.sh
# CHANGE 8.1: Update package.json

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase8_package_json_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 8.1: package.json Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

if [ -f "package.json" ]; then
    # Backup
    cp package.json package.json.prebrand.bak

    # Update package.json fields
    sed -i 's/"name": "claudeprompt"/"name": "para-group-ai-orchestrator"/g' package.json
    sed -i 's/"description": ".*ClaudePrompt.*"/"description": "Para Group AI Orchestrator® - Enterprise AI orchestration platform"/g' package.json
    sed -i 's/"homepage": ".*"/"homepage": "https://ai.paragroup.com"/g' package.json

    echo "✅ Updated package.json" | tee -a "$LOG_FILE"
else
    echo "⏭️  package.json not found - skipping" | tee -a "$LOG_FILE"
fi

echo "✅ PHASE 8.1 COMPLETE" | tee -a "$LOG_FILE"