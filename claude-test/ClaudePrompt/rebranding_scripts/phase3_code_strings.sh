#!/bin/bash
# phase3_code_strings.sh
# CHANGE 3.2: Update string references

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase3_strings_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 3.2: Code String Updates" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find all source code files
CODE_FILES=$(find . -type f \
    \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" \) \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/rebranding_logs/*")

PROCESSED=0

for file in $CODE_FILES; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update strings (preserve case sensitivity)
    sed -i 's/"ClaudePrompt"/"Para Group AI Orchestrator®"/g' "$file"
    sed -i "s/'ClaudePrompt'/'Para Group AI Orchestrator®'/g" "$file"
    sed -i 's/"claudeprompt"/"para-group-ai-orchestrator"/g' "$file"
    sed -i "s/'claudeprompt'/'para-group-ai-orchestrator'/g" "$file"

    # Update CLI command references
    sed -i 's/"cpp"/"prsg"/g' "$file"
    sed -i "s/'cpp'/'prsg'/g" "$file"

    ((PROCESSED++))
done

echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "✅ PHASE 3.2 COMPLETE" | tee -a "$LOG_FILE"