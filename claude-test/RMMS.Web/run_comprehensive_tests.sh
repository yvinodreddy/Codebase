#!/bin/bash

# RMMS Comprehensive Automated Testing Suite
# Version: 1.0
# Date: 2025-10-01

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0

# Results file
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).log"
SUMMARY_FILE="test_summary_$(date +%Y%m%d_%H%M%S).md"

# Function to log test result
log_test() {
    local test_id=$1
    local test_name=$2
    local status=$3
    local message=$4

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if [ "$status" = "PASS" ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo -e "${GREEN}[✓] ${test_id}: ${test_name}${NC}" | tee -a "$RESULTS_FILE"
    elif [ "$status" = "FAIL" ]; then
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo -e "${RED}[✗] ${test_id}: ${test_name}${NC}" | tee -a "$RESULTS_FILE"
        echo -e "    ${RED}Reason: ${message}${NC}" | tee -a "$RESULTS_FILE"
    elif [ "$status" = "WARN" ]; then
        WARNINGS=$((WARNINGS + 1))
        echo -e "${YELLOW}[!] ${test_id}: ${test_name}${NC}" | tee -a "$RESULTS_FILE"
        echo -e "    ${YELLOW}Warning: ${message}${NC}" | tee -a "$RESULTS_FILE"
    fi
}

# Function to print section header
print_section() {
    echo -e "\n${BLUE}========================================${NC}" | tee -a "$RESULTS_FILE"
    echo -e "${BLUE}$1${NC}" | tee -a "$RESULTS_FILE"
    echo -e "${BLUE}========================================${NC}\n" | tee -a "$RESULTS_FILE"
}

# Start testing
echo "RMMS Comprehensive Automated Testing Suite" | tee "$RESULTS_FILE"
echo "Started: $(date)" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

#############################################
# PHASE 1: BUILD VERIFICATION & SMOKE TESTS
#############################################
print_section "PHASE 1: BUILD VERIFICATION & SMOKE TESTS"

# FUNC-SMOKE-001: Application builds successfully
echo "Running: FUNC-SMOKE-001 - Application builds successfully..." | tee -a "$RESULTS_FILE"
if dotnet build RMMS.Web.sln --no-incremental > /dev/null 2>&1; then
    log_test "FUNC-SMOKE-001" "Application builds successfully" "PASS"
else
    log_test "FUNC-SMOKE-001" "Application builds successfully" "FAIL" "Build failed"
fi

# CODE-STAT-002: Check for compiler warnings
echo "Checking: CODE-STAT-002 - Compiler warnings..." | tee -a "$RESULTS_FILE"
BUILD_OUTPUT=$(dotnet build RMMS.Web.sln --no-incremental 2>&1)
WARNING_COUNT=$(echo "$BUILD_OUTPUT" | grep -c "warning" || true)
if [ "$WARNING_COUNT" -eq 0 ]; then
    log_test "CODE-STAT-002" "No compiler warnings" "PASS"
else
    log_test "CODE-STAT-002" "Compiler warnings found" "WARN" "$WARNING_COUNT warnings found"
fi

#############################################
# PHASE 2: SECURITY CODE REVIEW
#############################################
print_section "PHASE 2: SECURITY CODE REVIEW"

# SEC-SQL-005: Verify stored procedure calls use parameters
echo "Checking: SEC-SQL-005 - SQL parameter usage..." | tee -a "$RESULTS_FILE"
STRING_CONCAT=$(grep -r "\"sp_.*\" *+" RMMS.Services/ 2>/dev/null | wc -l)
if [ "$STRING_CONCAT" -eq 0 ]; then
    log_test "SEC-SQL-005" "No string concatenation in SP calls" "PASS"
else
    log_test "SEC-SQL-005" "String concatenation in SP calls detected" "WARN" "Found $STRING_CONCAT instances"
fi

# SEC-AUDIT-002: Check for hardcoded secrets
echo "Checking: SEC-AUDIT-002 - Hardcoded secrets..." | tee -a "$RESULTS_FILE"
HARDCODED_SECRETS=$(grep -r -i "password.*=.*\"" --include="*.cs" RMMS.Web/ RMMS.Services/ 2>/dev/null | grep -v "PasswordHash" | grep -v "//.*password" | wc -l)
if [ "$HARDCODED_SECRETS" -eq 0 ]; then
    log_test "SEC-AUDIT-002" "No hardcoded secrets in C# files" "PASS"
else
    log_test "SEC-AUDIT-002" "Potential hardcoded secrets found" "WARN" "Found $HARDCODED_SECRETS instances - manual review needed"
fi

# SEC-AUDIT-003: HTTPS enforcement check
echo "Checking: SEC-AUDIT-003 - HTTPS enforcement..." | tee -a "$RESULTS_FILE"
if grep -q "UseHttpsRedirection" RMMS.Web/Program.cs; then
    log_test "SEC-AUDIT-003" "HTTPS redirection enabled" "PASS"
else
    log_test "SEC-AUDIT-003" "HTTPS redirection not found" "FAIL" "UseHttpsRedirection() not called in Program.cs"
fi

# SEC-AUDIT-004: Security headers check
echo "Checking: SEC-AUDIT-004 - Security headers..." | tee -a "$RESULTS_FILE"
SECURITY_HEADERS=("X-Frame-Options" "X-Content-Type-Options" "X-XSS-Protection")
HEADERS_FOUND=0
for header in "${SECURITY_HEADERS[@]}"; do
    if grep -q "$header" RMMS.Web/Program.cs; then
        HEADERS_FOUND=$((HEADERS_FOUND + 1))
    fi
done
if [ "$HEADERS_FOUND" -eq ${#SECURITY_HEADERS[@]} ]; then
    log_test "SEC-AUDIT-004" "All security headers configured" "PASS"
else
    log_test "SEC-AUDIT-004" "Missing security headers" "WARN" "Found $HEADERS_FOUND/${#SECURITY_HEADERS[@]} headers"
fi

# SEC-XSS-002: Check for HTML encoding in views
echo "Checking: SEC-XSS-002 - HTML encoding in views..." | tee -a "$RESULTS_FILE"
RAW_HTML=$(grep -r "@Html.Raw" RMMS.Web/Views/ 2>/dev/null | wc -l)
if [ "$RAW_HTML" -eq 0 ]; then
    log_test "SEC-XSS-002" "No @Html.Raw usage (good - prevents XSS)" "PASS"
else
    log_test "SEC-XSS-002" "Raw HTML rendering found" "WARN" "Found $RAW_HTML @Html.Raw usages - review for XSS"
fi

# SEC-CSRF-004: Check for ValidateAntiForgeryToken
echo "Checking: SEC-CSRF-004 - Anti-forgery token validation..." | tee -a "$RESULTS_FILE"
POST_METHODS=$(grep -r "\[HttpPost\]" RMMS.Web/Controllers/ 2>/dev/null | wc -l)
ANTIFORGERY=$(grep -r "ValidateAntiForgeryToken" RMMS.Web/Controllers/ 2>/dev/null | wc -l)
if [ "$POST_METHODS" -gt 0 ] && [ "$ANTIFORGERY" -gt 0 ]; then
    log_test "SEC-CSRF-004" "Anti-forgery protection implemented" "PASS"
else
    log_test "SEC-CSRF-004" "Anti-forgery protection" "WARN" "Found $ANTIFORGERY tokens for $POST_METHODS POST methods"
fi

#############################################
# PHASE 3: CODE QUALITY CHECKS
#############################################
print_section "PHASE 3: CODE QUALITY CHECKS"

# CODE-STAT-003: Check for code duplication (basic check)
echo "Checking: CODE-STAT-003 - Code duplication..." | tee -a "$RESULTS_FILE"
# Simple duplicate line check (this is basic, real tools like SonarQube are better)
DUPLICATE_LINES=$(find RMMS.Services/ -name "*.cs" -exec cat {} \; 2>/dev/null | sort | uniq -d | wc -l)
if [ "$DUPLICATE_LINES" -lt 100 ]; then
    log_test "CODE-STAT-003" "Minimal code duplication detected" "PASS"
else
    log_test "CODE-STAT-003" "Code duplication detected" "WARN" "$DUPLICATE_LINES duplicate lines found"
fi

# CODE-MEM-001: Check for IDisposable pattern
echo "Checking: CODE-MEM-001 - Disposable pattern usage..." | tee -a "$RESULTS_FILE"
USING_STATEMENTS=$(grep -r "using.*(" RMMS.Services/*.cs 2>/dev/null | wc -l)
DISPOSABLE_TYPES=$(grep -r ": IDisposable" RMMS.Services/*.cs 2>/dev/null | wc -l)
if [ "$USING_STATEMENTS" -gt 0 ]; then
    log_test "CODE-MEM-001" "Using statements for resource management" "PASS"
else
    log_test "CODE-MEM-001" "Resource management patterns" "WARN" "Found $USING_STATEMENTS using statements, $DISPOSABLE_TYPES IDisposable types"
fi

#############################################
# PHASE 4: CONFIGURATION VALIDATION
#############################################
print_section "PHASE 4: CONFIGURATION VALIDATION"

# CONF-001: appsettings.json exists
echo "Checking: CONF-001 - Configuration files..." | tee -a "$RESULTS_FILE"
if [ -f "RMMS.Web/appsettings.json" ] && [ -f "RMMS.Web/appsettings.Development.json" ]; then
    log_test "CONF-001" "Configuration files exist" "PASS"
else
    log_test "CONF-001" "Configuration files missing" "FAIL" "appsettings.json or appsettings.Development.json not found"
fi

# CONF-002: Check for connection string
echo "Checking: CONF-002 - Connection string configuration..." | tee -a "$RESULTS_FILE"
if grep -q "ConnectionStrings" RMMS.Web/appsettings.json; then
    log_test "CONF-002" "Connection string configured" "PASS"
else
    log_test "CONF-002" "Connection string missing" "FAIL" "No ConnectionStrings section in appsettings.json"
fi

# CONF-004: Logging configuration
echo "Checking: CONF-004 - Logging configuration..." | tee -a "$RESULTS_FILE"
if grep -q "Serilog\|Logging" RMMS.Web/appsettings.json; then
    log_test "CONF-004" "Logging configured" "PASS"
else
    log_test "CONF-004" "Logging configuration" "WARN" "Logging configuration may not be complete"
fi

# CONF-ENV-001: Check .NET version
echo "Checking: CONF-ENV-001 - .NET runtime version..." | tee -a "$RESULTS_FILE"
DOTNET_VERSION=$(dotnet --version)
if [[ "$DOTNET_VERSION" == 8.* ]]; then
    log_test "CONF-ENV-001" ".NET 8.0 runtime detected" "PASS"
else
    log_test "CONF-ENV-001" ".NET runtime version" "WARN" "Version $DOTNET_VERSION (expected 8.x)"
fi

#############################################
# PHASE 5: FILE STRUCTURE & ORGANIZATION
#############################################
print_section "PHASE 5: FILE STRUCTURE & ORGANIZATION"

# Check for critical directories
echo "Checking: File structure validation..." | tee -a "$RESULTS_FILE"
REQUIRED_DIRS=("RMMS.Web/Controllers" "RMMS.Web/Views" "RMMS.Web/wwwroot" "RMMS.Services" "RMMS.Models" "RMMS.DataAccess")
DIRS_FOUND=0
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        DIRS_FOUND=$((DIRS_FOUND + 1))
    fi
done
if [ "$DIRS_FOUND" -eq ${#REQUIRED_DIRS[@]} ]; then
    log_test "FILE-STRUCT-001" "All required directories present" "PASS"
else
    log_test "FILE-STRUCT-001" "Directory structure" "FAIL" "Found $DIRS_FOUND/${#REQUIRED_DIRS[@]} required directories"
fi

# Check for Views
echo "Checking: View files..." | tee -a "$RESULTS_FILE"
VIEW_COUNT=$(find RMMS.Web/Views -name "*.cshtml" 2>/dev/null | wc -l)
if [ "$VIEW_COUNT" -gt 10 ]; then
    log_test "FILE-VIEWS-001" "View files present ($VIEW_COUNT views)" "PASS"
else
    log_test "FILE-VIEWS-001" "View files" "WARN" "Only $VIEW_COUNT views found"
fi

# Check for Controllers
echo "Checking: Controller files..." | tee -a "$RESULTS_FILE"
CONTROLLER_COUNT=$(find RMMS.Web/Controllers -name "*Controller.cs" 2>/dev/null | wc -l)
if [ "$CONTROLLER_COUNT" -gt 5 ]; then
    log_test "FILE-CTRL-001" "Controller files present ($CONTROLLER_COUNT controllers)" "PASS"
else
    log_test "FILE-CTRL-001" "Controller files" "WARN" "Only $CONTROLLER_COUNT controllers found"
fi

# Check for Models
echo "Checking: Model files..." | tee -a "$RESULTS_FILE"
MODEL_COUNT=$(find RMMS.Models -name "*.cs" 2>/dev/null | grep -v "obj\|bin" | wc -l)
if [ "$MODEL_COUNT" -gt 5 ]; then
    log_test "FILE-MODEL-001" "Model files present ($MODEL_COUNT models)" "PASS"
else
    log_test "FILE-MODEL-001" "Model files" "WARN" "Only $MODEL_COUNT models found"
fi

#############################################
# PHASE 6: DEPENDENCY & PACKAGE CHECKS
#############################################
print_section "PHASE 6: DEPENDENCY & PACKAGE CHECKS"

# SEC-AUDIT-001: Check for vulnerable packages
echo "Checking: SEC-AUDIT-001 - Vulnerable packages..." | tee -a "$RESULTS_FILE"
VULNERABLE_PACKAGES=$(dotnet list package --vulnerable 2>&1 | grep -c "has the following vulnerable packages" || true)
if [ "$VULNERABLE_PACKAGES" -eq 0 ]; then
    log_test "SEC-AUDIT-001" "No known vulnerable packages" "PASS"
else
    log_test "SEC-AUDIT-001" "Vulnerable packages detected" "FAIL" "Run 'dotnet list package --vulnerable' for details"
fi

# Check for outdated packages
echo "Checking: Package updates available..." | tee -a "$RESULTS_FILE"
OUTDATED_PACKAGES=$(dotnet list package --outdated 2>&1 | grep -c ">" || true)
if [ "$OUTDATED_PACKAGES" -eq 0 ]; then
    log_test "PKG-UPDATE-001" "All packages up to date" "PASS"
else
    log_test "PKG-UPDATE-001" "Outdated packages found" "WARN" "$OUTDATED_PACKAGES packages can be updated"
fi

#############################################
# PHASE 7: STATIC FILE CHECKS
#############################################
print_section "PHASE 7: STATIC FILE CHECKS"

# Check for CSS files
echo "Checking: CSS files..." | tee -a "$RESULTS_FILE"
CSS_COUNT=$(find RMMS.Web/wwwroot/css -name "*.css" 2>/dev/null | wc -l)
if [ "$CSS_COUNT" -gt 0 ]; then
    log_test "STATIC-CSS-001" "CSS files present ($CSS_COUNT files)" "PASS"
else
    log_test "STATIC-CSS-001" "CSS files missing" "FAIL" "No CSS files found in wwwroot/css"
fi

# Check for JavaScript files
echo "Checking: JavaScript files..." | tee -a "$RESULTS_FILE"
JS_COUNT=$(find RMMS.Web/wwwroot/js -name "*.js" 2>/dev/null | wc -l)
if [ "$JS_COUNT" -gt 0 ]; then
    log_test "STATIC-JS-001" "JavaScript files present ($JS_COUNT files)" "PASS"
else
    log_test "STATIC-JS-001" "JavaScript files" "WARN" "No JavaScript files found in wwwroot/js"
fi

# Check for microsoft-fluent.css (UI Enhancement requirement)
echo "Checking: Microsoft Fluent Design CSS..." | tee -a "$RESULTS_FILE"
if [ -f "RMMS.Web/wwwroot/css/microsoft-fluent.css" ]; then
    log_test "UI-FLUENT-001" "Microsoft Fluent Design CSS present" "PASS"
else
    log_test "UI-FLUENT-001" "Microsoft Fluent Design CSS missing" "FAIL" "microsoft-fluent.css not found"
fi

# Check for responsive.css
echo "Checking: Responsive CSS..." | tee -a "$RESULTS_FILE"
if [ -f "RMMS.Web/wwwroot/css/responsive.css" ]; then
    log_test "UI-RESP-001" "Responsive CSS present" "PASS"
else
    log_test "UI-RESP-001" "Responsive CSS missing" "FAIL" "responsive.css not found"
fi

# Check for DataTables CSS
echo "Checking: DataTables custom CSS..." | tee -a "$RESULTS_FILE"
if [ -f "RMMS.Web/wwwroot/css/datatables-custom.css" ]; then
    log_test "UI-DT-001" "DataTables custom CSS present" "PASS"
else
    log_test "UI-DT-001" "DataTables custom CSS missing" "FAIL" "datatables-custom.css not found"
fi

# Check for site-enhanced.js
echo "Checking: Enhanced JavaScript..." | tee -a "$RESULTS_FILE"
if [ -f "RMMS.Web/wwwroot/js/site-enhanced.js" ]; then
    log_test "UI-JS-001" "Enhanced JavaScript present" "PASS"
else
    log_test "UI-JS-001" "Enhanced JavaScript missing" "FAIL" "site-enhanced.js not found"
fi

#############################################
# GENERATE SUMMARY
#############################################
print_section "TEST SUMMARY"

echo "" | tee -a "$RESULTS_FILE"
echo "Total Tests Run: $TOTAL_TESTS" | tee -a "$RESULTS_FILE"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}" | tee -a "$RESULTS_FILE"
echo -e "${RED}Failed: $FAILED_TESTS${NC}" | tee -a "$RESULTS_FILE"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

PASS_RATE=$(( PASSED_TESTS * 100 / TOTAL_TESTS ))
echo "Pass Rate: ${PASS_RATE}%" | tee -a "$RESULTS_FILE"

if [ "$FAILED_TESTS" -eq 0 ]; then
    echo -e "\n${GREEN}✓ ALL CRITICAL TESTS PASSED${NC}" | tee -a "$RESULTS_FILE"
    EXIT_CODE=0
else
    echo -e "\n${RED}✗ SOME TESTS FAILED - REVIEW REQUIRED${NC}" | tee -a "$RESULTS_FILE"
    EXIT_CODE=1
fi

echo "" | tee -a "$RESULTS_FILE"
echo "Completed: $(date)" | tee -a "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" | tee -a "$RESULTS_FILE"

# Generate Markdown Summary
cat > "$SUMMARY_FILE" << EOF
# RMMS Automated Test Report

**Date**: $(date)
**Test Suite Version**: 1.0

## Executive Summary

- **Total Tests**: $TOTAL_TESTS
- **Passed**: $PASSED_TESTS (${PASS_RATE}%)
- **Failed**: $FAILED_TESTS
- **Warnings**: $WARNINGS

## Test Coverage

### Phase 1: Build Verification ✓
- Application builds successfully
- Compiler warnings checked

### Phase 2: Security Review ✓
- SQL injection protection
- Hardcoded secrets scan
- HTTPS enforcement
- Security headers
- XSS protection
- CSRF protection

### Phase 3: Code Quality ✓
- Code duplication analysis
- Resource management patterns

### Phase 4: Configuration ✓
- Configuration files validation
- Connection string verification
- Logging configuration
- .NET runtime version

### Phase 5: File Structure ✓
- Directory structure
- View files
- Controller files
- Model files

### Phase 6: Dependencies ✓
- Vulnerable package scan
- Package update check

### Phase 7: Static Assets ✓
- CSS files
- JavaScript files
- UI enhancement files

## Production Readiness Assessment

EOF

if [ "$FAILED_TESTS" -eq 0 ]; then
    cat >> "$SUMMARY_FILE" << EOF
### Status: ✅ **READY FOR NEXT PHASE**

All automated tests in Phase 1 (Foundation) have passed. The application is ready to proceed to:
- Phase 2: Functional Testing (manual/integration tests)
- Phase 3: Performance Testing
- Phase 4: UAT

**Recommendation**: Proceed with manual testing and user acceptance testing.

EOF
else
    cat >> "$SUMMARY_FILE" << EOF
### Status: ❌ **NOT READY**

$FAILED_TESTS critical test(s) failed. Please review and fix before proceeding.

**Recommendation**: Fix all failing tests before moving to next phase.

EOF
fi

cat >> "$SUMMARY_FILE" << EOF
## Next Steps

1. Review detailed results in: \`$RESULTS_FILE\`
2. Address any warnings or failures
3. Run Phase 2 functional tests (requires application runtime)
4. Conduct performance testing
5. Execute user acceptance testing

## Notes

- This is an automated test suite covering ~30% of the full test specification
- Manual testing required for: Usability, Performance, Security penetration, UAT
- Database connectivity tests require running database
- Runtime tests require application startup

---

**Report generated by**: RMMS Automated Testing Suite v1.0
**For detailed logs**: See $RESULTS_FILE
EOF

echo -e "\n${BLUE}Summary report saved to: $SUMMARY_FILE${NC}"

exit $EXIT_CODE
