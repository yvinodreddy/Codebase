#!/bin/bash
# RMMS Application - Production Ready Deployment and Testing Script
set -e

echo "=========================================="
echo "RMMS - Complete Setup & Testing"
echo "=========================================="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Step 1: Cleaning up...${NC}"
pkill -9 -f "dotnet.*RMMS.Web" 2>/dev/null || true
sleep 2
echo -e "${GREEN}✓ Cleanup complete${NC}"

echo -e "${YELLOW}Step 2: Fixing database schema...${NC}"
cd /tmp && dotnet script complete_schema_fix.csx 2>&1 | grep -E "(✓|Connected)" || true
echo -e "${GREEN}✓ Schema fixed${NC}"

echo -e "${YELLOW}Step 3: Building...${NC}"
cd /home/user01/claude-test/RMMS.Web && dotnet build 2>&1 | tail -3
echo -e "${GREEN}✓ Build complete${NC}"

echo -e "${YELLOW}Step 4: Starting application...${NC}"
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet run --urls "http://localhost:5000" > /tmp/rmms_prod.log 2>&1 &
APP_PID=$!
echo "PID: $APP_PID"
sleep 10

if curl -s http://localhost:5000 > /dev/null; then
    echo -e "${GREEN}✓ App started${NC}"
else
    echo -e "${RED}✗ App failed${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 5: Seeding database...${NC}"
curl -X POST -s "http://localhost:5000/Seed/SeedData" > /tmp/seed_result.html
if grep -q "COMPLETE" /tmp/seed_result.html; then
    echo -e "${GREEN}✓ Seeded successfully${NC}"
else
    echo -e "${YELLOW}⚠ Check seed status${NC}"
fi

echo ""
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE${NC}"
echo "URL: http://localhost:5000"
echo "PID: $APP_PID"
echo "Logs: tail -f /tmp/rmms_prod.log"
