#!/bin/bash
# phase5_trademark_symbol.sh
# CHANGE 5.3: Add ® symbol usage

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase5_trademark_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 5.3: Trademark Symbol (®) Addition" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find all files that should have ® symbol
FILES=$(find . -type f \
    \( -name "*.md" -o -name "*.html" -o -name "*.py" \) \
    ! -path "*/.git/*" \
    ! -path "*/rebranding_logs/*")

PROCESSED=0

for file in $FILES; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Add ® symbol after "Para Group" on first occurrence in each file
    # (avoiding duplicate ® symbols)
    sed -i '0,/Para Group[^®]/s//Para Group®/' "$file"

    ((PROCESSED++))
done

echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "✅ PHASE 5.3 COMPLETE" | tee -a "$LOG_FILE"