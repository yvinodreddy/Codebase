#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║           EXAM SYSTEM INTEGRATION VALIDATION SCRIPT                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

function test_check {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC} - $2"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}❌ FAIL${NC} - $2"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

function info_message {
    echo -e "${BLUE}ℹ️  INFO${NC} - $1"
}

function section_header {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Change to production directory
cd "$(dirname "$0")" || exit 1

section_header "1. FILE EXISTENCE CHECKS"

# Check if all required files exist
test_check "$([ -f "questions-database.js" ]; echo $?)" "questions-database.js exists"
test_check "$([ -f "questions-subjective.js" ]; echo $?)" "questions-subjective.js exists"
test_check "$([ -f "exam-integration.js" ]; echo $?)" "exam-integration.js exists"
test_check "$([ -f "index.html" ]; echo $?)" "index.html exists"
test_check "$([ -f "test-exam-system.html" ]; echo $?)" "test-exam-system.html exists"
test_check "$([ -f "test-integration.html" ]; echo $?)" "test-integration.html exists"

# Check backup exists
BACKUP_COUNT=$(ls -1 index.html.backup_* 2>/dev/null | wc -l)
test_check "$([ $BACKUP_COUNT -gt 0 ]; echo $?)" "Backup of original index.html exists ($BACKUP_COUNT backup(s) found)"

section_header "2. FILE SIZE VALIDATION"

# Check file sizes are reasonable
DB_SIZE=$(stat -f%z questions-database.js 2>/dev/null || stat -c%s questions-database.js 2>/dev/null)
test_check "$([ $DB_SIZE -gt 10000 ]; echo $?)" "questions-database.js has content ($(numfmt --to=iec $DB_SIZE 2>/dev/null || echo ${DB_SIZE} bytes))"

SUB_SIZE=$(stat -f%z questions-subjective.js 2>/dev/null || stat -c%s questions-subjective.js 2>/dev/null)
test_check "$([ $SUB_SIZE -gt 10000 ]; echo $?)" "questions-subjective.js has content ($(numfmt --to=iec $SUB_SIZE 2>/dev/null || echo ${SUB_SIZE} bytes))"

INT_SIZE=$(stat -f%z exam-integration.js 2>/dev/null || stat -c%s exam-integration.js 2>/dev/null)
test_check "$([ $INT_SIZE -gt 5000 ]; echo $?)" "exam-integration.js has content ($(numfmt --to=iec $INT_SIZE 2>/dev/null || echo ${INT_SIZE} bytes))"

section_header "3. INTEGRATION VERIFICATION"

# Check if script tags are present in index.html
test_check "$(grep -q 'questions-database.js' index.html; echo $?)" "questions-database.js is loaded in index.html"
test_check "$(grep -q 'questions-subjective.js' index.html; echo $?)" "questions-subjective.js is loaded in index.html"
test_check "$(grep -q 'exam-integration.js' index.html; echo $?)" "exam-integration.js is loaded in index.html"

# Check if QUESTIONS array is replaced with dynamic initialization
test_check "$(grep -q 'let QUESTIONS = \[\];' index.html; echo $?)" "QUESTIONS array is initialized as empty (dynamic loading)"
test_check "$(grep -q 'let examManager = null;' index.html; echo $?)" "examManager variable declared"

# Check if initialization code is present
test_check "$(grep -q 'examManager = initializeExamSystem()' index.html; echo $?)" "Exam initialization code present in startExam()"
test_check "$(grep -q 'QUESTIONS = examManager.selectedQuestions' index.html; echo $?)" "QUESTIONS array population code present"

section_header "4. QUESTION DATABASE VALIDATION"

# Count questions in database files
PYTHON_MCQ=$(grep -c '"type": "mcq"' questions-database.js | head -1)
SQL_MCQ=$(grep -c '"type": "mcq"' questions-database.js | tail -1)
info_message "Python MCQ questions found in database: checking structure"
info_message "SQL MCQ questions found in database: checking structure"

# Check for encryption framework
test_check "$(grep -q 'ENCRYPTION_KEY' questions-database.js || grep -q 'ENCRYPTION_KEY' exam-integration.js; echo $?)" "Encryption framework present"
test_check "$(grep -q 'CryptoJS' questions-database.js || grep -q 'CryptoJS' exam-integration.js; echo $?)" "CryptoJS integration present"

# Check for key functions
test_check "$(grep -q 'initializeExamSystem' exam-integration.js; echo $?)" "initializeExamSystem function exists"
test_check "$(grep -q 'ExamQuestionManager' exam-integration.js; echo $?)" "ExamQuestionManager class exists"
test_check "$(grep -q 'shuffleAndSelect' exam-integration.js; echo $?)" "shuffleAndSelect function exists (randomization)"

section_header "5. DOCUMENTATION VALIDATION"

# Check if documentation files exist
test_check "$([ -f "EXAM_SYSTEM_DOCUMENTATION.md" ]; echo $?)" "EXAM_SYSTEM_DOCUMENTATION.md exists"
test_check "$([ -f "IMPLEMENTATION_SUMMARY.md" ]; echo $?)" "IMPLEMENTATION_SUMMARY.md exists"
test_check "$([ -f "QUICK_START_GUIDE.md" ]; echo $?)" "QUICK_START_GUIDE.md exists"
test_check "$([ -f "FILES_CREATED.txt" ]; echo $?)" "FILES_CREATED.txt exists"

section_header "6. CODE QUALITY CHECKS"

# Check for console logging (debugging)
LOG_COUNT=$(grep -c 'console.log.*question' index.html)
info_message "Console logging statements found: $LOG_COUNT (good for debugging)"

# Check for error handling
test_check "$(grep -q 'try {' index.html; echo $?)" "Error handling (try-catch) present"
test_check "$(grep -q 'catch (error)' index.html; echo $?)" "Error catching implemented"

# Check for security features
test_check "$(grep -q 'encrypted' index.html || grep -q 'encrypted' exam-integration.js; echo $?)" "Encryption references present"
test_check "$(grep -q 'decrypt' index.html || grep -q 'decrypt' exam-integration.js; echo $?)" "Decryption logic present"

section_header "7. FINAL SUMMARY"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                           VALIDATION RESULTS                                  ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Tests Run:    ${BLUE}$TOTAL_TESTS${NC}"
echo -e "Tests Passed:       ${GREEN}$PASS_COUNT${NC}"
echo -e "Tests Failed:       ${RED}$FAIL_COUNT${NC}"

SUCCESS_RATE=$((PASS_COUNT * 100 / TOTAL_TESTS))
echo -e "Success Rate:       ${BLUE}$SUCCESS_RATE%${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✅ ALL VALIDATION CHECKS PASSED! ✅                        ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}🎉 Integration Complete!${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Open test-integration.html in your browser to run comprehensive tests"
    echo "  2. Open index.html and start an exam to test the full application"
    echo "  3. Verify random question selection works correctly"
    echo "  4. Check that source view shows only encrypted data"
    echo ""
elif [ $SUCCESS_RATE -ge 80 ]; then
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║                    ⚠️  MOSTLY PASSED WITH WARNINGS  ⚠️                        ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Some tests failed but core functionality should work.${NC}"
    echo "Review the failed tests above and consider fixing them before production deployment."
    echo ""
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                        ❌ VALIDATION FAILED ❌                                ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}Critical tests failed. Please review and fix the issues before proceeding.${NC}"
    echo ""
fi

# Create validation report
REPORT_FILE="validation-report-$(date +%Y%m%d_%H%M%S).txt"
{
    echo "EXAM SYSTEM INTEGRATION VALIDATION REPORT"
    echo "Generated: $(date)"
    echo ""
    echo "Total Tests: $TOTAL_TESTS"
    echo "Passed: $PASS_COUNT"
    echo "Failed: $FAIL_COUNT"
    echo "Success Rate: $SUCCESS_RATE%"
    echo ""
    echo "Status: $([ $FAIL_COUNT -eq 0 ] && echo 'ALL TESTS PASSED' || echo 'SOME TESTS FAILED')"
} > "$REPORT_FILE"

info_message "Validation report saved to: $REPORT_FILE"
echo ""

exit $FAIL_COUNT
