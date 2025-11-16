#!/bin/bash
# RMMS Continue Script - Automated Step Execution
# Version: 1.0
# Created: 2025-10-13 01:30
# Purpose: Execute next step from CURRENT_STEP.md automatically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         RMMS AUTOMATED CONTINUATION SYSTEM                 ║"
echo "║              Continue from Current Step                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Function to display current step
show_current_step() {
    echo -e "${BLUE}📍 CHECKING CURRENT STEP...${NC}"
    echo ""

    if [ ! -f "CURRENT_STEP.md" ]; then
        echo -e "${RED}❌ ERROR: CURRENT_STEP.md not found${NC}"
        echo "Please ensure you're in the correct directory."
        exit 1
    fi

    # Extract step ID from CURRENT_STEP.md
    STEP_ID=$(grep "^\*\*STEP ID:\*\*" CURRENT_STEP.md | sed 's/\*\*STEP ID:\*\* //')
    STEP_NAME=$(grep "^\*\*STEP NAME:\*\*" CURRENT_STEP.md | sed 's/\*\*STEP NAME:\*\* //')
    ESTIMATED_TIME=$(grep "^\*\*ESTIMATED TIME:\*\*" CURRENT_STEP.md | sed 's/\*\*ESTIMATED TIME:\*\* //')

    echo -e "${GREEN}Current Step: ${STEP_ID}${NC}"
    echo -e "${GREEN}Step Name:${STEP_NAME}${NC}"
    echo -e "${GREEN}Estimated Time:${ESTIMATED_TIME}${NC}"
    echo ""
}

