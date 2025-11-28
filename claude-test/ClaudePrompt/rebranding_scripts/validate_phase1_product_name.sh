#!/bin/bash
# validate_phase1_product_name.sh
# Validates CHANGE 1.1 implementation

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="rebranding_logs/validate_phase1_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "VALIDATING PHASE 1.1: Product Name Changes" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Check 1: Verify new name exists
NEW_NAME_COUNT=$(grep -r "Para Group AI Orchestrator" /home/user01/claude-test/ClaudePrompt \
    --include="*.py" --include="*.md" 2>/dev/null | wc -l)
echo "New name occurrences: $NEW_NAME_COUNT" | tee -a "$LOG_FILE"

# Check 2: Verify old name removed (should be minimal/zero)
OLD_NAME_COUNT=$(grep -r "ClaudePrompt" /home/user01/claude-test/ClaudePrompt \
    --include="*.py" --include="*.md" 2>/dev/null | wc -l)
echo "Old name occurrences (should be 0): $OLD_NAME_COUNT" | tee -a "$LOG_FILE"

# Check 3: Verify ® symbol usage
REGISTERED_SYMBOL_COUNT=$(grep -r "®" /home/user01/claude-test/ClaudePrompt \
    --include="*.py" --include="*.md" 2>/dev/null | wc -l)
echo "® symbol occurrences: $REGISTERED_SYMBOL_COUNT" | tee -a "$LOG_FILE"

# Results
echo "" | tee -a "$LOG_FILE"
if [ $NEW_NAME_COUNT -gt 0 ] && [ $OLD_NAME_COUNT -eq 0 ] && [ $REGISTERED_SYMBOL_COUNT -gt 0 ]; then
    echo "✅ VALIDATION PASSED - Product name successfully rebranded" | tee -a "$LOG_FILE"
    exit 0
else
    echo "⚠️  VALIDATION FAILED - Review required" | tee -a "$LOG_FILE"
    exit 1
fi