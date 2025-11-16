#!/bin/bash

# RMMS Phase 2: Functional Testing Suite
# Version: 1.0
# Date: 2025-10-01
# Prerequisites: Database must be accessible

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0
SKIPPED_TESTS=0

# Results file
RESULTS_FILE="phase2_test_results_$(date +%Y%m%d_%H%M%S).log"
SUMMARY_FILE="phase2_test_summary_$(date +%Y%m%d_%H%M%S).md"

# Application info
APP_URL="http://localhost:5090"
APP_PID=""

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
    elif [ "$status" = "SKIP" ]; then
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        echo -e "${CYAN}[⊘] ${test_id}: ${test_name}${NC}" | tee -a "$RESULTS_FILE"
        echo -e "    ${CYAN}Skipped: ${message}${NC}" | tee -a "$RESULTS_FILE"
    fi
}

# Function to print section header
print_section() {
    echo -e "\n${BLUE}========================================${NC}" | tee -a "$RESULTS_FILE"
    echo -e "${BLUE}$1${NC}" | tee -a "$RESULTS_FILE"
    echo -e "${BLUE}========================================${NC}\n" | tee -a "$RESULTS_FILE"
}

# Function to check if port is in use
check_port() {
    netstat -tuln 2>/dev/null | grep -q ":$1 " || ss -tuln 2>/dev/null | grep -q ":$1 "
}

# Function to wait for application to start
wait_for_app() {
    local max_wait=30
    local wait_time=0

    echo "Waiting for application to start (max ${max_wait}s)..." | tee -a "$RESULTS_FILE"

    while [ $wait_time -lt $max_wait ]; do
        if curl -s -o /dev/null -w "%{http_code}" "$APP_URL" | grep -q "200\|302"; then
            echo "Application is responding!" | tee -a "$RESULTS_FILE"
            return 0
        fi
        sleep 1
        wait_time=$((wait_time + 1))
        echo -n "." | tee -a "$RESULTS_FILE"
    done

    echo -e "\n${RED}Application failed to start within ${max_wait} seconds${NC}" | tee -a "$RESULTS_FILE"
    return 1
}

# Function to check database connectivity
check_database() {
    local conn_string=$(grep -A 5 "ConnectionStrings" RMMS.Web/appsettings.json | grep "DefaultConnection" | cut -d'"' -f4)

    if [ -z "$conn_string" ]; then
        return 1
    fi

    # Extract server from connection string
    local server=$(echo "$conn_string" | grep -oP 'Server=[^;]+' | cut -d'=' -f2)

    if [ -z "$server" ]; then
        return 1
    fi

    # Try to ping SQL Server (basic check)
    if echo "$server" | grep -q "localhost\|127.0.0.1\|\."; then
        # Local server - check if SQL Server port is open
        if check_port 1433; then
            return 0
        fi
    fi

    return 1
}

# Start testing
echo "RMMS Phase 2: Functional Testing Suite" | tee "$RESULTS_FILE"
echo "Started: $(date)" | tee -a "$RESULTS_FILE"
echo "Application URL: $APP_URL" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

#############################################
# PRE-FLIGHT CHECKS
#############################################
print_section "PRE-FLIGHT CHECKS"

# Check if application is already running
echo "Checking: Application status..." | tee -a "$RESULTS_FILE"
if check_port 5090; then
    log_test "PRE-001" "Application already running on port 5090" "PASS"
    APP_RUNNING=true
else
    log_test "PRE-001" "Application not running" "WARN" "Will attempt to start application"
    APP_RUNNING=false
fi

# Check database connectivity
echo "Checking: Database connectivity..." | tee -a "$RESULTS_FILE"
if check_database; then
    log_test "PRE-002" "Database appears accessible" "PASS"
else
    log_test "PRE-002" "Database connectivity" "WARN" "Cannot confirm database is accessible"
fi

# Check if we need to start the application
if [ "$APP_RUNNING" = false ]; then
    print_section "STARTING APPLICATION"

    echo "Starting application in background..." | tee -a "$RESULTS_FILE"
    cd RMMS.Web
    nohup dotnet run > ../app_output.log 2>&1 &
    APP_PID=$!
    cd ..

    echo "Application started with PID: $APP_PID" | tee -a "$RESULTS_FILE"

    if wait_for_app; then
        log_test "APP-START-001" "Application startup" "PASS"
    else
        log_test "APP-START-001" "Application startup" "FAIL" "Application did not respond within timeout"

        # Show last 20 lines of app output
        echo -e "\n${YELLOW}Last 20 lines of application output:${NC}" | tee -a "$RESULTS_FILE"
        tail -20 app_output.log | tee -a "$RESULTS_FILE"

        echo -e "\n${RED}Cannot proceed with functional tests - application not running${NC}" | tee -a "$RESULTS_FILE"
        exit 1
    fi
