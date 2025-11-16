#!/bin/bash

# API Testing Script for Patient Management System
# Usage: ./test-api.sh

# Configuration
API_BASE_URL="http://localhost:3000/api"
TOKEN="your-auth-token-here"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "   Patient Management API Testing"
echo "========================================="

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4

    echo -e "\n${YELLOW}Testing:${NC} $description"
    echo "Method: $method"
    echo "Endpoint: $API_BASE_URL$endpoint"

    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$API_BASE_URL$endpoint")
    elif [ "$method" == "POST" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$API_BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" == "PUT" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "$API_BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" == "DELETE" ]; then
        response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$API_BASE_URL$endpoint")
    fi

    http_status=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
    body=$(echo "$response" | sed -n '1,/HTTP_STATUS/p' | sed '$d')

    if [ "$http_status" -ge 200 ] && [ "$http_status" -lt 300 ]; then
        echo -e "${GREEN}✓ Success${NC} (Status: $http_status)"
    else
        echo -e "${RED}✗ Failed${NC} (Status: $http_status)"
    fi

    echo "Response: $body" | head -n 5
}

# 1. Check if API is running
echo -e "\n${YELLOW}1. Checking API Status...${NC}"
if curl -s --head --request GET "$API_BASE_URL/health" | grep "200" > /dev/null; then
    echo -e "${GREEN}✓ API is running${NC}"
else
    echo -e "${RED}✗ API is not responding${NC}"
    echo "Make sure your API server is running on $API_BASE_URL"
    exit 1
fi

# 2. Test GET all patients
test_endpoint "GET" "/patients" "" "Get all patients"

# 3. Test GET single patient
test_endpoint "GET" "/patients/1" "" "Get patient by ID"

# 4. Test POST create patient
patient_data='{
    "firstName": "Test",
    "lastName": "Patient",
    "dateOfBirth": "1990-01-01",
    "gender": "Male",
    "phone": "555-0123",
    "email": "test@example.com"
}'
test_endpoint "POST" "/patients" "$patient_data" "Create new patient"

# 5. Test PUT update patient
update_data='{
    "phone": "555-9999",
    "email": "updated@example.com"
}'
test_endpoint "PUT" "/patients/1" "$update_data" "Update patient"

# 6. Test DELETE patient
test_endpoint "DELETE" "/patients/999" "" "Delete patient"

# 7. Test appointments endpoint
test_endpoint "GET" "/appointments" "" "Get all appointments"

# 8. Test search functionality
test_endpoint "GET" "/patients/search?q=John" "" "Search patients"

echo -e "\n========================================="
echo "   API Testing Complete"
echo "========================================="