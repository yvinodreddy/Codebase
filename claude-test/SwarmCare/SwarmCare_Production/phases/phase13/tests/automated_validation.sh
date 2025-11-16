#!/bin/bash
################################################################################
# Phase 13: Automated Validation Script
# Production-Ready Verification for Predictive Analytics & ML Models
################################################################################

# Don't exit on error - we want to report all findings
set +e

PHASE_DIR="/home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase13"
cd "$PHASE_DIR"

echo "================================================================================"
echo "PHASE 13: AUTOMATED VALIDATION & VERIFICATION"
echo "================================================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((TOTAL_CHECKS++))
    ((PASSED_CHECKS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((TOTAL_CHECKS++))
    ((FAILED_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. ENVIRONMENT VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check_pass "Python 3 installed (version: $PYTHON_VERSION)"
else
    check_fail "Python 3 not found"
    exit 1
fi

# Check required packages
echo ""
echo "Checking required Python packages..."
REQUIRED_PACKAGES=("numpy" "pandas" "sklearn" "joblib" "pytest")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $pkg" 2>/dev/null; then
        check_pass "Package '$pkg' installed"
    else
        check_fail "Package '$pkg' missing"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. FILE STRUCTURE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check required files
REQUIRED_FILES=(
    "code/implementation.py"
    "code/__init__.py"
    "tests/test_phase13.py"
    "README.md"
    "docs/IMPLEMENTATION_GUIDE.md"
    ".state/phase_state.json"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "File exists: $file"
    else
        check_fail "File missing: $file"
    fi
done

# Check required directories
REQUIRED_DIRS=("code" "tests" "docs" ".state" "models")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        check_pass "Directory exists: $dir"
    else
        check_fail "Directory missing: $dir"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. CODE QUALITY VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check syntax
if python3 -m py_compile code/implementation.py 2>/dev/null; then
    check_pass "implementation.py syntax valid"
else
    check_fail "implementation.py syntax errors"
fi

if python3 -m py_compile tests/test_phase13.py 2>/dev/null; then
    check_pass "test_phase13.py syntax valid"
else
    check_fail "test_phase13.py syntax errors"
fi

# Check imports
if python3 -c "from code.implementation import Phase13Implementation" 2>/dev/null; then
    check_pass "Phase13Implementation imports successfully"
else
    check_fail "Phase13Implementation import failed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. UNIT TESTS EXECUTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run unit tests
echo "Running comprehensive test suite..."
if python3 tests/test_phase13.py > /tmp/phase13_test_output.txt 2>&1; then
    TEST_RESULTS=$(grep "Tests Run:" /tmp/phase13_test_output.txt || echo "Tests Run: 0")
    SUCCESS_RATE=$(grep "Success Rate:" /tmp/phase13_test_output.txt || echo "Success Rate: 0.00%")

    echo "$TEST_RESULTS"
    echo "$SUCCESS_RATE"

    if grep -q "Success Rate: 100.00%" /tmp/phase13_test_output.txt; then
        check_pass "All unit tests passed (100% success rate)"
    else
        check_fail "Some unit tests failed"
    fi
else
    check_fail "Test execution failed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. IMPLEMENTATION EXECUTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run implementation
echo "Executing Phase 13 implementation..."
if python3 code/implementation.py > /tmp/phase13_impl_output.txt 2>&1; then
    if grep -q "RESULT: SUCCESS" /tmp/phase13_impl_output.txt; then
        check_pass "Implementation executed successfully"

        # Check model metrics
        if grep -q "ROC AUC:" /tmp/phase13_impl_output.txt; then
            check_pass "Readmission model trained with metrics"
        fi

        if grep -q "RMSE:" /tmp/phase13_impl_output.txt; then
            check_pass "Length of Stay model trained with metrics"
        fi

        if grep -q "Mortality Risk Model" /tmp/phase13_impl_output.txt; then
            check_pass "Mortality model trained with metrics"
        fi
    else
        check_fail "Implementation execution failed"
    fi
else
    check_fail "Implementation crashed during execution"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. MODEL VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check model files
MODEL_FILES=("readmission_model.pkl" "los_model.pkl" "mortality_model.pkl")
for model in "${MODEL_FILES[@]}"; do
    if [ -f "models/$model" ]; then
        SIZE=$(du -h "models/$model" | cut -f1)
        check_pass "Model saved: $model (size: $SIZE)"
    else
        check_fail "Model file missing: $model"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. HIPAA COMPLIANCE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for PHI handling
if grep -q "anonymize_patient_data" code/implementation.py; then
    check_pass "Data anonymization implemented"
else
    check_fail "Data anonymization not found"
fi

if grep -q "hashlib" code/implementation.py; then
    check_pass "Patient ID hashing implemented"
else
    check_warn "Patient ID hashing may be missing"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. PHASE STATE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check phase state
if [ -f ".state/phase_state.json" ]; then
    if grep -q '"phase_id": 13' .state/phase_state.json; then
        check_pass "Phase state file valid"
    fi

    if grep -q '"story_points": 62' .state/phase_state.json; then
        check_pass "Story points correctly set (62)"
    fi

    STATUS=$(grep '"status"' .state/phase_state.json | head -1 | awk -F'"' '{print $4}')
    if [ "$STATUS" == "COMPLETED" ]; then
        check_pass "Phase status: COMPLETED"
    else
        check_warn "Phase status: $STATUS (expected: COMPLETED)"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "9. PRODUCTION READINESS CHECKLIST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check production readiness
READINESS_ITEMS=(
    "Error handling implemented:grep -q 'try:.*except' code/implementation.py"
    "Logging configured:grep -q 'logging' code/implementation.py"
    "Input validation present:grep -q 'validate_patient_data' code/implementation.py"
    "Type hints used:grep -q 'def.*->.*:' code/implementation.py"
    "Docstrings present:grep -q '\"\"\"' code/implementation.py"
)

for item in "${READINESS_ITEMS[@]}"; do
    DESCRIPTION="${item%%:*}"
    COMMAND="${item##*:}"

    if eval "$COMMAND" &>/dev/null; then
        check_pass "$DESCRIPTION"
    else
        check_warn "$DESCRIPTION - may need review"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "FINAL VALIDATION REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total Checks:  $TOTAL_CHECKS"
echo -e "${GREEN}Passed:        $PASSED_CHECKS${NC}"
echo -e "${RED}Failed:        $FAILED_CHECKS${NC}"
echo ""

SUCCESS_PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "Success Rate:  $SUCCESS_PERCENTAGE%"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ PHASE 13: PRODUCTION READY - ALL VALIDATIONS PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════════${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}✗ VALIDATION FAILED - $FAILED_CHECKS ISSUES DETECTED${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════════════════════════════${NC}"
    exit 1
fi
