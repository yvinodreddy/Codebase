#!/bin/bash
# phase4_code_comments.sh
# CHANGE 4.3: Update code comments

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase4_comments_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 4.3: Code Comments Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Python files
PYTHON_FILES=$(find . -type f -name "*.py" \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*")

PROCESSED=0

for file in $PYTHON_FILES; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update comments
    sed -i 's/# ClaudePrompt/# Para Group AI Orchestrator®/g' "$file"
    sed -i 's/# claudeprompt/# paragroup/g' "$file"

    # Update docstrings
    sed -i 's/"""ClaudePrompt/"""Para Group AI Orchestrator®/g' "$file"
    sed -i "s/'''ClaudePrompt/'''Para Group AI Orchestrator®/g" "$file"

    ((PROCESSED++))
done

echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "✅ PHASE 4.3 COMPLETE" | tee -a "$LOG_FILE"