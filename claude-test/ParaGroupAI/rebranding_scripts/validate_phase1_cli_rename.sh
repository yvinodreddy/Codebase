#!/bin/bash
# validate_phase1_cli_rename.sh
# Validates CHANGE 1.2 implementation

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="rebranding_logs/validate_phase1_cli_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "VALIDATING PHASE 1.2: CLI Command Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ClaudePrompt

# Check 1: prsg file exists
if [ -f "prsg" ]; then
    echo "✅ prsg file exists" | tee -a "$LOG_FILE"
else
    echo "❌ prsg file NOT found" | tee -a "$LOG_FILE"
    exit 1
fi

# Check 2: cpp symlink points to prsg (backward compatibility)
if [ -L "cpp" ]; then
    TARGET=$(readlink cpp)
    if [ "$TARGET" == "prsg" ]; then
        echo "✅ cpp symlink points to prsg (backward compatible)" | tee -a "$LOG_FILE"
    else
        echo "❌ cpp symlink points to wrong target: $TARGET" | tee -a "$LOG_FILE"
        exit 1
    fi
else
    echo "⚠️  cpp is not a symlink (might be original file)" | tee -a "$LOG_FILE"
fi

# Check 3: Bash alias exists
if grep -q "alias prsg=" ~/.bashrc; then
    echo "✅ Bash alias 'prsg' exists in ~/.bashrc" | tee -a "$LOG_FILE"
else
    echo "❌ Bash alias 'prsg' NOT found in ~/.bashrc" | tee -a "$LOG_FILE"
    exit 1
fi

# Check 4: Documentation references updated
DOC_CPP_COUNT=$(grep -r '`cpp ' /home/user01/claude-test/ClaudePrompt \
    --include="*.md" 2>/dev/null | wc -l)
DOC_PRSG_COUNT=$(grep -r '`prsg ' /home/user01/claude-test/ClaudePrompt \
    --include="*.md" 2>/dev/null | wc -l)
echo "Documentation references: cpp=$DOC_CPP_COUNT, prsg=$DOC_PRSG_COUNT" | tee -a "$LOG_FILE"

if [ $DOC_PRSG_COUNT -gt 0 ]; then
    echo "✅ Documentation updated with 'prsg' references" | tee -a "$LOG_FILE"
else
    echo "⚠️  No 'prsg' references found in documentation" | tee -a "$LOG_FILE"
fi

# Results
echo "" | tee -a "$LOG_FILE"
echo "✅ VALIDATION PASSED - CLI command successfully renamed" | tee -a "$LOG_FILE"
exit 0