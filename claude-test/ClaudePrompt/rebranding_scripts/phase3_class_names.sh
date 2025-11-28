#!/bin/bash
# phase3_class_names.sh
# CHANGE 3.3: Update class names and constants

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase3_classes_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 3.3: Class Names & Constants Updates" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Python files only for class names
PYTHON_FILES=$(find . -type f -name "*.py" \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/rebranding_logs/*")

PROCESSED=0

for file in $PYTHON_FILES; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update class names (CamelCase)
    sed -i 's/class ClaudePrompt/class ParaGroupAIOrchestrator/g' "$file"
    sed -i 's/ClaudePromptConfig/ParaGroupAIConfig/g' "$file"
    sed -i 's/ClaudePromptManager/ParaGroupAIManager/g' "$file"

    # Update constants (UPPER_CASE)
    sed -i 's/CLAUDEPROMPT_/PARAGROUP_AI_/g' "$file"
    sed -i 's/CPP_/PRSG_/g' "$file"

    ((PROCESSED++))
done

echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "✅ PHASE 3.3 COMPLETE" | tee -a "$LOG_FILE"