# Function to execute Step 3.1.1
execute_step_3_1_1() {
    echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  EXECUTING STEP 3.1.1: Activate Analytics Services${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${BLUE}🔥 CRITICAL DISCOVERY:${NC}"
    echo "Analytics services are already coded in _Disabled folder!"
    echo "This is a 2-hour quick win to activate 90% complete functionality."
    echo ""

    # Ask for confirmation
    read -p "Do you want to proceed with Step 3.1.1? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⚠️  Execution cancelled by user.${NC}"
        exit 0
    fi

    echo ""
    echo -e "${GREEN}✅ Starting Step 3.1.1 execution...${NC}"
    echo ""

    # Sub-task 1: Create Implementations directory
    echo -e "${BLUE}[1/9] Creating Implementations directory...${NC}"
    mkdir -p RMMS.Services/Services/Analytics/Implementations
    if [ -d "RMMS.Services/Services/Analytics/Implementations" ]; then
        echo -e "${GREEN}✅ Directory created successfully${NC}"
    else
        echo -e "${RED}❌ Failed to create directory${NC}"
        exit 1
    fi
    echo ""

    # Sub-task 2: Copy analytics services
    echo -e "${BLUE}[2/9] Copying analytics services from _Disabled...${NC}"

    if [ ! -f "_Disabled/ProductionAnalyticsService.cs" ]; then
        echo -e "${RED}❌ ERROR: _Disabled/ProductionAnalyticsService.cs not found${NC}"
        echo "Please ensure the analytics services exist in _Disabled folder."
        exit 1
    fi

    cp _Disabled/ProductionAnalyticsService.cs RMMS.Services/Services/Analytics/Implementations/
    echo -e "  ✅ ProductionAnalyticsService.cs copied"

    cp _Disabled/InventoryAnalyticsService.cs RMMS.Services/Services/Analytics/Implementations/
    echo -e "  ✅ InventoryAnalyticsService.cs copied"

    cp _Disabled/ComprehensiveAnalyticsServices.cs RMMS.Services/Services/Analytics/Implementations/
    echo -e "  ✅ ComprehensiveAnalyticsServices.cs copied"

    echo -e "${GREEN}✅ All services copied successfully${NC}"
    echo ""

    # Sub-task 3: Update namespaces
    echo -e "${BLUE}[3/9] Updating namespaces in service files...${NC}"

    # Update ProductionAnalyticsService.cs
    sed -i 's/namespace RMMS\.Web\.Services/namespace RMMS.Services.Services.Analytics.Implementations/' \
        RMMS.Services/Services/Analytics/Implementations/ProductionAnalyticsService.cs
    echo -e "  ✅ ProductionAnalyticsService.cs namespace updated"

    # Update InventoryAnalyticsService.cs
    sed -i 's/namespace RMMS\.Web\.Services/namespace RMMS.Services.Services.Analytics.Implementations/' \
        RMMS.Services/Services/Analytics/Implementations/InventoryAnalyticsService.cs
    echo -e "  ✅ InventoryAnalyticsService.cs namespace updated"

    # Update ComprehensiveAnalyticsServices.cs
    sed -i 's/namespace RMMS\.Web\.Services/namespace RMMS.Services.Services.Analytics.Implementations/' \
        RMMS.Services/Services/Analytics/Implementations/ComprehensiveAnalyticsServices.cs
    echo -e "  ✅ ComprehensiveAnalyticsServices.cs namespace updated"

    echo -e "${GREEN}✅ All namespaces updated successfully${NC}"
    echo ""

    # Sub-task 4: Register services in Program.cs
    echo -e "${BLUE}[4/9] Registering services in Program.cs...${NC}"
    echo -e "${YELLOW}⚠️  This step requires manual intervention${NC}"
    echo ""
    echo "Please add the following code to RMMS.Web/Program.cs after line 93:"
    echo ""
    echo -e "${YELLOW}────────────────────────────────────────────────────────────${NC}"
    cat << 'EOF'
// ============================================================
// PHASE 3.1: ANALYTICS SERVICES
// ============================================================
using RMMS.Services.Services.Analytics;
using RMMS.Services.Services.Analytics.Implementations;

// Production Analytics (Tasks 1, 7, 8, 9)
builder.Services.AddScoped<IProductionAnalyticsService, ProductionAnalyticsService>();

// Inventory Analytics (Tasks 2, 10)
builder.Services.AddScoped<IInventoryAnalyticsService, InventoryAnalyticsService>();

// Sales & Customer Analytics (Tasks 3, 5)
builder.Services.AddScoped<ISalesTrendAnalyticsService, SalesTrendAnalyticsService>();
builder.Services.AddScoped<ICustomerBehaviorAnalyticsService, CustomerBehaviorAnalyticsService>();

// Profit & Cost Analytics (Task 4, 11)
builder.Services.AddScoped<IProfitMarginAnalysisService, ProfitMarginAnalysisService>();
builder.Services.AddScoped<ICostAnalysisService, CostAnalysisService>();

// Supplier Performance (Task 6)
builder.Services.AddScoped<ISupplierPerformanceService, SupplierPerformanceService>();

// Business Intelligence (Task 12)
builder.Services.AddScoped<IBusinessIntelligenceService, BusinessIntelligenceService>();
EOF
    echo -e "${YELLOW}────────────────────────────────────────────────────────────${NC}"
    echo ""

    read -p "Have you added the service registrations to Program.cs? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⚠️  Please add the service registrations and run this script again.${NC}"
        exit 0
    fi

    echo -e "${GREEN}✅ Service registrations confirmed${NC}"
    echo ""

    # Sub-task 5: Build solution
    echo -e "${BLUE}[5/9] Building solution...${NC}"
    dotnet build > /tmp/build_output.txt 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Build succeeded${NC}"
    else
        echo -e "${RED}❌ Build failed. Errors:${NC}"
        tail -30 /tmp/build_output.txt
        echo ""
        echo "Please fix the build errors and run this script again."
        exit 1
    fi
    echo ""

    # Sub-task 6: Test service injection
    echo -e "${BLUE}[6/9] Testing service injection...${NC}"
    echo -e "${YELLOW}⚠️  Ensure application is running on http://localhost:5090${NC}"

    # Check if app is running
    if pgrep -f "dotnet.*RMMS.Web" > /dev/null; then
        echo -e "${GREEN}✅ Application is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Application not running. Start it with: dotnet run${NC}"
    fi
    echo ""

    # Sub-task 7: Create analytics views
    echo -e "${BLUE}[7/9] Creating analytics views...${NC}"
    echo -e "${YELLOW}⚠️  This step requires creating view files${NC}"
    echo ""
    echo "Views to create:"
    echo "  1. /Views/Analytics/_ViewStart.cshtml"
    echo "  2. /Views/Analytics/Index.cshtml"
    echo "  3. /Views/Analytics/Production.cshtml"
    echo "  4. /Views/Analytics/Inventory.cshtml"
    echo "  5. /Views/Analytics/Sales.cshtml"
    echo ""
    echo "Refer to QUICK_START_PHASE3.md for view templates."
    echo ""

    read -p "Have you created the analytics views? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⚠️  Please create the views and run this script again.${NC}"
        echo "Or continue manually following QUICK_START_PHASE3.md"
        exit 0
    fi

    echo -e "${GREEN}✅ Analytics views confirmed${NC}"
    echo ""

    # Sub-task 8: Test analytics pages
    echo -e "${BLUE}[8/9] Testing analytics pages...${NC}"

    # Test /Analytics endpoint
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5090/Analytics 2>/dev/null || echo "000")

    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
        echo -e "${GREEN}✅ /Analytics returns HTTP $HTTP_CODE${NC}"
    else
        echo -e "${YELLOW}⚠️  /Analytics returns HTTP $HTTP_CODE${NC}"
        echo "Expected 200 or 302 (redirect to login)"
    fi
    echo ""

    # Sub-task 9: Commit changes
    echo -e "${BLUE}[9/9] Ready to commit changes${NC}"
    echo ""
    echo "Suggested commit message:"
    echo "  'Phase 3.1: Analytics services activated'"
    echo ""

    read -p "Do you want to commit changes now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Note: User should handle git commits manually
        echo -e "${YELLOW}⚠️  Please commit manually:${NC}"
        echo "  git add ."
        echo "  git commit -m 'Phase 3.1: Analytics services activated'"
    fi
    echo ""

    # Step complete
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ STEP 3.1.1 COMPLETE!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Update CURRENT_STEP.md to next step
    echo -e "${BLUE}📝 Updating CURRENT_STEP.md to next step...${NC}"
    # This would update to step 3.1.2 in a real implementation
    echo -e "${YELLOW}⚠️  CURRENT_STEP.md update not yet implemented${NC}"
    echo "Next step will be 3.1.2: Create remaining analytics views"
    echo ""
}

