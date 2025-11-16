#!/bin/bash

################################################################################
# Phase 25: Run All Tests
################################################################################
#
# Executes complete test suite:
# 1. Implementation tests (15 tests)
# 2. Core XAI tests (32 tests)
# 3. Production validation (28 checks)
# 4. Performance benchmarks (6 benchmarks)
#
# Total: 81 tests/checks/benchmarks
#
################################################################################

set -e

cd "$(dirname "$0")"

echo "================================================================================"
echo "PHASE 25: COMPREHENSIVE TEST SUITE"
echo "================================================================================"
echo "Started: $(date)"
echo "================================================================================"
echo ""

PYTHON_CMD="python3"
TOTAL_PASSED=0
TOTAL_FAILED=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

run_test() {
    local test_name=$1
    local test_command=$2

    echo "================================================================================"
    echo "Running: $test_name"
    echo "================================================================================"

    if eval $test_command; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        return 1
    fi
}

# ============================================================================
# TEST 1: Implementation Tests
# ============================================================================
echo ""
if run_test "Implementation Tests" "$PYTHON_CMD test_phase25.py -v 2>&1"; then
    ((TOTAL_PASSED++))
else
    ((TOTAL_FAILED++))
fi

# ============================================================================
# TEST 2: Core XAI Tests
# ============================================================================
echo ""
if run_test "Core XAI Tests" "$PYTHON_CMD test_patient_facing_xai.py -v 2>&1"; then
    ((TOTAL_PASSED++))
else
    ((TOTAL_FAILED++))
fi

# ============================================================================
# TEST 3: Production Validation
# ============================================================================
echo ""
if run_test "Production Validation" "$PYTHON_CMD validate_phase25.py 2>&1"; then
    ((TOTAL_PASSED++))
else
    ((TOTAL_FAILED++))
fi

# ============================================================================
# TEST 4: Performance Benchmarks
# ============================================================================
echo ""
if run_test "Performance Benchmarks" "bash benchmark_phase25.sh 2>&1"; then
    ((TOTAL_PASSED++))
else
    ((TOTAL_FAILED++))
fi

# ============================================================================
# FINAL SUMMARY
# ============================================================================
echo ""
echo "================================================================================"
echo "FINAL TEST SUMMARY"
echo "================================================================================"
echo "Test Suites Passed: $TOTAL_PASSED/4"
echo "Test Suites Failed: $TOTAL_FAILED/4"
echo "================================================================================"

if [ $TOTAL_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TEST SUITES PASSED - PRODUCTION READY${NC}"
    echo "================================================================================"
    exit 0
else
    echo -e "${RED}❌ SOME TEST SUITES FAILED${NC}"
    echo "================================================================================"
    exit 1
fi