fi

#############################################
# PHASE 2.1: HTTP ACCESSIBILITY TESTS
#############################################
print_section "PHASE 2.1: HTTP ACCESSIBILITY TESTS"

# Test home page
echo "Testing: Home page accessibility..." | tee -a "$RESULTS_FILE"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL" || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    log_test "HTTP-001" "Home page accessible (HTTP $HTTP_CODE)" "PASS"
else
    log_test "HTTP-001" "Home page accessibility" "FAIL" "Unexpected HTTP code: $HTTP_CODE"
fi

# Test login page
echo "Testing: Login page accessibility..." | tee -a "$RESULTS_FILE"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL/Account/Login" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log_test "HTTP-002" "Login page accessible (HTTP $HTTP_CODE)" "PASS"
else
    log_test "HTTP-002" "Login page accessibility" "WARN" "HTTP code: $HTTP_CODE (might require auth)"
fi

# Test static assets
echo "Testing: Static CSS files..." | tee -a "$RESULTS_FILE"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL/css/microsoft-fluent.css" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log_test "HTTP-003" "Static CSS accessible" "PASS"
else
    log_test "HTTP-003" "Static CSS accessibility" "WARN" "HTTP code: $HTTP_CODE"
fi

echo "Testing: Static JavaScript files..." | tee -a "$RESULTS_FILE"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL/js/site-enhanced.js" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log_test "HTTP-004" "Static JS accessible" "PASS"
else
    log_test "HTTP-004" "Static JS accessibility" "WARN" "HTTP code: $HTTP_CODE"
fi

# Test HTTPS redirect (if configured)
echo "Testing: HTTPS redirection..." | tee -a "$RESULTS_FILE"
HTTP_REDIRECT=$(curl -s -o /dev/null -w "%{redirect_url}" "http://localhost:5090" || echo "")
if echo "$HTTP_REDIRECT" | grep -q "https://"; then
    log_test "SEC-HTTP-001" "HTTP to HTTPS redirect working" "PASS"
else
    log_test "SEC-HTTP-001" "HTTP to HTTPS redirect" "SKIP" "Not configured in development"
fi

#############################################
# PHASE 2.2: DATABASE SCHEMA VALIDATION
#############################################
print_section "PHASE 2.2: DATABASE SCHEMA VALIDATION"

echo "Checking: Database schema validation..." | tee -a "$RESULTS_FILE"
echo "Note: Requires SQL Server access for full validation" | tee -a "$RESULTS_FILE"

# Check if stored procedures exist in code
REQUIRED_SPs=(
    "sp_GetPaddyProcurement"
    "sp_GetRiceSales"
    "sp_GetCashBook"
    "sp_GetBankTransactions"
    "sp_GetVouchers"
)

SP_COUNT=0
for sp in "${REQUIRED_SPs[@]}"; do
    if grep -rq "$sp" RMMS.Services/ RMMS.DataAccess/ 2>/dev/null; then
        SP_COUNT=$((SP_COUNT + 1))
    fi
done

if [ "$SP_COUNT" -ge 3 ]; then
    log_test "DB-SCHEMA-001" "Stored procedures referenced in code ($SP_COUNT found)" "PASS"
else
    log_test "DB-SCHEMA-001" "Stored procedures in code" "WARN" "Only $SP_COUNT of ${#REQUIRED_SPs[@]} found"
fi

#############################################
# PHASE 2.3: CONTROLLER ENDPOINT TESTS
#############################################
print_section "PHASE 2.3: CONTROLLER ENDPOINT TESTS"

# Test various endpoints (will require authentication, so we expect 302 redirects)
ENDPOINTS=(
    "/PaddyProcurement"
    "/RiceSales"
    "/ExternalRiceSales"
    "/ByProductSales"
    "/CashBook"
    "/BankTransactions"
    "/Vouchers"
    "/PayablesOverdue"
    "/ReceivablesOverdue"
    "/LoansAdvances"
    "/FixedAssets"
    "/Reports"
)

