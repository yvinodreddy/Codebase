#!/bin/bash
# phase10_trademark_notices.sh
# CHANGE 10.1: Add trademark notices

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase10_trademark_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 10.1: Trademark Notices Addition" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Python files - add header comment
PYTHON_FILES=$(find . -type f -name "*.py" \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/rebranding_logs/*")

TRADEMARK_HEADER_PY='"""
Para Group AI Orchestrator®

Para Group® is a registered trademark of Para Group LLC
USPTO Registration Numbers: 7113228, 7113231

Copyright © 2025 Para Group LLC. All rights reserved.
"""

'

for file in $PYTHON_FILES; do
    # Check if file already has trademark notice
    if ! grep -q "Para Group® is a registered trademark" "$file"; then
        # Add header at top of file (after shebang if exists)
        if head -n 1 "$file" | grep -q "^#!"; then
            # File has shebang - insert after it
            sed -i "1 a\\
$TRADEMARK_HEADER_PY" "$file"
        else
            # No shebang - insert at top
            sed -i "1 i\\
$TRADEMARK_HEADER_PY" "$file"
        fi
        echo "✅ Added trademark notice: $file" | tee -a "$LOG_FILE"
    fi
done

echo "✅ PHASE 10.1 COMPLETE" | tee -a "$LOG_FILE"