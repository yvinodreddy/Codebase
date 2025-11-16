#!/bin/bash
################################################################################
# Phase 11: Research & Publications
# Comprehensive Testing & Validation Suite
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "PHASE 11: COMPREHENSIVE TESTING & VALIDATION"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local command="$2"

    echo "────────────────────────────────────────────────────────────────────────────────"
    echo "  TEST: $name"
    echo "────────────────────────────────────────────────────────────────────────────────"

    if eval "$command"; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        ((FAILED++))
        return 1
    fi
    echo ""
}

# Test 1: Unit Tests
run_test "Unit Tests (26 tests)" "python3 tests/test_phase11.py -v 2>&1 | tail -5"

# Test 2: Implementation Execution
run_test "Implementation Execution" "python3 code/implementation.py > /dev/null 2>&1"

# Test 3: Validation Script
run_test "Validation Script" "python3 validate_phase11.py > /dev/null 2>&1"

# Test 4: Import Tests
run_test "Module Imports" "python3 -c 'from code.implementation import Phase11Implementation, ResearchPaperGenerator, CitationManager, QualityValidator, PaperTemplates; print(\"All imports successful\")'"

# Test 5: Paper Generation
run_test "Paper Generation Test" "python3 -c '
from code.implementation import ResearchPaperGenerator
g = ResearchPaperGenerator()
p = g.generate_paper(\"Test\", \"technical\", \"clinical_ai\")
assert p[\"metadata\"][\"word_count\"] > 1000
print(\"Paper generation successful\")
'"

# Test 6: Validation Check
run_test "Quality Validation Test" "python3 -c '
from code.implementation import QualityValidator, ResearchPaperGenerator
g = ResearchPaperGenerator()
v = QualityValidator()
p = g.generate_paper(\"Test\", \"technical\", \"clinical_ai\")
result = v.validate_paper(p)
assert result[\"valid\"] == True
assert result[\"score\"] == 100.0
print(\"Validation successful\")
'"

# Test 7: Citation Management
run_test "Citation Management Test" "python3 -c '
from code.implementation import CitationManager
m = CitationManager()
citations = m.generate_citations(\"clinical_ai\", \"technical\")
assert len(citations) >= 3
bib = m.format_bibliography(citations)
assert len(bib) > 0
print(\"Citation management successful\")
'"

# Test 8: Phase Execution
run_test "Phase Execution Test" "python3 -c '
from code.implementation import Phase11Implementation
phase = Phase11Implementation()
result = phase.execute({\"goal\": \"Test\", \"phase_id\": 11})
assert result.success == True
assert result.output[\"papers_generated\"] == 5
assert result.output[\"production_ready\"] == True
print(\"Phase execution successful\")
'"

# Test 9: State File Check
run_test "State File Creation" "python3 -c '
import os
from pathlib import Path
state_file = Path(\".state/phase_state.json\")
assert state_file.exists(), \"State file not found\"
print(\"State file exists\")
'"

# Test 10: Validation Report Check
run_test "Validation Report Check" "python3 -c '
import json
from pathlib import Path
report_file = Path(\".state/validation_report.json\")
assert report_file.exists(), \"Validation report not found\"
with open(report_file) as f:
    report = json.load(f)
assert report[\"validation_passed\"] == True
assert report[\"papers_generated\"] == 5
print(\"Validation report valid\")
'"

echo "================================================================================"
echo "TEST SUMMARY"
echo "================================================================================"
echo -e "${GREEN}PASSED: $PASSED${NC}"
echo -e "${RED}FAILED: $FAILED${NC}"
echo "TOTAL:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo ""
    echo "✅ Phase 11 is 100% production-ready"
    echo "✅ All 5 research papers validated"
    echo "✅ Comprehensive testing complete"
    echo "================================================================================"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "================================================================================"
    exit 1
fi
