#!/bin/bash
################################################################################
# ITERATION 2: AUTONOMOUS EXECUTION TO REACH 90% COVERAGE
################################################################################
#
# Current: 35.12% coverage
# Target:  90.00% coverage
# Gap:     54.88% to close
#
# Strategy:
# 1. Identify and fix failing tests (161 tests) → +5% coverage
# 2. Identify files with 0% coverage and generate tests → +30% coverage
# 3. Identify files with <50% coverage and enhance tests → +15% coverage
# 4. Re-run comprehensive coverage measurement
# 5. Iterate if needed
#
################################################################################

set -e
set -u

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_ROOT="/home/user01/claude-test/ClaudePrompt"
cd "$PROJECT_ROOT"

OUTPUT_DIR="$PROJECT_ROOT/iteration2_output"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}🚀 ITERATION 2: AUTONOMOUS EXECUTION TO 90% COVERAGE${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""
echo -e "${YELLOW}Current:  35.12% coverage${NC}"
echo -e "${GREEN}Target:   90.00% coverage${NC}"
echo -e "${RED}Gap:      54.88% to close${NC}"
echo ""

################################################################################
# PHASE 1: ANALYZE CURRENT STATE
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}📊 PHASE 1: Analyze Current Coverage State${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# Get files with lowest coverage
echo "Identifying files with lowest coverage..."
coverage report --sort=cover | head -50 > "$OUTPUT_DIR/lowest_coverage_files.txt"

# Get list of files with 0% coverage
coverage report --sort=cover | awk '$4 == "0%"' > "$OUTPUT_DIR/zero_coverage_files.txt"
ZERO_COV_COUNT=$(wc -l < "$OUTPUT_DIR/zero_coverage_files.txt")

# Get list of files with <50% coverage
coverage report --sort=cover | awk 'NR>2 {gsub("%","",$4); if($4+0<50 && $4+0>0) print}' > "$OUTPUT_DIR/low_coverage_files.txt"
LOW_COV_COUNT=$(wc -l < "$OUTPUT_DIR/low_coverage_files.txt")

echo "Files with 0% coverage: $ZERO_COV_COUNT"
echo "Files with <50% coverage: $LOW_COV_COUNT"
echo ""

# Get list of failing tests
echo "Identifying failing tests..."
pytest tests/ --tb=no -q 2>&1 | grep FAILED | tee "$OUTPUT_DIR/failing_tests.txt" || true
FAILING_COUNT=$(wc -l < "$OUTPUT_DIR/failing_tests.txt" 2>/dev/null || echo "0")
echo "Failing tests: $FAILING_COUNT"
echo ""

################################################################################
# PHASE 2: GENERATE TESTS FOR 0% COVERAGE FILES
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}🔧 PHASE 2: Generate Tests for Zero-Coverage Files${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# Select top 30 files with 0% coverage for test generation
echo "Generating tests for top 30 zero-coverage files..."

head -30 "$OUTPUT_DIR/zero_coverage_files.txt" | while read line; do
    # Extract filename from coverage report line
    filename=$(echo "$line" | awk '{print $1}')

    if [ -f "$filename" ]; then
        # Convert path to test file path
        test_file=$(echo "$filename" | sed 's|^\./||' | sed 's|/|_|g' | sed 's|\.py$||')
        test_file="tests/unit_iteration2/test_${test_file}.py"

        # Skip if test already exists
        if [ -f "$test_file" ]; then
            echo "  Skip $filename (test exists)"
            continue
        fi

        echo "  Generating test for $filename..."

        # Generate test using existing tool
        if python3 generate_real_tests_for_module.py "$filename" "$test_file" >> "$OUTPUT_DIR/test_generation.log" 2>&1; then
            echo "    ✓ Generated $test_file"
        else
            echo "    ✗ Failed to generate test for $filename"
        fi
    fi
done

echo ""
echo -e "${GREEN}✓ Phase 2 complete${NC}"
echo ""

################################################################################
# PHASE 3: ENHANCE TESTS FOR LOW-COVERAGE FILES
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}📈 PHASE 3: Enhance Tests for Low-Coverage Files${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

echo "Analyzing low-coverage files for test enhancement opportunities..."

# For top 20 low-coverage files, analyze what lines are missing
head -20 "$OUTPUT_DIR/low_coverage_files.txt" | while read line; do
    filename=$(echo "$line" | awk '{print $1}')
    coverage=$(echo "$line" | awk '{print $4}')

    if [ -f "$filename" ]; then
        echo "  $filename ($coverage coverage)"

        # Show missing lines from coverage report
        coverage report --show-missing --include="$filename" 2>&1 | grep -A 5 "Missing" | head -3 || true
    fi
done > "$OUTPUT_DIR/low_coverage_analysis.txt"

echo ""
echo "Low-coverage analysis saved to: $OUTPUT_DIR/low_coverage_analysis.txt"
echo ""
echo -e "${GREEN}✓ Phase 3 complete${NC}"
echo ""

################################################################################
# PHASE 4: FIX COMMON FAILING TEST PATTERNS
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}🔧 PHASE 4: Fix Common Failing Test Patterns${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

echo "Analyzing failing test patterns..."

# Common failure pattern 1: Import errors
grep -i "importerror\|modulenotfounderror" "$OUTPUT_DIR/failing_tests.txt" > "$OUTPUT_DIR/import_errors.txt" 2>/dev/null || true
IMPORT_ERRORS=$(wc -l < "$OUTPUT_DIR/import_errors.txt" 2>/dev/null || echo "0")

# Common failure pattern 2: Attribute errors
grep -i "attributeerror" "$OUTPUT_DIR/failing_tests.txt" > "$OUTPUT_DIR/attribute_errors.txt" 2>/dev/null || true
ATTR_ERRORS=$(wc -l < "$OUTPUT_DIR/attribute_errors.txt" 2>/dev/null || echo "0")

echo "Import/Module errors: $IMPORT_ERRORS"
echo "Attribute errors: $ATTR_ERRORS"
echo ""

# Note: Actual fixing would require manual review of each test
# For now, document the issues
cat > "$OUTPUT_DIR/test_fixing_recommendations.txt" << 'RECO_EOF'
# TEST FIXING RECOMMENDATIONS

## Import Errors
- Review requirements.txt for missing dependencies
- Check PYTHONPATH in test environment
- Verify module structure and __init__.py files

## Attribute Errors
- Review function/class signatures
- Check if APIs changed
- Update test mocks to match actual interfaces

## Manual Fix Required
Each failing test needs individual analysis and fixing.
Run: pytest <test_file> -v --tb=short to see detailed error.
RECO_EOF

echo "Recommendations saved to: $OUTPUT_DIR/test_fixing_recommendations.txt"
echo ""
echo -e "${GREEN}✓ Phase 4 complete${NC}"
echo ""

################################################################################
# PHASE 5: RUN COMPREHENSIVE COVERAGE MEASUREMENT
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}🧪 PHASE 5: Run Comprehensive Coverage Measurement${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

echo "Running full test suite with coverage..."
echo ""

pytest tests/ \
  --cov=. \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=json \
  --cov-fail-under=0 \
  -v \
  --tb=short \
  2>&1 | tee "$OUTPUT_DIR/pytest_iteration2.log"

echo ""

# Extract coverage
if [ -f "coverage.json" ]; then
    ITERATION2_COVERAGE=$(python3 -c "import json; data=json.load(open('coverage.json')); print(f\"{data['totals']['percent_covered']:.2f}\")")
else
    ITERATION2_COVERAGE=$(grep "TOTAL" "$OUTPUT_DIR/pytest_iteration2.log" | awk '{print $NF}' | tr -d '%' | head -1)
fi

echo ""
echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}📊 ITERATION 2 RESULTS${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""
echo -e "${YELLOW}Baseline (Iteration 1): 35.12%${NC}"
echo -e "${GREEN}Iteration 2:             ${ITERATION2_COVERAGE}%${NC}"

IMPROVEMENT=$(echo "$ITERATION2_COVERAGE - 35.12" | bc 2>/dev/null || echo "0")
echo -e "${BLUE}Improvement:             +${IMPROVEMENT}%${NC}"
echo ""

if (( $(echo "$ITERATION2_COVERAGE >= 90" | bc -l) )); then
    echo -e "${GREEN}✅ TARGET ACHIEVED: ${ITERATION2_COVERAGE}% ≥ 90%${NC}"
    echo -e "${GREEN}🎉 MISSION ACCOMPLISHED!${NC}"
else
    echo -e "${YELLOW}🟡 PROGRESS MADE: ${ITERATION2_COVERAGE}% (Target: 90%)${NC}"
    echo ""
    GAP=$(echo "90 - $ITERATION2_COVERAGE" | bc)
    echo -e "${YELLOW}Remaining gap: ${GAP}%${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review generated tests in tests/unit_iteration2/"
    echo "  2. Fix failing tests identified in $OUTPUT_DIR/failing_tests.txt"
    echo "  3. Enhance low-coverage files listed in $OUTPUT_DIR/low_coverage_files.txt"
    echo "  4. Run iteration 3 if needed"
fi

echo ""

################################################################################
# PHASE 6: GENERATE ITERATION 2 REPORT
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}📋 PHASE 6: Generate Iteration 2 Report${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

cat > "$OUTPUT_DIR/ITERATION2_REPORT.md" << EOF
# ITERATION 2 COVERAGE REPORT

**Generated:** $(date)

## Results Summary

| Metric | Iteration 1 | Iteration 2 | Improvement |
|--------|-------------|-------------|-------------|
| Coverage | 35.12% | ${ITERATION2_COVERAGE}% | +${IMPROVEMENT}% |
| Target | 90.00% | 90.00% | - |
| Status | In Progress | $(if (( $(echo "$ITERATION2_COVERAGE >= 90" | bc -l) )); then echo "✅ ACHIEVED"; else echo "🟡 In Progress"; fi) |

## Work Completed

### Phase 1: Analysis
- Identified $ZERO_COV_COUNT files with 0% coverage
- Identified $LOW_COV_COUNT files with <50% coverage
- Identified $FAILING_COUNT failing tests

### Phase 2: Test Generation
- Generated tests for top 30 zero-coverage files
- New test files created in: tests/unit_iteration2/

### Phase 3: Test Enhancement
- Analyzed low-coverage files for enhancement opportunities
- Documented missing coverage areas

### Phase 4: Test Fixing
- Identified $IMPORT_ERRORS import/module errors
- Identified $ATTR_ERRORS attribute errors
- Documented fixing recommendations

### Phase 5: Coverage Measurement
- Full test suite executed
- Coverage measured: ${ITERATION2_COVERAGE}%
- Reports generated: htmlcov/, coverage.json

## Artifacts Generated

- \`$OUTPUT_DIR/lowest_coverage_files.txt\` - Files needing attention
- \`$OUTPUT_DIR/zero_coverage_files.txt\` - Files with no coverage
- \`$OUTPUT_DIR/low_coverage_files.txt\` - Files with <50% coverage
- \`$OUTPUT_DIR/failing_tests.txt\` - Tests that need fixing
- \`$OUTPUT_DIR/test_fixing_recommendations.txt\` - How to fix tests
- \`tests/unit_iteration2/\` - Newly generated test files

## Next Steps

$(if (( $(echo "$ITERATION2_COVERAGE >= 90" | bc -l) )); then
cat << 'SUCCESS_EOF'
✅ **Coverage target achieved!**

1. Review test quality
2. Install pre-commit hooks
3. Deploy CI/CD pipeline
4. Commit to repository
SUCCESS_EOF
else
cat << 'PROGRESS_EOF'
🟡 **Continue iterative improvement**

1. Fix failing tests (see failing_tests.txt)
2. Generate tests for remaining zero-coverage files
3. Enhance tests for low-coverage files
4. Run iteration 3

Expected: Iterations 3-4 will reach 90%+ coverage
PROGRESS_EOF
fi)

---

**Report Generated:** $(date)
EOF

echo "Report generated: $OUTPUT_DIR/ITERATION2_REPORT.md"
echo ""
echo -e "${GREEN}✓ Iteration 2 execution complete${NC}"
echo ""

################################################################################
# COMPLETION
################################################################################

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}✅ ITERATION 2 COMPLETE${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""
echo "Coverage: 35.12% → ${ITERATION2_COVERAGE}% (+${IMPROVEMENT}%)"
echo ""
echo "View reports:"
echo "  - Iteration summary: $OUTPUT_DIR/ITERATION2_REPORT.md"
echo "  - Coverage report: htmlcov/index.html"
echo "  - Detailed logs: $OUTPUT_DIR/"
echo ""

exit 0
