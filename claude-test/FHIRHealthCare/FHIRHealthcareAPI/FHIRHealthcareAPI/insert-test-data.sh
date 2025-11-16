#!/bin/bash

# FHIR Healthcare API - Test Data Insertion Script
# This script inserts all the test data records

API_URL="http://localhost:5079"
TOKEN=""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================="
echo "  FHIR Healthcare API - Test Data Setup"
echo "========================================="

# First, let's try to get a token if needed
echo -e "\n${YELLOW}Checking if authentication is required...${NC}"

# Test if endpoints require authentication
TEST_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$API_URL/api/fhir/Observation/glucose" -X POST -H "Content-Type: application/json" -d '{"test":"test"}' 2>/dev/null)
HTTP_CODE=$(echo "$TEST_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)

if [ "$HTTP_CODE" == "401" ] || [ "$HTTP_CODE" == "403" ]; then
    echo -e "${YELLOW}Authentication required. Please provide token or credentials.${NC}"
    # Try to login with common test credentials
    # You may need to modify these credentials
    echo "Attempting to login..."

    # Add your login logic here if needed
    # TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}' | grep -o '"token":"[^"]*' | cut -d'"' -f4)
else
    echo -e "${GREEN}No authentication required or using default auth.${NC}"
fi

# Function to make API calls
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4

    echo -e "\n${BLUE}$description${NC}"

    if [ -n "$TOKEN" ]; then
        RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X "$method" "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d "$data" 2>/dev/null)
    else
        RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X "$method" "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    fi

    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
    BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

    if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "201" ] || [ "$HTTP_CODE" == "204" ]; then
        echo -e "${GREEN}✓ Success (Status: $HTTP_CODE)${NC}"
        if [ -n "$BODY" ]; then
            echo "Response: $BODY" | head -n 3
        fi
    else
        echo -e "${RED}✗ Failed (Status: $HTTP_CODE)${NC}"
        echo "Response: $BODY" | head -n 3
    fi
}

echo -e "\n${YELLOW}=== INSERTING OBSERVATION RECORDS ===${NC}"

# 1. Glucose observation (non-fasting)
make_request "POST" "/api/fhir/Observation/glucose" \
'{
  "patientId": "1",
  "glucoseValue": 145,
  "isFasting": false,
  "measuredAt": "2024-01-25T08:00:00Z"
}' "Creating glucose observation (non-fasting) - Record ID: 2"

# 2. Glucose observation (fasting)
make_request "POST" "/api/fhir/Observation/glucose" \
'{
  "patientId": "1",
  "glucoseValue": 110,
  "isFasting": true,
  "measuredAt": "2024-01-26T06:00:00Z"
}' "Creating glucose observation (fasting) - Record ID: 3"

# 3. Blood pressure observation
make_request "POST" "/api/fhir/Observation/blood-pressure" \
'{
  "patientId": "1",
  "systolic": 138,
  "diastolic": 88,
  "measuredAt": "2024-01-26T09:00:00Z"
}' "Creating blood pressure observation - Record ID: 4"

# 4. HbA1c observation
make_request "POST" "/api/fhir/Observation/hba1c" \
'{
  "patientId": "1",
  "hbA1cPercentage": 7.2,
  "measuredAt": "2024-01-15T10:00:00Z"
}' "Creating HbA1c observation - Record ID: 5"

echo -e "\n${YELLOW}=== INSERTING CONDITION RECORDS ===${NC}"

# 5. Hyperlipidemia condition
make_request "POST" "/api/fhir/Condition" \
'{
  "patientId": "1",
  "conditionName": "Hyperlipidemia",
  "snomedCode": "55822004",
  "icd10Code": "E78.5",
  "onsetDate": "2019-01-10",
  "clinicalStatus": "active",
  "severity": "moderate",
  "supportingObservationIds": ["2","3","4"]
}' "Creating Hyperlipidemia condition - Record ID: 6"

# 6. Diabetes condition
make_request "POST" "/api/fhir/Condition/diabetes" \
'{
  "patientId": "1",
  "onsetDate": "2018-06-15",
  "withComplications": false,
  "supportingObservationIds": ["2","3","5"]
}' "Creating Diabetes condition - Record ID: 7"

