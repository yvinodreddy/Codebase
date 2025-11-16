#!/bin/bash
# Claude Code Mastery System Validation Script
# Validates all documentation and scripts are working correctly

echo "=============================================="
echo "Claude Code Mastery System Validation"
echo "=============================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Function to check file existence
check_file() {
    local file=$1
    local description=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description: $file"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $description: $file (MISSING)"
        ((FAIL++))
        return 1
    fi
}

# Function to check file content
check_content() {
    local file=$1
    local pattern=$2
    local description=$3

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description"
        ((PASS++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $description"
        ((WARN++))
        return 1
    fi
}

# Function to check script execution
check_script() {
    local script=$1
    local description=$2

    if [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} $description: executable"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $description: not executable"
        ((FAIL++))
        return 1
    fi
}

echo "1. Checking Documentation Files..."
echo "-----------------------------------"
check_file "README.md" "Master README"
check_file "CLAUDE_CODE_COMPLETE_GUIDE.md" "Complete Guide"
check_file "QUICK_REFERENCE_CARD.md" "Quick Reference"
check_file "LEARNING_PATH.md" "Learning Path"
check_file "PRACTICE_SCENARIOS.md" "Practice Scenarios"
check_file "PRODUCTIVITY_WORKFLOWS.md" "Productivity Workflows"
check_file "SETUP_GUIDE.md" "Setup Guide"
echo ""

echo "2. Checking Scripts..."
echo "-----------------------------------"
check_file "monitor_releases.py" "Release Monitor Script"
check_script "monitor_releases.py" "Release Monitor Script"
echo ""

echo "3. Checking Documentation Structure..."
echo "-----------------------------------"
check_content "README.md" "Quick Start" "README has Quick Start section"
check_content "README.md" "Learning Paths" "README has Learning Paths"
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Table of Contents" "Complete Guide has TOC"
check_content "QUICK_REFERENCE_CARD.md" "Keyboard Shortcuts" "Quick Reference has shortcuts"
check_content "LEARNING_PATH.md" "30-Day" "Learning Path has 30-day plan"
check_content "PRACTICE_SCENARIOS.md" "Scenario" "Practice has scenarios"
check_content "PRODUCTIVITY_WORKFLOWS.md" "Workflow" "Workflows document exists"
check_content "SETUP_GUIDE.md" "Prerequisites" "Setup has prerequisites"
echo ""

echo "4. Testing Python Script..."
echo "-----------------------------------"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python 3 is installed"
    ((PASS++))

    # Test script syntax
    if python3 -m py_compile monitor_releases.py 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Release monitor script syntax is valid"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Release monitor script has syntax errors"
        ((FAIL++))
    fi

    # Test help command
    if python3 monitor_releases.py --help > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Release monitor --help works"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Release monitor --help failed"
        ((FAIL++))
    fi

    # Test status command
    if python3 monitor_releases.py --status > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Release monitor --status works"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Release monitor --status failed"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗${NC} Python 3 is not installed"
    ((FAIL++))
fi
echo ""

echo "5. Checking Documentation Quality..."
echo "-----------------------------------"

# Check word counts (should be substantial)
for file in README.md CLAUDE_CODE_COMPLETE_GUIDE.md LEARNING_PATH.md PRACTICE_SCENARIOS.md PRODUCTIVITY_WORKFLOWS.md SETUP_GUIDE.md QUICK_REFERENCE_CARD.md; do
    if [ -f "$file" ]; then
        words=$(wc -w < "$file")
        if [ "$words" -gt 1000 ]; then
            echo -e "${GREEN}✓${NC} $file: $words words (substantial)"
            ((PASS++))
        elif [ "$words" -gt 500 ]; then
            echo -e "${YELLOW}⚠${NC} $file: $words words (moderate)"
            ((WARN++))
        else
            echo -e "${RED}✗${NC} $file: $words words (too short)"
            ((FAIL++))
        fi
    fi
done
echo ""

echo "6. Checking for Key Sections..."
echo "-----------------------------------"

# Check README completeness
check_content "README.md" "Quick Start" "README: Quick Start"
check_content "README.md" "Learning Paths" "README: Learning Paths"
check_content "README.md" "Documentation Overview" "README: Documentation Overview"
check_content "README.md" "ROI Calculator" "README: ROI Calculator"
check_content "README.md" "30-Day Challenge" "README: 30-Day Challenge"

# Check Complete Guide completeness
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Quick Start" "Complete Guide: Quick Start"
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Core Concepts" "Complete Guide: Core Concepts"
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Intermediate" "Complete Guide: Intermediate"
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Advanced" "Complete Guide: Advanced"
check_content "CLAUDE_CODE_COMPLETE_GUIDE.md" "Productivity Multipliers" "Complete Guide: Productivity"

# Check Learning Path structure
check_content "LEARNING_PATH.md" "WEEK 1" "Learning Path: Week 1"
check_content "LEARNING_PATH.md" "WEEK 2" "Learning Path: Week 2"
check_content "LEARNING_PATH.md" "Day 1:" "Learning Path: Daily structure"

echo ""

echo "7. Checking Cross-References..."
echo "-----------------------------------"

# Check if README links to other documents
check_content "README.md" "SETUP_GUIDE.md" "README links to Setup Guide"
check_content "README.md" "LEARNING_PATH.md" "README links to Learning Path"
check_content "README.md" "PRACTICE_SCENARIOS.md" "README links to Practice"
check_content "README.md" "PRODUCTIVITY_WORKFLOWS.md" "README links to Workflows"

echo ""

echo "8. File Statistics..."
echo "-----------------------------------"
echo "Documentation Files:"
ls -lh *.md 2>/dev/null | awk '{print "  " $9 ": " $5}'
echo ""
echo "Script Files:"
ls -lh *.py *.sh 2>/dev/null | awk '{print "  " $9 ": " $5}'
echo ""

echo "9. Line Counts..."
echo "-----------------------------------"
for file in *.md *.py; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        echo "  $file: $lines lines"
    fi
done
echo ""

# Summary
echo "=============================================="
echo "VALIDATION SUMMARY"
echo "=============================================="
echo -e "${GREEN}Passed:${NC}  $PASS"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo -e "${RED}Failed:${NC}  $FAIL"
echo ""

TOTAL=$((PASS + WARN + FAIL))
if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$((PASS * 100 / TOTAL))
    echo "Success Rate: ${SUCCESS_RATE}%"
    echo ""
fi

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CRITICAL CHECKS PASSED!${NC}"
    echo ""
    echo "The Claude Code Mastery System is complete and ready to use!"
    echo ""
    echo "Next Steps:"
    echo "  1. Read README.md for overview"
    echo "  2. Follow SETUP_GUIDE.md for installation"
    echo "  3. Start with LEARNING_PATH.md Day 1"
    echo "  4. Keep QUICK_REFERENCE_CARD.md handy"
    echo ""
    exit 0
else
    echo -e "${RED}✗ SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please fix the issues above before proceeding."
    echo ""
    exit 1
fi
