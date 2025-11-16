#!/bin/bash

# Test all menu pages and check HTTP status
BASE_URL="http://localhost:5090"

echo "======================================"
echo "TESTING ALL RMMS MENU PAGES"
echo "======================================"
echo ""

# Function to test a page
test_page() {
    local url=$1
    local name=$2
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$status" = "200" ]; then
        echo "✅ $name - OK ($status)"
    elif [ "$status" = "500" ]; then
        echo "❌ $name - ERROR 500 (Server Error)"
    elif [ "$status" = "404" ]; then
        echo "❌ $name - ERROR 404 (Not Found)"
    else
        echo "⚠️  $name - Status $status"
    fi
}

echo "DASHBOARD:"
test_page "$BASE_URL/" "Home/Dashboard"
echo ""

echo "MASTER DATA:"
test_page "$BASE_URL/Customers" "Customers"
test_page "$BASE_URL/Vendors" "Vendors"
test_page "$BASE_URL/Products" "Products"
test_page "$BASE_URL/Employees" "Employees"
echo ""

echo "INVENTORY:"
test_page "$BASE_URL/Warehouses" "Warehouses"
test_page "$BASE_URL/Inventory" "Inventory Ledger"
test_page "$BASE_URL/StockMovements" "Stock Movements"
test_page "$BASE_URL/StockAdjustments" "Stock Adjustments"
echo ""

echo "PRODUCTION:"
test_page "$BASE_URL/Machines" "Machines"
test_page "$BASE_URL/ProductionOrders" "Production Orders"
test_page "$BASE_URL/ProductionBatches" "Production Batches"
test_page "$BASE_URL/YieldAnalysis" "Yield Analysis"
echo ""

echo "PROCUREMENT:"
test_page "$BASE_URL/PaddyProcurement" "Paddy Procurement"
test_page "$BASE_URL/RiceProcurementExternal" "External Rice Procurement"
echo ""

echo "SALES:"
test_page "$BASE_URL/Inquiries" "Inquiries"
test_page "$BASE_URL/Quotations" "Quotations"
test_page "$BASE_URL/SalesOrders" "Sales Orders"
test_page "$BASE_URL/RiceSales" "Rice Sales"
test_page "$BASE_URL/ByProductSales" "By-Product Sales"
test_page "$BASE_URL/ExternalRiceSales" "External Rice Sales"
echo ""

echo "FINANCE:"
test_page "$BASE_URL/BankTransactions" "Bank Book"
test_page "$BASE_URL/CashBook" "Cash Book"
test_page "$BASE_URL/Vouchers" "Vouchers"
test_page "$BASE_URL/PayablesOverdue" "Payables"
test_page "$BASE_URL/ReceivablesOverdue" "Receivables"
test_page "$BASE_URL/LoansAdvances" "Loans & Advances"
echo ""

echo "ASSETS:"
test_page "$BASE_URL/FixedAssets" "Fixed Assets"
echo ""

echo "REPORTS:"
test_page "$BASE_URL/Reports" "Reports"
echo ""

echo "======================================"
echo "TEST COMPLETE"
echo "======================================"
