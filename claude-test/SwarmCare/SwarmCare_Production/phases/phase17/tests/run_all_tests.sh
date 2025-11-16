#!/bin/bash
################################################################################
# Phase 17: Population Health Management
# Comprehensive Test Runner
################################################################################

set -e

echo ""
echo "================================================================================"
echo "PHASE 17: POPULATION HEALTH MANAGEMENT - COMPREHENSIVE TEST SUITE"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to tests directory
cd "$(dirname "$0")"

TEST_RESULTS=()
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo ""
    echo "================================================================================"
    echo "$test_name"
    echo "================================================================================"

    if eval "$test_command"; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}"
        TEST_RESULTS+=("✅ $test_name")
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        TEST_RESULTS+=("❌ $test_name")
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test 1: Implementation Tests
run_test "TEST 1: Implementation Tests" "python3 test_phase17.py"

# Test 2: Population Health Core Tests
run_test "TEST 2: Population Health Core Tests" "python3 test_population_health.py"

# Test 3: Production Validation
run_test "TEST 3: Production Validation" "python3 validate_phase17.py"

# Test 4: Performance Benchmarks
run_test "TEST 4: Performance Benchmarks" "bash benchmark_phase17.sh"

# Summary
echo ""
echo "================================================================================"
echo "TEST SUMMARY"
echo "================================================================================"
echo ""
for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
done
echo ""
echo "================================================================================"
echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}Success Rate: 100%${NC}"
else
    echo -e "${YELLOW}Success Rate: $(( TESTS_PASSED * 100 / (TESTS_PASSED + TESTS_FAILED) ))%${NC}"
fi
echo "================================================================================"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED - PHASE 17 IS PRODUCTION READY! 🎉${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED - REVIEW REQUIRED ⚠️${NC}"
    echo ""
    exit 1
fi