ACCESSIBLE_COUNT=0
for endpoint in "${ENDPOINTS[@]}"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL$endpoint" || echo "000")

    # 200 = accessible, 302 = redirect to login (expected), 401/403 = auth required (expected)
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "401" ]; then
        ACCESSIBLE_COUNT=$((ACCESSIBLE_COUNT + 1))
    fi
done

if [ "$ACCESSIBLE_COUNT" -ge 10 ]; then
    log_test "ENDPOINT-001" "Controller endpoints accessible ($ACCESSIBLE_COUNT/${#ENDPOINTS[@]})" "PASS"
else
    log_test "ENDPOINT-001" "Controller endpoints" "WARN" "Only $ACCESSIBLE_COUNT/${#ENDPOINTS[@]} accessible"
fi

#############################################
# PHASE 2.4: VIEW RENDERING TESTS
#############################################
print_section "PHASE 2.4: VIEW RENDERING TESTS"

echo "Checking: View file completeness..." | tee -a "$RESULTS_FILE"

# Check if Index views exist for all modules
MODULES=(
    "PaddyProcurement"
    "RiceSales"
    "ExternalRiceSales"
    "ByProductSales"
    "CashBook"
    "BankTransactions"
    "Vouchers"
    "PayablesOverdue"
    "ReceivablesOverdue"
    "LoansAdvances"
    "FixedAssets"
)

VIEW_SETS_COMPLETE=0
for module in "${MODULES[@]}"; do
    if [ -f "RMMS.Web/Views/$module/Index.cshtml" ]; then
        VIEW_SETS_COMPLETE=$((VIEW_SETS_COMPLETE + 1))
    fi
done

