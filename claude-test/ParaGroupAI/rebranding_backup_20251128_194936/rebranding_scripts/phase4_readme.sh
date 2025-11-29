#!/bin/bash
# phase4_readme.sh
# CHANGE 4.1: Update README.md

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase4_readme_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 4.1: README.md Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find all README files
README_FILES=$(find . -type f -name "README*" \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*")

for file in $README_FILES; do
    echo "Updating: $file" | tee -a "$LOG_FILE"

    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update content
    sed -i 's/# ClaudePrompt/# Para Group AI Orchestrator®/g' "$file"
    sed -i 's/ClaudePrompt/Para Group AI Orchestrator®/g' "$file"
    sed -i 's/cpp /prsg /g' "$file"
    sed -i 's/`cpp`/`prsg`/g' "$file"

    # Add trademark notice at top if not present
    if ! grep -q "Para Group®" "$file"; then
        sed -i '1s/^/# Para Group AI Orchestrator®\n\n**Para Group®** is a registered trademark of Para Group LLC (USPTO Registration #7113228, #7113231)\n\n---\n\n/' "$file"
    fi

    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

echo "✅ PHASE 4.1 COMPLETE" | tee -a "$LOG_FILE"