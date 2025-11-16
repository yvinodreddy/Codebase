#!/bin/bash

# FHIR Healthcare API - Comprehensive Endpoint Testing Script
# This script tests all critical endpoints to verify the API is working correctly

API_BASE="https://localhost:7012"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================="
echo "FHIR Healthcare API - Endpoint Tests"
echo "API Base URL: $API_BASE"
echo "========================================="
echo ""

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local endpoint="$2"
    local method="${3:-GET}"
    local expected_pattern="$4"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Testing: $test_name ... "

    if [ "$method" = "GET" ]; then
        response=$(curl -k -s -w "\n%{http_code}" "$API_BASE$endpoint" 2>/dev/null)
    else
        response=$(curl -k -s -w "\n%{http_code}" -X "$method" "$API_BASE$endpoint" 2>/dev/null)
    fi

    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        if [ -n "$expected_pattern" ]; then
            if echo "$body" | grep -q "$expected_pattern"; then
                echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
                PASSED_TESTS=$((PASSED_TESTS + 1))
            else
                echo -e "${RED}✗ FAILED${NC} (Expected pattern not found)"
                FAILED_TESTS=$((FAILED_TESTS + 1))
            fi
        else
            echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

echo -e "${BLUE}=== System Health Tests ===${NC}"
run_test "Health Check" "/health" "GET" "Healthy"
run_test "Data Seeding Status" "/api/DataSeeding/status" "GET" "Ready"
echo ""

echo -e "${BLUE}=== Patient Endpoints ===${NC}"
run_test "Get Patient 1" "/api/Patient/1" "GET" "Johnson"
run_test "Get Patient 2" "/api/Patient/2" "GET" "Chen"
run_test "Search Patient by Name" "/api/Patient/search/Sarah" "GET" "Johnson"
echo ""

echo -e "${BLUE}=== Observation Endpoints ===${NC}"
run_test "Get Patient 1 Observations" "/api/Observation/patient/1" "GET" "observation"
run_test "Get Patient 2 Observations" "/api/Observation/patient/2" "GET" "observation"
echo ""

echo -e "${BLUE}=== Condition Endpoints ===${NC}"
run_test "Get Patient 1 Conditions" "/api/Condition/patient/1" "GET" "Condition"
run_test "Get Patient 2 Conditions" "/api/Condition/patient/2" "GET" "Condition"
echo ""

echo -e "${BLUE}=== Medication Endpoints ===${NC}"
run_test "Get Patient 1 Medication Summary" "/api/Medication/patient/1" "GET"
run_test "Get Patient 2 Medication Summary" "/api/Medication/patient/2" "GET"
echo ""

echo -e "${BLUE}=== Terminology Services ===${NC}"
run_test "RxNorm Drug Lookup (Lisinopril)" "/api/RxNormLive/drug/197361" "GET" "lisinopril"
run_test "RxNorm Search (Aspirin)" "/api/RxNormLive/search/aspirin" "GET"
run_test "LOINC Test Lookup (Glucose)" "/api/LoincCurrent/test/1558-6" "GET"
echo ""

echo -e "${BLUE}=== Care Plan Endpoints ===${NC}"
run_test "Get Patient 1 Care Plans" "/api/CarePlan/patient/1" "GET" "CarePlan"
echo ""

echo -e "${BLUE}=== Public Test Endpoint ===${NC}"
run_test "Public Test Endpoint" "/api/PublicTest/hello" "GET"
echo ""

echo "========================================="
echo -e "${BLUE}Test Summary${NC}"
echo "========================================="
echo -e "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}API is fully operational and ready for MCP integration${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