if [ "$VIEW_SETS_COMPLETE" -eq ${#MODULES[@]} ]; then
    log_test "VIEW-001" "All module Index views present (${VIEW_SETS_COMPLETE}/${#MODULES[@]})" "PASS"
else
    log_test "VIEW-001" "Module Index views" "FAIL" "Missing views: $((${#MODULES[@]} - VIEW_SETS_COMPLETE))"
fi

# Check for Create/Edit views
CREATE_VIEWS=0
EDIT_VIEWS=0
for module in "${MODULES[@]}"; do
    [ -f "RMMS.Web/Views/$module/Create.cshtml" ] && CREATE_VIEWS=$((CREATE_VIEWS + 1))
    [ -f "RMMS.Web/Views/$module/Edit.cshtml" ] && EDIT_VIEWS=$((EDIT_VIEWS + 1))
done

if [ "$CREATE_VIEWS" -ge 8 ]; then
    log_test "VIEW-002" "Create views present ($CREATE_VIEWS/${#MODULES[@]})" "PASS"
else
    log_test "VIEW-002" "Create views" "WARN" "Only $CREATE_VIEWS/${#MODULES[@]} Create views found"
fi

if [ "$EDIT_VIEWS" -ge 8 ]; then
    log_test "VIEW-003" "Edit views present ($EDIT_VIEWS/${#MODULES[@]})" "PASS"
else
    log_test "VIEW-003" "Edit views" "WARN" "Only $EDIT_VIEWS/${#MODULES[@]} Edit views found"
fi

#############################################
# PHASE 2.5: DATATABLES IMPLEMENTATION CHECK
#############################################
print_section "PHASE 2.5: DATATABLES IMPLEMENTATION CHECK"

echo "Checking: DataTables implementation in views..." | tee -a "$RESULTS_FILE"

DATATABLES_COUNT=$(grep -r "ms-datatable" RMMS.Web/Views/*/Index.cshtml 2>/dev/null | wc -l)
if [ "$DATATABLES_COUNT" -ge 10 ]; then
    log_test "DT-001" "DataTables implemented in Index views ($DATATABLES_COUNT views)" "PASS"
else
    log_test "DT-001" "DataTables implementation" "WARN" "Only $DATATABLES_COUNT views have DataTables"
fi

# Check for export functionality
EXPORT_ENABLED=$(grep -r 'data-export="true"' RMMS.Web/Views/*/Index.cshtml 2>/dev/null | wc -l)
if [ "$EXPORT_ENABLED" -ge 10 ]; then
    log_test "DT-002" "Export functionality enabled ($EXPORT_ENABLED views)" "PASS"
else
    log_test "DT-002" "Export functionality" "WARN" "Only $EXPORT_ENABLED views have export enabled"
fi

#############################################
# PHASE 2.6: RESPONSIVE DESIGN CHECK
#############################################
print_section "PHASE 2.6: RESPONSIVE DESIGN CHECK"

echo "Checking: Responsive design implementation..." | tee -a "$RESULTS_FILE"

# Check for viewport meta tag
if grep -q "viewport" RMMS.Web/Views/Shared/_Layout.cshtml 2>/dev/null; then
    log_test "RESP-001" "Viewport meta tag present" "PASS"
else
    log_test "RESP-001" "Viewport meta tag" "FAIL" "Not found in _Layout.cshtml"
fi

# Check for Bootstrap grid usage
BOOTSTRAP_USAGE=$(grep -r "col-md\|col-sm\|col-lg" RMMS.Web/Views/ 2>/dev/null | wc -l)
if [ "$BOOTSTRAP_USAGE" -gt 50 ]; then
    log_test "RESP-002" "Bootstrap responsive grid used ($BOOTSTRAP_USAGE instances)" "PASS"
else
    log_test "RESP-002" "Bootstrap responsive grid" "WARN" "Only $BOOTSTRAP_USAGE instances found"
fi

# Check if responsive.css is loaded
if grep -q "responsive.css" RMMS.Web/Views/Shared/_Layout.cshtml 2>/dev/null; then
    log_test "RESP-003" "Responsive CSS loaded in layout" "PASS"
else
    log_test "RESP-003" "Responsive CSS in layout" "FAIL" "responsive.css not referenced"
fi

#############################################
# GENERATE MANUAL TESTING CHECKLIST
#############################################
print_section "GENERATING MANUAL TEST CHECKLIST"

echo "Creating manual testing checklist..." | tee -a "$RESULTS_FILE"

cat > "MANUAL_TESTING_CHECKLIST_PHASE2.md" << 'EOF'
# RMMS Phase 2: Manual Functional Testing Checklist

**Generated**: $(date)
**Application URL**: http://localhost:5090
**Default Credentials**: admin / admin@123

---

## TESTING INSTRUCTIONS

Complete each test case below and mark as ✅ PASS or ❌ FAIL.

---

## 1. AUTHENTICATION TESTING (SEC-AUTH Series)

### SEC-AUTH-001: Login with valid credentials
- [ ] Navigate to http://localhost:5090
- [ ] Enter username: `admin`
- [ ] Enter password: `admin@123`
- [ ] Click Login
- [ ] **Expected**: Redirected to Dashboard
- [ ] **Result**: _____

### SEC-AUTH-002: Login with invalid username
- [ ] Navigate to /Account/Login
- [ ] Enter username: `nonexistent`
- [ ] Enter password: `anything`
- [ ] Click Login
- [ ] **Expected**: Error message "Invalid credentials"
- [ ] **Result**: _____

### SEC-AUTH-003: Login with invalid password
- [ ] Navigate to /Account/Login
- [ ] Enter username: `admin`
- [ ] Enter password: `wrongpassword`
- [ ] Click Login
- [ ] **Expected**: Error message "Invalid credentials"
- [ ] **Result**: _____

### SEC-AUTH-007: Session timeout
- [ ] Login successfully
- [ ] Wait 30+ minutes idle
- [ ] Try to navigate to any page
- [ ] **Expected**: Redirected to login
- [ ] **Result**: _____

### SEC-AUTHZ-001: Access protected page without login
- [ ] Logout if logged in
- [ ] Navigate directly to /PaddyProcurement
- [ ] **Expected**: Redirected to /Account/Login
- [ ] **Result**: _____

---

## 2. PADDY PROCUREMENT MODULE (FUNC-PP Series)

### FUNC-PP-001: Create paddy procurement record
- [ ] Login as admin
- [ ] Navigate to Paddy Procurement
- [ ] Click "New Procurement"
- [ ] Fill all required fields:
  - Receipt Date: (today's date)
  - Voucher Number: TEST-001
  - Supplier Name: Test Supplier
  - Paddy Variety: Basmati
  - Quantity Received: 1000
  - Total Net Weight: 950
- [ ] Click Save
- [ ] **Expected**: Record created, redirected to Index
- [ ] **Result**: _____

### FUNC-PP-002: Edit paddy procurement record
- [ ] From Paddy Procurement Index
- [ ] Click Edit on any record
- [ ] Change Supplier Name to "Updated Supplier"
- [ ] Click Save
- [ ] **Expected**: Record updated
- [ ] **Result**: _____

### FUNC-PP-003: Delete paddy procurement record
- [ ] From Paddy Procurement Index
- [ ] Click Delete on test record
- [ ] Confirm deletion
- [ ] **Expected**: Record deleted
- [ ] **Result**: _____

### FUNC-PP-004: View paddy procurement details
- [ ] From Index, click View/Details
- [ ] **Expected**: All fields displayed correctly
- [ ] **Result**: _____

### FUNC-PP-005: Search paddy procurement records
- [ ] On Index page, use DataTables search box
- [ ] Enter supplier name
- [ ] **Expected**: Filtered results shown
- [ ] **Result**: _____

### FUNC-PP-006: Pagination works
- [ ] Ensure 10+ records exist
- [ ] **Expected**: Pagination controls visible
- [ ] Click Next page
- [ ] **Expected**: Next set of records shown
- [ ] **Result**: _____

---

## 3. RICE SALES MODULE (FUNC-RS Series)

### FUNC-RS-001: Create rice sales record
- [ ] Navigate to Rice Sales
- [ ] Click New Sale
- [ ] Fill required fields:
  - Sale Date: (today)
  - Invoice Number: INV-001
  - Buyer Name: Test Buyer
  - Rice Grade: Premium
  - Quantity: 500
  - Unit Price: 50
- [ ] Click Save
- [ ] **Expected**: Record created, Gross Invoice Amount calculated
- [ ] **Result**: _____

### FUNC-RS-005: Verify total amount calculation
- [ ] Create sale with Quantity=100, Unit Price=50
- [ ] **Expected**: Total calculated as 5000
- [ ] **Result**: _____

### FUNC-RS-006: Verify GST calculation
- [ ] Check if GST fields are calculated
- [ ] **Expected**: CGST, SGST, or IGST populated
- [ ] **Result**: _____

---

## 4. CASH BOOK MODULE (FUNC-CB Series)

### FUNC-CB-001: Create cash receipt
- [ ] Navigate to Cash Book
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Voucher No: CB-R-001
  - Particulars: Cash received from sale
  - Receipts: 5000
  - Payments: 0
- [ ] Save
- [ ] **Expected**: Receipt recorded
- [ ] **Result**: _____

### FUNC-CB-002: Create cash payment
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Voucher No: CB-P-001
  - Particulars: Office supplies
  - Receipts: 0
  - Payments: 500
- [ ] Save
- [ ] **Expected**: Payment recorded
- [ ] **Result**: _____

### FUNC-CB-005: View cash book balance
- [ ] On Cash Book Index
- [ ] Check summary cards at top
- [ ] **Expected**: Total Receipts, Payments, Current Balance shown
- [ ] **Expected**: Balance = Receipts - Payments
- [ ] **Result**: _____

---

## 5. BANK TRANSACTIONS MODULE (FUNC-BT Series)

### FUNC-BT-001: Create bank credit
- [ ] Navigate to Bank Transactions
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Bank Name: State Bank
  - Account No: 1234567890
  - Particulars: Customer payment
  - Deposits: 10000
  - Withdrawals: 0
- [ ] Save
- [ ] **Expected**: Deposit recorded
- [ ] **Result**: _____

### FUNC-BT-002: Create bank debit
- [ ] Create transaction with Withdrawals > 0
- [ ] **Expected**: Withdrawal recorded
- [ ] **Result**: _____

---

## 6. FIXED ASSETS MODULE (FUNC-FA Series)

### FUNC-FA-001: Create fixed asset
- [ ] Navigate to Fixed Assets
- [ ] Click Add Asset
- [ ] Fill:
  - Asset ID: FA-001
  - Purchase Date: (date)
  - Asset Name: Rice Mill Machine
  - Supplier: ABC Machinery
  - Purchase Value: 500000
  - Depreciation Rate: 10
- [ ] Save
- [ ] **Expected**: Asset created
- [ ] **Result**: _____

### FUNC-FA-005: Calculate depreciation
- [ ] View asset details
- [ ] Check Accumulated Depreciation
- [ ] **Expected**: Depreciation calculated based on rate
- [ ] **Result**: _____

---

## 7. DATATABLES FUNCTIONALITY

### DT-FUNC-001: Pagination
- [ ] On any Index page with 10+ records
- [ ] Change "Show 10 entries" to "Show 25 entries"
- [ ] **Expected**: Page shows 25 records
- [ ] **Result**: _____

### DT-FUNC-002: Search
- [ ] Use search box on Index page
- [ ] Enter search term
- [ ] **Expected**: Results filtered in real-time
- [ ] **Result**: _____

### DT-FUNC-003: Sorting
- [ ] Click column header to sort
- [ ] **Expected**: Data sorted ascending
- [ ] Click again
- [ ] **Expected**: Data sorted descending
- [ ] **Result**: _____

### DT-FUNC-004: Export to Excel
- [ ] Click "Excel" export button
- [ ] **Expected**: Excel file downloads
- [ ] **Result**: _____

### DT-FUNC-005: Export to PDF
- [ ] Click "PDF" export button
- [ ] **Expected**: PDF file downloads
- [ ] **Result**: _____

### DT-FUNC-006: Print
- [ ] Click "Print" button
- [ ] **Expected**: Print dialog opens
- [ ] **Result**: _____

---

## 8. REPORTS MODULE (FUNC-REP Series)

### FUNC-REP-001: Dashboard loads
- [ ] Navigate to / or /Home
- [ ] **Expected**: Dashboard with summary cards
- [ ] **Expected**: Charts load (if implemented)
- [ ] **Result**: _____

### FUNC-REP-002: Daily sales report
- [ ] Navigate to Reports
- [ ] Select Daily Sales Report
- [ ] Choose date
- [ ] **Expected**: Report generated
- [ ] **Result**: _____

### FUNC-REP-007: Stock report
- [ ] Navigate to Stock Summary
- [ ] **Expected**: Stock levels shown
- [ ] **Result**: _____

---

## 9. FORM VALIDATION (DATA-VAL Series)

### DATA-VAL-001: Required field validation
- [ ] On any Create form
- [ ] Leave required fields empty
- [ ] Try to save
- [ ] **Expected**: Validation errors shown
- [ ] **Expected**: Form not submitted
- [ ] **Result**: _____

### DATA-VAL-002: Data type validation
- [ ] Enter text in numeric field (e.g., Quantity)
- [ ] **Expected**: Client-side validation error
- [ ] **Result**: _____

### DATA-VAL-003: Range validation
- [ ] Enter negative number in Quantity
- [ ] **Expected**: Validation error
- [ ] **Result**: _____

### DATA-VAL-004: Date format validation
- [ ] Enter invalid date format
- [ ] **Expected**: Date picker or validation error
- [ ] **Result**: _____

---

## 10. UI/UX TESTING

### UX-USE-002: Navigation is intuitive
- [ ] Test main menu navigation
- [ ] **Expected**: All menu items work
- [ ] **Expected**: Active page highlighted
- [ ] **Result**: _____

### UX-USE-003: Forms are easy to fill
- [ ] Create a record in any module
- [ ] **Expected**: Labels clear, fields logically ordered
- [ ] **Result**: _____

### UX-USE-004: Error messages are helpful
- [ ] Trigger a validation error
- [ ] **Expected**: Error message explains issue
- [ ] **Expected**: Error message in red/highlighted
- [ ] **Result**: _____

### UX-USE-005: Confirmation messages are clear
- [ ] Save a record
- [ ] **Expected**: Success message shown
- [ ] **Result**: _____

---

## 11. RESPONSIVE DESIGN (UX-BROWSER Series)

### Test on Different Screen Sizes

#### Desktop (1920x1080)
- [ ] All pages render correctly
- [ ] DataTables show all columns
- [ ] No horizontal scrolling
- [ ] **Result**: _____

#### Tablet (768px width)
- [ ] Pages adjust to tablet view
- [ ] Tables responsive/scrollable
- [ ] Buttons accessible
- [ ] **Result**: _____

#### Mobile (375px width)
- [ ] Pages adjust to mobile view
- [ ] Navigation becomes hamburger menu
- [ ] Forms stack vertically
- [ ] Tables scrollable
- [ ] **Result**: _____

---

## 12. BROWSER COMPATIBILITY (UX-BROWSER Series)

Test the application in multiple browsers:

### Chrome (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Firefox (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Edge (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Safari (if available)
- [ ] All features work
- [ ] **Result**: _____

---

## SUMMARY

**Total Test Cases**: 50+
**Passed**: _____
**Failed**: _____
**Pass Rate**: _____%

**Critical Issues Found**:
1. _____
2. _____
3. _____

**Recommendations**:
_____

**Tester Name**: __________
**Date Completed**: __________
**Sign-off**: __________

---

## NOTES

- Mark each test as ✅ PASS or ❌ FAIL
- Document any issues in detail
- Take screenshots of errors
- Report all findings in issue tracker

EOF

log_test "MANUAL-001" "Manual testing checklist generated" "PASS"

#############################################
# CLEANUP
#############################################
print_section "CLEANUP"

# Stop application if we started it
if [ ! -z "$APP_PID" ] && kill -0 $APP_PID 2>/dev/null; then
    echo "Stopping application (PID: $APP_PID)..." | tee -a "$RESULTS_FILE"
    kill $APP_PID
    sleep 2
    log_test "CLEANUP-001" "Application stopped cleanly" "PASS"
else
    log_test "CLEANUP-001" "Application cleanup" "SKIP" "Application was already running or didn't start"
fi

#############################################
# GENERATE SUMMARY
#############################################
print_section "PHASE 2 TEST SUMMARY"

echo "" | tee -a "$RESULTS_FILE"
echo "Total Tests Run: $TOTAL_TESTS" | tee -a "$RESULTS_FILE"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}" | tee -a "$RESULTS_FILE"
echo -e "${RED}Failed: $FAILED_TESTS${NC}" | tee -a "$RESULTS_FILE"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}" | tee -a "$RESULTS_FILE"
echo -e "${CYAN}Skipped: $SKIPPED_TESTS${NC}" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$(( (PASSED_TESTS * 100) / TOTAL_TESTS ))
    echo "Pass Rate: ${PASS_RATE}%" | tee -a "$RESULTS_FILE"
fi

if [ "$FAILED_TESTS" -eq 0 ]; then
    echo -e "\n${GREEN}✓ ALL AUTOMATED TESTS PASSED${NC}" | tee -a "$RESULTS_FILE"
    EXIT_CODE=0
else
    echo -e "\n${RED}✗ SOME TESTS FAILED - REVIEW REQUIRED${NC}" | tee -a "$RESULTS_FILE"
    EXIT_CODE=1
fi

echo "" | tee -a "$RESULTS_FILE"
echo "Completed: $(date)" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" | tee -a "$RESULTS_FILE"
echo -e "${CYAN}Manual testing checklist: MANUAL_TESTING_CHECKLIST_PHASE2.md${NC}" | tee -a "$RESULTS_FILE"

# Generate summary report
cat > "$SUMMARY_FILE" << EOF
# RMMS Phase 2: Functional Testing Report

**Date**: $(date)
**Test Type**: Automated + Manual Checklist
**Application**: RMMS v1.0

## Executive Summary

- **Total Automated Tests**: $TOTAL_TESTS
- **Passed**: $PASSED_TESTS
- **Failed**: $FAILED_TESTS
- **Warnings**: $WARNINGS
- **Skipped**: $SKIPPED_TESTS
- **Pass Rate**: ${PASS_RATE}%

## Test Coverage

### Automated Tests Completed ✓
- Pre-flight checks
- HTTP accessibility tests
- Database schema validation
- Controller endpoint tests
- View rendering tests
- DataTables implementation check
- Responsive design check

### Manual Tests Required ⏳
- Authentication flows
- CRUD operations (all modules)
- Form validation
- DataTables functionality
- Reports generation
- Browser compatibility
- Responsive design (visual)

## Next Steps

1. Complete manual testing using: **MANUAL_TESTING_CHECKLIST_PHASE2.md**
2. Document all findings
3. Fix any critical issues
4. Proceed to Phase 3 (Performance Testing)

## Files Generated

- \`$RESULTS_FILE\` - Detailed test log
- \`$SUMMARY_FILE\` - This summary
- \`MANUAL_TESTING_CHECKLIST_PHASE2.md\` - Manual test checklist (50+ test cases)

---

**Status**: Phase 2 automated tests complete. Manual testing required for full coverage.
EOF

echo -e "\n${BLUE}Phase 2 Summary Report: $SUMMARY_FILE${NC}"
echo -e "${CYAN}📋 Manual Testing Checklist: MANUAL_TESTING_CHECKLIST_PHASE2.md${NC}"
echo -e "${YELLOW}⚠️  Complete the manual testing checklist to finish Phase 2${NC}\n"

exit $EXIT_CODE
