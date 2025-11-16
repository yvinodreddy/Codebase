#!/bin/bash

echo "========================================="
echo "RMMS Application - Page Testing Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:5090"

# Array of pages to test
declare -a pages=(
    "/"
    "/Home/Index"
    "/Customers"
    "/Vendors"
    "/Products"
    "/Employees"
    "/Warehouses"
    "/InventoryLedger"
    "/StockMovements"
    "/StockAdjustments"
    "/Machines"
    "/ProductionOrders"
    "/ProductionBatches"
)

echo "Testing all pages..."
echo ""

# Check if app is running
if ! curl -s http://localhost:5090 > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Application is not running on port 5090${NC}"
    echo "Please start the application first"
    exit 1
fi

echo -e "${GREEN}✓ Application is running${NC}"
echo ""

# Test each page
for page in "${pages[@]}"
do
    echo -n "Testing $page ... "

    # Make request and capture HTTP status
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -L "$BASE_URL$page" 2>&1)

    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ OK (200)${NC}"
    elif [ "$http_code" == "302" ] || [ "$http_code" == "301" ]; then
        echo -e "${YELLOW}⚠ REDIRECT ($http_code) - Likely requires login${NC}"
    elif [ "$http_code" == "404" ]; then
        echo -e "${RED}✗ NOT FOUND (404)${NC}"
    elif [ "$http_code" == "500" ]; then
        echo -e "${RED}✗ SERVER ERROR (500)${NC}"
    else
        echo -e "${RED}✗ ERROR ($http_code)${NC}"
    fi
done

echo ""
echo "========================================="
echo "Checking for application errors..."
echo "========================================="

# Check recent application logs
if [ -f /tmp/rmms_app.log ]; then
    echo ""
    echo "Last 20 errors from application log:"
    tail -200 /tmp/rmms_app.log | grep -i "error\|exception\|fail" | tail -20 | while read line; do
        echo -e "${RED}$line${NC}"
    done
else
    echo "No application log found at /tmp/rmms_app.log"
fi

echo ""
echo "========================================="
echo "Database Connection Test"
echo "========================================="

# Test database connection
if command -v sqlcmd &> /dev/null; then
    echo "Testing database connection..."
    if sqlcmd -S 172.17.208.1 -U sa -P 'YourStrong@Passw0rd' -d RMMS_Production -Q "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'" -C -h -1 2>/dev/null; then
        echo -e "${GREEN}✓ Database connection OK${NC}"
    else
        echo -e "${RED}✗ Database connection FAILED${NC}"
    fi
else
    # Try alternate path
    if /opt/mssql-tools18/bin/sqlcmd -S 172.17.208.1 -U sa -P 'YourStrong@Passw0rd' -d RMMS_Production -Q "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'" -C -h -1 2>/dev/null; then
        echo -e "${GREEN}✓ Database connection OK${NC}"
    else
        echo -e "${YELLOW}⚠ Cannot test database (sqlcmd not found in standard locations)${NC}"
    fi
fi

echo ""
echo "========================================="
echo "Test Complete"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Review the output above"
echo "2. For pages showing errors, open them in browser"
echo "3. Press F12 to see browser console errors"
echo "4. Fill out ISSUE_REPORT_TEMPLATE.md with details"
echo ""
