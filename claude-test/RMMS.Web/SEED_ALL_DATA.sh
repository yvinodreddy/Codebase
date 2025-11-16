#!/bin/bash

echo "========================================="
echo "RMMS DATA SEEDING SCRIPT"
echo "========================================="
echo ""
echo "This script will generate 40+ test records for all entities"
echo "to enable proper pagination and sorting testing."
echo ""
echo "Prerequisites:"
echo "1. Application must be running (dotnet run)"
echo "2. Database must be accessible"
echo ""
echo "Press ENTER to continue or CTRL+C to cancel..."
read

echo ""
echo "Starting data seeding process..."
echo ""

# Check if application is running
if ! curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo "ERROR: Application is not running at http://localhost:5000"
    echo "Please start the application first:"
    echo "  cd /home/user01/claude-test/RMMS.Web/RMMS.Web"
    echo "  dotnet run"
    exit 1
fi

echo "✓ Application is running"
echo ""
echo "Calling data seeding endpoint..."
echo ""

# Call the seeding endpoint
curl -X POST http://localhost:5000/Seed/SeedData \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -v

echo ""
echo ""
echo "========================================="
echo "DATA SEEDING COMPLETE!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Navigate to any page with tables/grids"
echo "2. Verify pagination shows at bottom"
echo "3. Verify sorting works on column headers"
echo "4. Verify 16 rows per page (default)"
echo "5. Check that 'Show entries' dropdown appears"
echo ""
echo "Pages to test:"
echo "- /PaddyProcurement"
echo "- /RiceSales"
echo "- /CashBook"
echo "- /BankTransactions"
echo "- /Vouchers"
echo "- /FixedAssets"
echo "- /LoansAdvances"
echo "- /ByProductSales"
echo "- /ExternalRiceSales"
echo "- /PayablesOverdue"
echo "- /ReceivablesOverdue"
echo "- /YieldAnalysis/Trends"
echo "- /YieldAnalysis/ByVariety"
echo "- /YieldAnalysis/ByMachine"
echo "- /Reports/CustomerWiseSales"
echo "- /Reports/ProductWiseSales"
echo "- /Reports/DailySales"
echo ""
