#!/bin/bash
# phase1_product_name_rebrand.sh
# CHANGE 1.1: Product name rebranding

set -e  # Exit on error

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase1_product_name_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 1.1: Product Name Rebranding" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "From: ClaudePrompt" | tee -a "$LOG_FILE"
echo "To: Para Group AI Orchestrator®" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Function: Replace product name in files
replace_product_name() {
    local file="$1"
    local backup="${file}.prebrand.bak"

    # Create backup
    cp "$file" "$backup"

    # Replace variations
    sed -i 's/ClaudePrompt/Para Group AI Orchestrator®/g' "$file"
    sed -i 's/claudeprompt/para-group-ai-orchestrator/g' "$file"
    sed -i 's/CLAUDEPROMPT/PARA_GROUP_AI_ORCHESTRATOR/g' "$file"

    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
}

# Find all relevant files (exclude .git, node_modules, __pycache__)
echo "Finding files to update..." | tee -a "$LOG_FILE"
FILES=$(find /home/user01/claude-test/ClaudePrompt \
    -type f \
    \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" \) \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/venv/*" \
    ! -path "*/tmp/*" \
    ! -path "*/rebranding_logs/*")

FILE_COUNT=$(echo "$FILES" | wc -l)
echo "Found $FILE_COUNT files to process" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Process each file
PROCESSED=0
ERRORS=0

for file in $FILES; do
    if replace_product_name "$file"; then
        ((PROCESSED++))
    else
        ((ERRORS++))
        echo "❌ Error processing: $file" | tee -a "$LOG_FILE"
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 1.1 SUMMARY" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "Files processed: $PROCESSED" | tee -a "$LOG_FILE"
echo "Errors: $ERRORS" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ $ERRORS -eq 0 ]; then
    echo "✅ PHASE 1.1 COMPLETE - ZERO ERRORS" | tee -a "$LOG_FILE"
    exit 0
else
    echo "⚠️  PHASE 1.1 COMPLETE WITH ERRORS - Review log file" | tee -a "$LOG_FILE"
    exit 1
fi