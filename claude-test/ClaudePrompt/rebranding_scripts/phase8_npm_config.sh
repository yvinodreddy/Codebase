#!/bin/bash
# phase8_npm_config.sh
# CHANGE 8.3: Update NPM configuration

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase8_npm_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 8.3: NPM Configuration Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Update .npmrc if exists
cd /home/user01/claude-test/ParaGroupAI

if [ -f ".npmrc" ]; then
    cp .npmrc .npmrc.prebrand.bak

    # Update registry/scope if needed
    sed -i 's/@claudeprompt/@paragroup/g' .npmrc

    echo "✅ Updated .npmrc" | tee -a "$LOG_FILE"
fi

echo "✅ PHASE 8.3 COMPLETE" | tee -a "$LOG_FILE"