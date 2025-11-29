#!/bin/bash
# phase4_api_docs.sh
# CHANGE 4.2: Update API documentation

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase4_api_docs_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 4.2: API Documentation Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find API documentation files
API_DOCS=$(find . -type f \
    \( -name "*api*.md" -o -name "*API*.md" -o -path "*/docs/*" \) \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*")

for file in $API_DOCS; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update API references
    sed -i 's/claudeprompt-api/paragroup-api/g' "$file"
    sed -i 's/ClaudePrompt API/Para Group AI Orchestrator® API/g' "$file"

    # Update endpoint examples
    sed -i 's|/api/v1/claudeprompt|/api/v1/paragroup|g' "$file"

    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

echo "✅ PHASE 4.2 COMPLETE" | tee -a "$LOG_FILE"