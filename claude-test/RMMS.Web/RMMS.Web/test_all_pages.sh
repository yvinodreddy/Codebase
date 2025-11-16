#!/bin/bash

# ╔════════════════════════════════════════════════════════════════════╗
# ║           COMPREHENSIVE UI PAGE TESTING SCRIPT                     ║
# ║           Tests all 27 pages + verifies pagination                 ║
# ╚════════════════════════════════════════════════════════════════════╝

BASE_URL="http://localhost:5090"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_PAGES=0
SUCCESS_PAGES=0
ERROR_PAGES=0
PAGINATION_OK=0
PAGINATION_FAIL=0

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║              COMPREHENSIVE UI PAGE TESTING                         ║"
echo "║              Testing: $BASE_URL                          ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Function to test a page
test_page() {
    local PAGE_NAME="$1"
    local PAGE_PATH="$2"
    local CHECK_PAGINATION="$3"

    ((TOTAL_PAGES++))

    printf "${BLUE}Testing:${NC} %-40s " "$PAGE_NAME"

    # Test if page loads
    HTTP_CODE=$(curl -s -o /tmp/page_test_$$.html -w "%{http_code}" "$BASE_URL$PAGE_PATH" --max-time 10)

    if [ "$HTTP_CODE" = "200" ]; then
        # Check for error indicators in page
        if grep -qi "error\|exception\|stack trace" /tmp/page_test_$$.html 2>/dev/null; then
            echo -e "${RED}❌ ERROR FOUND IN PAGE${NC}"
            ((ERROR_PAGES++))
            # Show first error line
            grep -i "error\|exception" /tmp/page_test_$$.html | head -1 | sed 's/<[^>]*>//g' | cut -c1-80
        else
            echo -e "${GREEN}✅ LOADS OK${NC}"
            ((SUCCESS_PAGES++))

            # Check pagination if requested
            if [ "$CHECK_PAGINATION" = "yes" ]; then
                # Check if pagination controls exist
                if grep -q "page-item\|pagination" /tmp/page_test_$$.html 2>/dev/null; then
                    # Try to count rows in table (rough estimate)
                    ROW_COUNT=$(grep -c "<tr" /tmp/page_test_$$.html 2>/dev/null || echo "0")

                    if [ "$ROW_COUNT" -le 20 ]; then
                        echo -e "   ${GREEN}  ↳ Pagination: ✅ (≤20 rows including header)${NC}"
                        ((PAGINATION_OK++))
                    else
                        echo -e "   ${YELLOW}  ↳ Pagination: ⚠️  ($ROW_COUNT rows - may exceed 16)${NC}"
                        ((PAGINATION_FAIL++))
                    fi
                else
                    echo -e "   ${YELLOW}  ↳ Pagination: ⚠️  (No pagination controls found)${NC}"
                    ((PAGINATION_FAIL++))
                fi
            fi
        fi
    elif [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "301" ]; then
        echo -e "${YELLOW}⚠️  REDIRECT ($HTTP_CODE)${NC}"
        ((SUCCESS_PAGES++))
    else
        echo -e "${RED}❌ FAILED (HTTP $HTTP_CODE)${NC}"
        ((ERROR_PAGES++))
    fi

    rm -f /tmp/page_test_$$.html
}

# Wait for application to be ready
echo "⏳ Waiting for application to be ready..."
sleep 3

for i in {1..10}; do
    if curl -s "$BASE_URL" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application is ready!${NC}"
        echo ""
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Application not responding after 10 seconds${NC}"
        exit 1
    fi
    sleep 1
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MASTER DATA MODULES (with pagination checks)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "1. Customers" "/Customers" "yes"
test_page "2. Vendors" "/Vendors" "yes"
test_page "3. Products" "/Products" "yes"
test_page "4. Employees" "/Employees" "yes"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  INVENTORY MODULES (with pagination checks)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "5. Warehouses" "/Warehouses" "yes"
test_page "6. Inventory Ledger" "/Inventory" "yes"
test_page "7. Stock Movements" "/StockMovements" "yes"
test_page "8. Stock Adjustments" "/StockAdjustments" "yes"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PRODUCTION MODULES (with pagination checks)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "9. Machines" "/Machines" "yes"
test_page "10. Production Orders" "/ProductionOrders" "yes"
test_page "11. Production Batches" "/ProductionBatches" "yes"
test_page "12. Yield Analysis" "/YieldAnalysis" "no"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SALES MODULES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "13. Inquiries" "/Inquiries" "yes"
test_page "14. Quotations" "/Quotations" "yes"
test_page "15. Sales Orders" "/SalesOrders" "yes"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PROCUREMENT MODULES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "16. Paddy Procurement" "/PaddyProcurement" "no"
test_page "17. Rice Procurement External" "/RiceProcurementExternal" "no"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SALES TRACKING MODULES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "18. Rice Sales" "/RiceSales" "no"
test_page "19. By-Product Sales" "/ByProductSales" "no"
test_page "20. External Rice Sales" "/ExternalRiceSales" "no"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  FINANCE MODULES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_page "21. Bank Transactions" "/BankTransactions" "no"
test_page "22. Cash Book" "/CashBook" "no"
test_page "23. Vouchers" "/Vouchers" "no"
test_page "24. Payables Overdue" "/PayablesOverdue" "no"
test_page "25. Receivables Overdue" "/ReceivablesOverdue" "no"
test_page "26. Loans & Advances" "/LoansAdvances" "no"
test_page "27. Fixed Assets" "/FixedAssets" "no"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                      TEST SUMMARY REPORT                           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 PAGE LOAD RESULTS:"
echo "   Total Pages Tested: $TOTAL_PAGES"
echo -e "   ${GREEN}Successful: $SUCCESS_PAGES ✅${NC}"
echo -e "   ${RED}Errors: $ERROR_PAGES ❌${NC}"
echo ""

if [ "$PAGINATION_OK" -gt 0 ] || [ "$PAGINATION_FAIL" -gt 0 ]; then
    echo "📄 PAGINATION RESULTS:"
    echo -e "   ${GREEN}Correct (≤16 records): $PAGINATION_OK ✅${NC}"
    echo -e "   ${YELLOW}Issues Found: $PAGINATION_FAIL ⚠️${NC}"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$ERROR_PAGES" -eq 0 ]; then
    echo -e "${GREEN}✅ SUCCESS: All pages load without errors!${NC}"

    if [ "$PAGINATION_FAIL" -eq 0 ] && [ "$PAGINATION_OK" -gt 0 ]; then
        echo -e "${GREEN}✅ SUCCESS: All pagination checks passed!${NC}"
    fi

    exit 0
else
    echo -e "${RED}❌ FAILURE: $ERROR_PAGES page(s) had errors${NC}"
    exit 1
fi
