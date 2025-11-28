#!/bin/bash
# phase11_presentations.sh
# CHANGE 11.3: Update presentation templates

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase11_presentations_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 11.3: Presentation Templates Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Find presentation files
PRES_FILES=$(find /home/user01/claude-test/ParaGroupAI \
    -type f \
    \( -name "*.pptx" -o -name "*.odp" -o -name "*.key" \) \
    ! -path "*/.git/*")

if [ -z "$PRES_FILES" ]; then
    echo "⏭️  No presentation files found" | tee -a "$LOG_FILE"
else
    echo "⚠️  Found presentation files - manual update required:" | tee -a "$LOG_FILE"
    echo "$PRES_FILES" | tee -a "$LOG_FILE"
fi

echo "✅ PHASE 11.3 COMPLETE" | tee -a "$LOG_FILE"