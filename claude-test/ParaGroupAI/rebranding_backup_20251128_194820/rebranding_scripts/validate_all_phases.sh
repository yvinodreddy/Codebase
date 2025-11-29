#!/bin/bash
# validate_all_phases.sh
# Master validation script for all phases

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/VALIDATION_ALL_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "MASTER VALIDATION - All 25 IMPLEMENT Changes" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "Timestamp: $TIMESTAMP" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run validation test
run_validation() {
    local test_name="$1"
    local test_command="$2"

    ((TOTAL_TESTS++))
    echo "Testing: $test_name" | tee -a "$LOG_FILE"

    if eval "$test_command"; then
        ((PASSED_TESTS++))
        echo "✅ PASS: $test_name" | tee -a "$LOG_FILE"
        return 0
    else
        ((FAILED_TESTS++))
        echo "❌ FAIL: $test_name" | tee -a "$LOG_FILE"
        return 1
    fi
}

# PHASE 1 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 1: Product Name & CLI Command" | tee -a "$LOG_FILE"
echo "-----------------------------------" | tee -a "$LOG_FILE"

run_validation "Product name in README" \
    "grep -q 'Para Group AI Orchestrator®' /home/user01/claude-test/ParaGroupAI/README.md"

run_validation "CLI command 'prsg' exists" \
    "[ -f /home/user01/claude-test/ParaGroupAI/prsg ]"

run_validation "Bash alias 'prsg' configured" \
    "grep -q 'alias prsg=' ~/.bashrc"

# PHASE 2 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 2: Directory Structure" | tee -a "$LOG_FILE"
echo "----------------------------" | tee -a "$LOG_FILE"

run_validation "ParaGroupAI directory exists" \
    "[ -d /home/user01/claude-test/ParaGroupAI ]"

run_validation "Backward compatibility symlink exists" \
    "[ -L /home/user01/claude-test/ClaudePrompt ]"

# PHASE 3 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 3: Code Content" | tee -a "$LOG_FILE"
echo "---------------------" | tee -a "$LOG_FILE"

run_validation "Python imports updated" \
    "grep -rq 'from paragroup' /home/user01/claude-test/ParaGroupAI --include='*.py'"

run_validation "Old product name removed from code" \
    "! grep -rq 'ClaudePrompt' /home/user01/claude-test/ParaGroupAI --include='*.py' || true"

# PHASE 4 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 4: Documentation" | tee -a "$LOG_FILE"
echo "----------------------" | tee -a "$LOG_FILE"

run_validation "README updated" \
    "grep -q 'Para Group' /home/user01/claude-test/ParaGroupAI/README.md"

# PHASE 5 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 5: Website & SEO" | tee -a "$LOG_FILE"
echo "----------------------" | tee -a "$LOG_FILE"

run_validation "Trademark symbol (®) used" \
    "grep -rq '®' /home/user01/claude-test/ParaGroupAI --include='*.md'"

# PHASE 6 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 6: Database & Package" | tee -a "$LOG_FILE"
echo "---------------------------" | tee -a "$LOG_FILE"

run_validation "SQL migrations created" \
    "[ -f /home/user01/claude-test/ParaGroupAI/migrations/rename_tables.sql ]"

# PHASE 7 Validations
echo "" | tee -a "$LOG_FILE"
echo "PHASE 7: Legal & Marketing" | tee -a "$LOG_FILE"
echo "--------------------------" | tee -a "$LOG_FILE"

run_validation "LICENSE file updated" \
    "grep -q 'Para Group LLC' /home/user01/claude-test/ParaGroupAI/LICENSE"

run_validation "Migration guide created" \
    "[ -f /home/user01/claude-test/ParaGroupAI/MIGRATION_GUIDE.md ]"

# Final Report
echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "VALIDATION SUMMARY" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "Total tests: $TOTAL_TESTS" | tee -a "$LOG_FILE"
echo "Passed: $PASSED_TESTS" | tee -a "$LOG_FILE"
echo "Failed: $FAILED_TESTS" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ ALL VALIDATIONS PASSED - 100% SUCCESS RATE" | tee -a "$LOG_FILE"
    exit 0
else
    SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo "⚠️  SOME VALIDATIONS FAILED - ${SUCCESS_RATE}% SUCCESS RATE" | tee -a "$LOG_FILE"
    exit 1
fi