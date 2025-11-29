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

# Find ONLY files that contain "ClaudePrompt" (much faster!)
echo "Finding files containing 'ClaudePrompt'..." | tee -a "$LOG_FILE"

# Use grep to find files containing the string (much faster than processing all files)
FILES=$(grep -rl "ClaudePrompt" /home/user01/claude-test/ClaudePrompt \
    --include="*.py" --include="*.md" --include="*.txt" --include="*.json" --include="*.yml" --include="*.yaml" \
    --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ --exclude-dir=venv --exclude-dir=tmp --exclude-dir=rebranding_logs \
    2>/dev/null || true)

FILE_COUNT=$(echo "$FILES" | grep -c . || echo "0")
echo "Found $FILE_COUNT files containing 'ClaudePrompt'" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "✅ No files to process (already rebranded or no matches)" | tee -a "$LOG_FILE"
    exit 0
fi

# Process each file with progress reporting
PROCESSED=0
ERRORS=0
PROGRESS=0

for file in $FILES; do
    ((PROGRESS++))
    echo "[$PROGRESS/$FILE_COUNT] Processing: $file" | tee -a "$LOG_FILE"

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