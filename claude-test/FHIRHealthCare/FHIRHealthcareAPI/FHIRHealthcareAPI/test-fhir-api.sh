#!/bin/bash

# FHIR Healthcare API Testing Script
# Usage: ./test-fhir-api.sh

API_URL="http://localhost:5079"
TOKEN=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================="
echo "  FHIR Healthcare API Testing Suite"
echo "========================================="

# Function to make authenticated requests
auth_request() {
    local method=$1
    local endpoint=$2
    local data=$3

    if [ -z "$TOKEN" ]; then
        echo -e "${RED}No token available. Please login first.${NC}"
        return 1
    fi

    if [ "$method" == "GET" ]; then
        curl -s -H "Authorization: Bearer $TOKEN" "$API_URL$endpoint"
    elif [ "$method" == "POST" ]; then
        curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint"
    fi
}

# 1. Test Login
echo -e "\n${YELLOW}1. Testing Authentication...${NC}"
echo "Attempting login with test credentials..."

# Try different user credentials
USERS=(
    '{"username":"admin","password":"admin"}'
    '{"username":"dr.smith","password":"Doctor123"}'
    '{"username":"test","password":"test123"}'
)

for user in "${USERS[@]}"; do
    echo "Trying: $user"
    response=$(curl -s -X POST "$API_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "$user")

    if echo "$response" | grep -q "token"; then
        TOKEN=$(echo "$response" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
        echo -e "${GREEN}✓ Login successful!${NC}"
        echo "Token received: ${TOKEN:0:20}..."
        break
    else
        echo -e "${YELLOW}Login failed for this user${NC}"
    fi
done

if [ -z "$TOKEN" ]; then
    echo -e "${RED}✗ Could not login with any test credentials${NC}"
    echo "Please check the user database or create a test user"
fi

# 2. Test Debug Headers
echo -e "\n${YELLOW}2. Testing Debug Headers Endpoint...${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/auth/debug-headers")
echo "$response" | head -n 10

# 3. Test Auth Verification
echo -e "\n${YELLOW}3. Testing Auth Verification...${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/auth/test-auth")
echo "$response" | head -n 10

# 4. Test FHIR Endpoints
echo -e "\n${YELLOW}4. Testing FHIR Endpoints...${NC}"

# Test Patient Search
echo -e "\n${BLUE}Testing Patient Search...${NC}"
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/fhir/patient/search?name=Smith")
http_status=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$http_status" == "200" ]; then
    echo -e "${GREEN}✓ Patient search successful${NC}"
else
    echo -e "${RED}✗ Patient search failed (Status: $http_status)${NC}"
fi

# Test Observation Endpoints
echo -e "\n${BLUE}Testing Observation Endpoints...${NC}"
endpoints=(
    "/api/observation/analytics/trends"
    "/api/observation/analytics/distribution"
    "/api/observation/search"
)

for endpoint in "${endpoints[@]}"; do
    echo "Testing: $endpoint"
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $TOKEN" \
        "$API_URL$endpoint")
    if [ "$response" == "200" ] || [ "$response" == "204" ]; then
        echo -e "${GREEN}✓ $endpoint - OK${NC}"
    else
        echo -e "${YELLOW}⚠ $endpoint - Status: $response${NC}"
    fi
done

# 5. Test Knowledge Graph Endpoints
echo -e "\n${YELLOW}5. Testing Knowledge Graph Endpoints...${NC}"
kg_endpoints=(
    "/api/knowledgegraph/search/conditions?query=diabetes"
    "/api/knowledgegraph/search/medications?query=aspirin"
    "/api/knowledgegraph/clinical-pathways"
)

for endpoint in "${kg_endpoints[@]}"; do
    echo "Testing: $endpoint"
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $TOKEN" \
        "$API_URL$endpoint")
    if [ "$response" == "200" ] || [ "$response" == "204" ]; then
        echo -e "${GREEN}✓ $endpoint - OK${NC}"
    else
        echo -e "${YELLOW}⚠ $endpoint - Status: $response${NC}"
    fi
done

# 6. Test Machine Learning Endpoints
echo -e "\n${YELLOW}6. Testing Machine Learning Endpoints...${NC}"
ml_endpoints=(
    "/api/predictivehealth/risk-assessment/patient123"
    "/api/predictivehealth/readmission-risk/patient123"
)

for endpoint in "${ml_endpoints[@]}"; do
    echo "Testing: $endpoint"
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $TOKEN" \
        "$API_URL$endpoint")
    if [ "$response" == "200" ] || [ "$response" == "204" ]; then
        echo -e "${GREEN}✓ $endpoint - OK${NC}"
    else
        echo -e "${YELLOW}⚠ $endpoint - Status: $response${NC}"
    fi
done

# 7. Check Available Endpoints
echo -e "\n${YELLOW}7. Checking All Available Endpoints...${NC}"
echo "Attempting to list all available routes..."

# Try common documentation endpoints
doc_endpoints=(
    "/swagger"
    "/swagger/index.html"
    "/api"
    "/api-docs"
    "/"
)

for endpoint in "${doc_endpoints[@]}"; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL$endpoint")
    if [ "$response" == "200" ]; then
        echo -e "${GREEN}✓ Documentation found at: $endpoint${NC}"
    fi
done

echo -e "\n========================================="
echo "   API Testing Complete"
echo "========================================="
echo -e "\n${BLUE}Summary:${NC}"
echo "- API URL: $API_URL"
echo "- Authentication: $([ -n "$TOKEN" ] && echo "✓ Working" || echo "✗ Not working")"
echo -e "\n${YELLOW}Note:${NC} Some endpoints may require additional setup:"
echo "- Database connections (GraphDB, Redis, Elasticsearch)"
echo "- Message queue (RabbitMQ)"
echo "- Sample data in the database"
echo ""
echo "Check the .env and appsettings.json files for configuration."