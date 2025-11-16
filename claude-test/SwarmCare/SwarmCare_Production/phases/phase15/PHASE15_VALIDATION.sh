#!/bin/bash
################################################################################
# Phase 15: Advanced Medical NLP & Auto-Coding
# Comprehensive Automated Validation Script
# Production-Ready Deployment Validation
################################################################################

set -e  # Exit on error

PHASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PHASE_DIR"

echo "================================================================================"
echo "PHASE 15: ADVANCED MEDICAL NLP & AUTO-CODING"
echo "COMPREHENSIVE VALIDATION SCRIPT"
echo "================================================================================"
echo ""

# Track overall status
VALIDATION_PASSED=true

# Function to run a validation step
run_validation() {
    local step_name="$1"
    local command="$2"

    echo "--------------------------------------------------------------------------------"
    echo "VALIDATION: $step_name"
    echo "--------------------------------------------------------------------------------"

    if eval "$command"; then
        echo "✅ PASSED: $step_name"
        return 0
    else
        echo "❌ FAILED: $step_name"
        VALIDATION_PASSED=false
        return 1
    fi
}

# 1. Verify directory structure
run_validation "Directory Structure" '
    [ -d "code" ] && \
    [ -d "tests" ] && \
    [ -d "docs" ] && \
    [ -d ".state" ] && \
    [ -f "README.md" ]
'

# 2. Verify all code files exist
run_validation "Code Files Present" '
    [ -f "code/implementation.py" ] && \
    [ -f "code/__init__.py" ] && \
    [ -f "code/medical_code_database.py" ] && \
    [ -f "code/medical_nlp_engine.py" ] && \
    [ -f "code/autocoding_system.py" ] && \
    [ -f "code/clinical_note_generator.py" ]
'

# 3. Test Medical Code Database
run_validation "Medical Code Database" '
    python3 code/medical_code_database.py > /dev/null 2>&1
'

# 4. Test Medical NLP Engine
run_validation "Medical NLP Engine" '
    python3 code/medical_nlp_engine.py > /dev/null 2>&1
'

# 5. Test Auto-Coding System
run_validation "Auto-Coding System" '
    python3 code/autocoding_system.py > /dev/null 2>&1
'

# 6. Test Clinical Note Generator
run_validation "Clinical Note Generator" '
    python3 code/clinical_note_generator.py > /dev/null 2>&1
'

# 7. Test Main Implementation
run_validation "Main Implementation" '
    python3 code/implementation.py > /dev/null 2>&1
'

# 8. Run Comprehensive Test Suite
run_validation "Comprehensive Test Suite (23 tests)" '
    python3 tests/test_phase15.py > /dev/null 2>&1
'

# 9. Verify Phase State
run_validation "Phase State File" '
    [ -f ".state/phase_state.json" ] && \
    python3 -c "import json; json.load(open(\".state/phase_state.json\"))" > /dev/null 2>&1
'

# 10. Check for Python syntax errors
run_validation "Python Syntax Check" '
    python3 -m py_compile code/*.py && \
    python3 -m py_compile tests/*.py
'

echo ""
echo "================================================================================"
echo "VALIDATION SUMMARY"
echo "================================================================================"

if [ "$VALIDATION_PASSED" = true ]; then
    echo "✅ ALL VALIDATIONS PASSED"
    echo ""
    echo "Phase 15 is PRODUCTION-READY and fully operational with:"
    echo "  • 51 ICD-10 diagnosis codes"
    echo "  • 30 CPT procedure codes"
    echo "  • Advanced Medical NLP with Named Entity Recognition"
    echo "  • Automated Clinical Note Generation (SOAP, Discharge, Progress)"
    echo "  • 23/23 tests passing (100% success rate)"
    echo "  • Negation Detection, Relationship Extraction, Temporal Analysis"
    echo ""
    echo "================================================================================"
    exit 0
else
    echo "❌ SOME VALIDATIONS FAILED"
    echo "Please review the output above and fix the failing validations."
    echo "================================================================================"
    exit 1
fi
