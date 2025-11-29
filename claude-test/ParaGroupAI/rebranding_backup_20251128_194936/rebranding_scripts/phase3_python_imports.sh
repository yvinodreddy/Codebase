#!/bin/bash
# phase3_python_imports.sh
# CHANGE 3.1: Update Python import statements

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase3_imports_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 3.1: Python Import Updates" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find all Python files
PYTHON_FILES=$(find . -type f -name "*.py" \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/venv/*" \
    ! -path "*/rebranding_logs/*")

PROCESSED=0

for file in $PYTHON_FILES; do
    # Backup original file
    cp "$file" "${file}.prebrand.bak"

    # Update import statements
    sed -i 's/from claudeprompt/from paragroup/g' "$file"
    sed -i 's/import claudeprompt/import paragroup/g' "$file"
    sed -i 's/from ClaudePrompt/from ParaGroupAI/g' "$file"
    sed -i 's/import ClaudePrompt/import ParaGroupAI/g' "$file"

    ((PROCESSED++))
    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 3.1 SUMMARY" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "✅ PHASE 3.1 COMPLETE" | tee -a "$LOG_FILE"