# 7. Hypertension condition
make_request "POST" "/api/fhir/Condition/hypertension" \
'{
  "patientId": "1",
  "stage": "2",
  "onsetDate": "2015-03-20",
  "supportingObservationIds": ["4"]
}' "Creating Hypertension condition - Record ID: 8"

echo -e "\n${YELLOW}=== INSERTING VALIDATED LAB RECORDS ===${NC}"

# 8. Lab record 1
make_request "POST" "/api/validated-lab/record" \
'{
  "patientId": "1",
  "loincCode": "33747-0",
  "value": 95.5,
  "unit": "mg/dL",
  "interpretation": "Normal"
}' "Creating lab record (LOINC: 33747-0) - Record ID: 9"

# 9. Lab record 2
make_request "POST" "/api/validated-lab/record" \
'{
  "patientId": "1",
  "loincCode": "2085-9",
  "value": 220,
  "unit": "mg/dL",
  "interpretation": "High"
}' "Creating lab record (LOINC: 2085-9) - Record ID: 10"

# 10. Lab record 3
make_request "POST" "/api/validated-lab/record" \
'{
  "patientId": "1",
  "loincCode": "2160-0",
  "value": 1.2,
  "unit": "mg/dL",
  "interpretation": "Normal"
}' "Creating lab record (LOINC: 2160-0) - Record ID: 11"

# 11. Lab record 4 (duplicate LOINC code)
make_request "POST" "/api/validated-lab/record" \
'{
  "patientId": "1",
  "loincCode": "2160-0",
  "value": 1.2,
  "unit": "mg/dL",
  "interpretation": "Normal"
}' "Creating lab record (LOINC: 2160-0 duplicate) - Record ID: 12"

echo -e "\n${YELLOW}=== INSERTING MEDICATION RECORDS ===${NC}"

# 12. Metformin prescription
make_request "POST" "/api/fhir/Medication/prescribe-validated" \
'{
  "patientId": "1",
  "medicationName": "Metformin",
  "rxNormCode": "6809",
  "dosageInstructions": "500mg twice daily with meals",
  "refills": 5
}' "Prescribing Metformin - Record ID: 13"

# 13. Lisinopril prescription (validated)
make_request "POST" "/api/fhir/Medication/prescribe-validated" \
'{
  "patientId": "1",
  "medicationName": "Lisinopril",
  "rxNormCode": "29046",
  "dosageInstructions": "10mg once daily",
  "refills": 3
}' "Prescribing Lisinopril (validated) - Record ID: 14"

# 14. Atorvastatin prescription
make_request "POST" "/api/fhir/Medication/prescribe" \
'{
  "patientId": "1",
  "medicationName": "Atorvastatin",
  "rxNormCode": "83367",
  "dosageInstructions": "40mg once daily at bedtime",
  "refills": 6
}' "Prescribing Atorvastatin - Record ID: 15"

# 15. Lisinopril prescription (duplicate)
make_request "POST" "/api/fhir/Medication/prescribe" \
'{
  "patientId": "1",
  "medicationName": "Lisinopril",
  "rxNormCode": "29046",
  "dosageInstructions": "10mg once daily",
  "refills": 3
}' "Prescribing Lisinopril (duplicate) - Record ID: 16"

echo -e "\n${YELLOW}=== CREATING CARE PLANS ===${NC}"

# 16. Diabetes care plan
make_request "POST" "/api/care-plan/diabetes" \
'{
  "patientId": "1",
  "conditionId": "6",
  "practitionerId": "dr-Smith-001"
}' "Creating Diabetes care plan - Record ID: 17"

# 17. Hypertension care plan
make_request "POST" "/api/care-plan/hypertension" \
'{
  "patientId": "1",
  "conditionId": "8",
  "practitionerId": "dr-Smith-001",
  "currentSystolic": 138,
  "currentDiastolic": 88
}' "Creating Hypertension care plan - Record ID: 18"

echo -e "\n${YELLOW}=== SUMMARY ===${NC}"
echo "Test data insertion complete!"
echo "Total records to be created: 18"
echo ""
echo "Note: If any records failed, please check:"
echo "1. API is running on $API_URL"
echo "2. Authentication is properly configured"
echo "3. Database connections are active"
echo "4. Patient with ID '1' exists in the system"