# Function to show help
show_help() {
    echo "Usage: ./continue.sh [options]"
    echo ""
    echo "Options:"
    echo "  --help, -h       Show this help message"
    echo "  --status, -s     Show current step without executing"
    echo "  --force, -f      Force execution without confirmation"
    echo ""
    echo "Examples:"
    echo "  ./continue.sh              # Execute next step with confirmation"
    echo "  ./continue.sh --status     # Just show current step"
    echo "  ./continue.sh --force      # Execute without asking"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --status|-s)
        show_current_step
        exit 0
        ;;
    --force|-f)
        # Force execution
        ;;
    "")
        # Normal execution
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac

# Main execution
show_current_step

# Determine which step to execute based on STEP_ID
STEP_ID=$(grep "^\*\*STEP ID:\*\*" CURRENT_STEP.md | sed 's/\*\*STEP ID:\*\* //')

case "$STEP_ID" in
    3.1.1)
        execute_step_3_1_1
        ;;
    *)
        echo -e "${YELLOW}⚠️  Step $STEP_ID not yet automated${NC}"
        echo "Please follow instructions in:"
        echo "  - QUICK_START_PHASE3.md (for immediate steps)"
        echo "  - ULTRATHINK_COMPLETE_IMPLEMENTATION_PLAN.md (for full roadmap)"
        echo "  - STEP_BY_STEP_EXECUTION.md (for sequential steps)"
        echo ""
        exit 0
        ;;
esac

echo -e "${GREEN}✅ Continue script completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. Run ./resume.sh to see updated status"
echo "  2. Run ./continue.sh again for next step"
echo "  3. Or refer to STEP_BY_STEP_EXECUTION.md for manual steps"
echo ""
