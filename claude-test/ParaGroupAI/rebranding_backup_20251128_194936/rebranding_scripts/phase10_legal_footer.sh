#!/bin/bash
# phase10_legal_footer.sh
# CHANGE 10.3: Add legal footer to documentation

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase10_legal_footer_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 10.3: Legal Footer Addition" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

LEGAL_FOOTER='

---

**Legal Notice:**
Para Group® is a registered trademark of Para Group LLC (USPTO Reg. #7113228, #7113231).
Copyright © 2025 Para Group LLC. All rights reserved.
'

# Find all markdown files
MD_FILES=$(find . -type f -name "*.md" \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/rebranding_logs/*")

for file in $MD_FILES; do
    # Check if footer already exists
    if ! grep -q "Para Group® is a registered trademark" "$file"; then
        # Add footer
        echo "$LEGAL_FOOTER" >> "$file"
        echo "✅ Added legal footer: $file" | tee -a "$LOG_FILE"
    fi
done

echo "✅ PHASE 10.3 COMPLETE" | tee -a "$LOG_FILE"