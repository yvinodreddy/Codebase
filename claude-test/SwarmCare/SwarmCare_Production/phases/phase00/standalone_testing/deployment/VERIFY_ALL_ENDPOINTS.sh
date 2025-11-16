#!/bin/bash
################################################################################
# Comprehensive Endpoint Verification Script
# Tests all API endpoints and services
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}     COMPREHENSIVE ENDPOINT VERIFICATION${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# Configuration
BASE_URL="http://localhost:8000"
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local url="$2"
    local method="${3:-GET}"

    echo -n "Testing: $name ... "

    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>&1)
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" 2>&1)
    fi

    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ PASS (200)${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL ($response)${NC}"
        ((FAILED++))
    fi
}

echo -e "${YELLOW}[1/5] Testing Core Endpoints...${NC}"
test_endpoint "Dashboard (Root)" "$BASE_URL/"
test_endpoint "Health Check" "$BASE_URL/api/health"
test_endpoint "API Documentation" "$BASE_URL/docs"

echo ""
echo -e "${YELLOW}[2/5] Testing Services...${NC}"
test_endpoint "Services Status" "$BASE_URL/api/services/status"

echo ""
echo -e "${YELLOW}[3/5] Testing User Stories...${NC}"
test_endpoint "Get All Stories" "$BASE_URL/api/stories"
test_endpoint "Get Metrics" "$BASE_URL/api/metrics"

echo ""
echo -e "${YELLOW}[4/5] Testing Trackers...${NC}"
test_endpoint "Phase Tracker" "$BASE_URL/api/trackers/phase"
test_endpoint "Unified Tracker" "$BASE_URL/api/trackers/unified"

echo ""
echo -e "${YELLOW}[5/5] Testing Generated Files & Logs...${NC}"
test_endpoint "Generated Files" "$BASE_URL/api/generated/files"
test_endpoint "Execution Logs" "$BASE_URL/api/logs"
test_endpoint "Run Tests" "$BASE_URL/api/tests/run" "POST"

echo ""
echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}     TEST SUMMARY${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ ALL ENDPOINTS WORKING - 100% SUCCESS!${NC}"
    echo ""
    exit 0
else
    echo ""
    echo -e "${RED}❌ SOME ENDPOINTS FAILED${NC}"
    echo ""
    exit 1
fi
