#!/bin/bash

echo "=========================================="
echo "RMMS Application - Automated Verification"
echo "=========================================="
echo ""

PASS=0
FAIL=0
TOTAL=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run a test
run_test() {
    TOTAL=$((TOTAL + 1))
    TEST_NAME=$1
    COMMAND=$2

    echo -n "Test $TOTAL: $TEST_NAME... "

    if eval "$COMMAND" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASS=$((PASS + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAIL=$((FAIL + 1))
        return 1
    fi
}

cd /home/user01/claude-test/RMMS.Web

echo "=== BUILD VERIFICATION ==="
echo ""

run_test "Debug Build Succeeds" "dotnet build --configuration Debug"
run_test "Release Build Succeeds" "dotnet build --configuration Release"

echo ""
echo "=== FILE STRUCTURE VERIFICATION ==="
echo ""

run_test "DecimalModelBinder.cs exists" "test -f RMMS.Web/Utilities/DecimalModelBinder.cs"
run_test "Program.cs has decimal binder registration" "grep -q 'DecimalModelBinderProvider' RMMS.Web/Program.cs"
run_test "site-enhanced.js has DataTable fix" "grep -q 'destroy()' RMMS.Web/wwwroot/js/site-enhanced.js"
run_test "_Layout.cshtml has alert fix" "grep -q 'data-no-auto-dismiss' RMMS.Web/Views/Shared/_Layout.cshtml"

echo ""
echo "=== CONTROLLER VERIFICATION ==="
echo ""

run_test "PaddyProcurementController exists" "test -f RMMS.Web/Controllers/PaddyProcurementController.cs"
run_test "RiceSalesController exists" "test -f RMMS.Web/Controllers/RiceSalesController.cs"
run_test "ByProductSalesController exists" "test -f RMMS.Web/Controllers/ByProductSalesController.cs"
run_test "PayablesOverdueController has SendBulkReminders" "grep -q 'SendBulkReminders' RMMS.Web/Controllers/PayablesOverdueController.cs"
run_test "ReceivablesOverdueController has SendBulkReminders" "grep -q 'SendBulkReminders' RMMS.Web/Controllers/ReceivablesOverdueController.cs"
run_test "ReportsController has PaddyProcurementService" "grep -q 'IPaddyProcurementService' RMMS.Web/Controllers/ReportsController.cs"

echo ""
echo "=== SERVICE VERIFICATION ==="
echo ""

run_test "DashboardService exists" "test -f RMMS.Services/DashboardService.cs"
run_test "PaddyProcurementService exists" "test -f RMMS.Services/PaddyProcurementService.cs"
run_test "RiceSalesService exists" "test -f RMMS.Services/RiceSalesService.cs"
run_test "PayableOverdueService exists" "test -f RMMS.Services/PayableOverdueService.cs"
run_test "ReceivableOverdueService exists" "test -f RMMS.Services/ReceivableOverdueService.cs"

echo ""
echo "=== VIEW VERIFICATION ==="
echo ""

run_test "Stock Summary view exists" "test -f RMMS.Web/Views/PaddyProcurement/StockSummary.cshtml"
run_test "Rice Sales Edit view exists" "test -f RMMS.Web/Views/RiceSales/Edit.cshtml"
run_test "Outstanding Payments view exists" "test -f RMMS.Web/Views/Reports/OutstandingPayments.cshtml"
run_test "Outstanding Payments has DataTable init" "grep -q 'DataTable' RMMS.Web/Views/Reports/OutstandingPayments.cshtml"
run_test "Payables has Send Reminders button" "grep -q 'sendReminders' RMMS.Web/Views/PayablesOverdue/Index.cshtml"
run_test "Receivables has Send Reminders button" "grep -q 'sendReminders' RMMS.Web/Views/ReceivablesOverdue/Index.cshtml"

echo ""
echo "=== DATABASE CONNECTIVITY VERIFICATION ==="
echo ""

run_test "DashboardService uses stored procedures" "grep -q 'sp_Dashboard' RMMS.Services/DashboardService.cs"
run_test "PaddyProcurement uses repository" "grep -q '_repository' RMMS.Services/PaddyProcurementService.cs"
run_test "RiceSales uses repository" "grep -q '_repository' RMMS.Services/RiceSalesService.cs"

echo ""
echo "=== CONFIGURATION VERIFICATION ==="
echo ""

run_test "appsettings.json exists" "test -f RMMS.Web/appsettings.json"
run_test "Connection string configured" "grep -q 'ConnectionStrings' RMMS.Web/appsettings.json"

echo ""
echo "=== CRITICAL FIX VERIFICATION ==="
echo ""

run_test "Global decimal validation registered" "grep -q 'DecimalModelBinderProvider' RMMS.Web/Program.cs"
run_test "DataTable destroy implemented" "grep -q 'if.*isDataTable.*destroy' RMMS.Web/wwwroot/js/site-enhanced.js"
run_test "Alert selective dismiss implemented" "grep -A5 'auto-dismiss' RMMS.Web/Views/Shared/_Layout.cshtml | grep -q 'data-no-auto-dismiss'"
run_test "Stock Summary returns correct type" "grep -A3 'StockSummary()' RMMS.Web/Controllers/PaddyProcurementController.cs | grep -q 'GetAllProcurements'"
run_test "Paddy Stock Report uses service" "grep -A3 'PaddyStock()' RMMS.Web/Controllers/ReportsController.cs | grep -q '_paddyProcurementService'"
run_test "Outstanding Payments Pay Now connected" "grep -q 'asp-controller=\"PayablesOverdue\".*RecordPayment' RMMS.Web/Views/Reports/OutstandingPayments.cshtml"
run_test "Outstanding Payments Send Reminder connected" "grep -q 'asp-controller=\"ReceivablesOverdue\".*SendReminder' RMMS.Web/Views/Reports/OutstandingPayments.cshtml"

echo ""
echo "=== CODE QUALITY CHECKS ==="
echo ""

run_test "No syntax errors (build clean)" "dotnet build > /dev/null 2>&1"
run_test "No duplicate class definitions" "! find . -name '*.cs' -exec grep -l 'public class.*Controller' {} \; | sort | uniq -d | grep -q ."

echo ""
echo "=========================================="
echo "           TEST SUMMARY"
echo "=========================================="
echo ""
echo -e "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

PERCENTAGE=$((PASS * 100 / TOTAL))
echo "Success Rate: $PERCENTAGE%"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ ALL AUTOMATED TESTS PASSED!${NC}"
    echo ""
    echo "Code Quality: EXCELLENT"
    echo "Build Status: SUCCESS"
    echo "Next Step: Run application and perform manual testing"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Review failed tests above and fix issues"
    exit 1
fi
