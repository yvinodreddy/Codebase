# FHIR Healthcare API - MCP Integration Quick Start

## 🎉 SUCCESS - API is LIVE and READY!

**Base URL**: `https://localhost:7012`
**Status**: ✅ Running with 85 test resources seeded
**Swagger**: https://localhost:7012/swagger

---

## ✅ Verified Working Endpoints

### Quick Data Verification
```bash
# Verify all test data
curl -k https://localhost:7012/api/public-test/verify-data

# Get specific patient (Sarah Johnson)
curl -k https://localhost:7012/api/public-test/patient/1

# View all available endpoints
curl -k https://localhost:7012/swagger/v1/swagger.json
```

### Core FHIR Resources (MCP Ready)

#### Patients
```bash
# Get patient by ID
GET https://localhost:7012/api/fhir/Patient/1
GET https://localhost:7012/api/public-test/patient/1

# Search patients
POST https://localhost:7012/api/fhir/Patient/search
```

#### Observations (Vital Signs & Labs)
```bash
# Get all observations for a patient
GET https://localhost:7012/api/fhir/Observation/patient/1

# View observations for all patients
GET https://localhost:7012/api/public-test/all-data
```

#### Conditions (Diagnoses)
```bash
# Get active conditions
GET https://localhost:7012/api/fhir/Condition/patient/1/active

# Get condition history
GET https://localhost:7012/api/fhir/Condition/patient/1/history

# Get conditions via public test endpoint
GET https://localhost:7012/api/public-test/conditions/1
```

#### Medications
```bash
# Get patient medications
GET https://localhost:7012/api/fhir/Medication/patient/1
```

#### Care Plans
```bash
# Get patient care plans
GET https://localhost:7012/api/public-test/care-plans/1
```

### Clinical Decision Support
```bash
# Comprehensive health check
POST https://localhost:7012/api/fhir/decision-support/comprehensive-check

# Check drug interactions
POST https://localhost:7012/api/fhir/decision-support/check-interactions

# Find care gaps
GET https://localhost:7012/api/clinical-decision-support/alerts/{patientId}

# Get clinical analysis
GET https://localhost:7012/api/clinical-decision-support/analysis/{patientId}
```

### Live Terminology Validation
```bash
# RxNorm Drug Lookup
GET https://localhost:7012/api/rxnorm-live/drug/197361
GET https://localhost:7012/api/rxnorm-live/search?drugName=aspirin

# Drug Interaction Check
POST https://localhost:7012/api/rxnorm-live/interactions
Body: ["197361", "860975"]

# LOINC Lab Test Lookup
GET https://localhost:7012/api/loinc-current/1558-6

# SNOMED Condition Lookup
GET https://localhost:7012/api/snomed-test/validate/38341003
```

### Knowledge Graph Queries
```bash
# Patient summary graph
POST https://localhost:7012/api/knowledge-graph/patient/1/convert

# Related medications
GET https://localhost:7012/api/knowledge-graph/medications/197361/related

# Related conditions
GET https://localhost:7012/api/knowledge-graph/conditions/38341003/related
```

### System Health Monitoring
```bash
# API Health
GET https://localhost:7012/health

# Performance Metrics
GET https://localhost:7012/api/monitoring/performance

# System Status
GET https://localhost:7012/api/monitoring/status
```

---

## 📊 Seeded Test Data

| Patient ID | Name | Age | Conditions | Medications | Care Plan |
|-----------|------|-----|------------|-------------|-----------|
| 1 | Sarah Johnson | 40 | Hypertension | Lisinopril 10mg | ✓ |
| 2 | Michael Chen | 53 | Type 2 Diabetes | Metformin 500mg | ✓ |
| 3 | Emily Rodriguez | 35 | COPD | Albuterol Inhaler | ✓ |
| 4 | James Williams | 60 | Asthma | Atorvastatin 20mg | - |
| 5 | Maria Garcia | 47 | MI History | Aspirin 81mg | - |
| 6 | David Brown | 67 | - | - | - |
| 7 | Jennifer Davis | 30 | - | - | - |
| 8 | Robert Martinez | 43 | - | - | - |

**All patients** have complete vital signs and lab results:
- Blood Pressure
- Heart Rate
- Temperature
- Blood Glucose
- HbA1c
- Cholesterol Panel (Total, HDL, LDL)

---

## 🔌 MCP Bridge Configuration

### Option 1: Direct API Calls (No Auth Required for Test Endpoints)
```javascript
// In your MCP bridge server
const FHIR_BASE = "https://localhost:7012";

async function getPatient(patientId) {
  const response = await fetch(`${FHIR_BASE}/api/public-test/patient/${patientId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    // Disable SSL verification in development
    rejectUnauthorized: false
  });
  return response.json();
}

async function verifyData() {
  const response = await fetch(`${FHIR_BASE}/api/public-test/verify-data`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    rejectUnauthorized: false
  });
  return response.json();
}
```

### Option 2: Authenticated Endpoints (For Protected Resources)
```javascript
// 1. Register a user
const registerResponse = await fetch(`${FHIR_BASE}/api/Auth/register`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: "mcpbridge",
    password: "SecurePass123!",
    email: "mcp@example.com"
  }),
  rejectUnauthorized: false
});

// 2. Login to get token
const loginResponse = await fetch(`${FHIR_BASE}/api/Auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: "mcpbridge",
    password: "SecurePass123!"
  }),
  rejectUnauthorized: false
});

const { token } = await loginResponse.json();

// 3. Use token for protected endpoints
const patientResponse = await fetch(`${FHIR_BASE}/api/fhir/Patient/1`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  rejectUnauthorized: false
});
```

---

## 🧪 Quick Test Commands

### 1. Test API is running
```bash
curl -k https://localhost:7012/health
```

### 2. Verify test data
```bash
curl -k https://localhost:7012/api/public-test/verify-data | python3 -m json.tool
```

### 3. Get patient details
```bash
curl -k https://localhost:7012/api/public-test/patient/1 | python3 -m json.tool
```

### 4. Get patient observations
```bash
curl -k https://localhost:7012/api/fhir/Observation/patient/1 | python3 -m json.tool
```

### 5. Check drug interaction
```bash
curl -k https://localhost:7012/api/rxnorm-live/drug/197361 | python3 -m json.tool
```

---

## 🎯 MCP Integration Examples

### Example 1: Get Patient Medical Record
```bash
# Step 1: Get patient demographics
curl -k https://localhost:7012/api/public-test/patient/1

# Step 2: Get active conditions
curl -k https://localhost:7012/api/fhir/Condition/patient/1/active

# Step 3: Get current medications
curl -k https://localhost:7012/api/fhir/Medication/patient/1

# Step 4: Get latest observations
curl -k https://localhost:7012/api/fhir/Observation/patient/1

# Step 5: Get care plan
curl -k https://localhost:7012/api/public-test/care-plans/1
```

### Example 2: Drug Safety Check
```bash
# Lookup drug information
curl -k https://localhost:7012/api/rxnorm-live/drug/197361

# Check for interactions with patient's current meds
curl -k -X POST https://localhost:7012/api/fhir/decision-support/check-interactions \
  -H "Content-Type: application/json" \
  -d '{"patientId": "1", "newMedicationRxcui": "860975"}'
```

### Example 3: Clinical Decision Support
```bash
# Get comprehensive clinical analysis
curl -k https://localhost:7012/api/clinical-decision-support/analysis/1
```

---

## 🚀 Next Steps for MCP Integration

1. **Point your bridge to**: `https://localhost:7012`
2. **Start with test endpoints**: Use `/api/public-test/*` endpoints (no auth required)
3. **Verify data accessibility**: Call `/api/public-test/verify-data`
4. **Test patient queries**: Try getting patient 1's complete record
5. **Add authentication**: Implement JWT auth for production endpoints
6. **Build MCP tools**: Map FHIR endpoints to MCP tool functions

---

## 📱 Available Claude Desktop MCP Tools

Here are suggested MCP tool definitions for your bridge:

```json
{
  "tools": [
    {
      "name": "get_patient",
      "description": "Get patient demographics and contact information",
      "inputSchema": {
        "type": "object",
        "properties": {
          "patientId": { "type": "string", "description": "Patient ID" }
        }
      }
    },
    {
      "name": "get_patient_conditions",
      "description": "Get patient's active medical conditions",
      "inputSchema": {
        "type": "object",
        "properties": {
          "patientId": { "type": "string" }
        }
      }
    },
    {
      "name": "get_patient_medications",
      "description": "Get patient's current medications",
      "inputSchema": {
        "type": "object",
        "properties": {
          "patientId": { "type": "string" }
        }
      }
    },
    {
      "name": "get_patient_vitals",
      "description": "Get patient's latest vital signs and lab results",
      "inputSchema": {
        "type": "object",
        "properties": {
          "patientId": { "type": "string" }
        }
      }
    },
    {
      "name": "check_drug_interactions",
      "description": "Check for drug-drug interactions",
      "inputSchema": {
        "type": "object",
        "properties": {
          "rxcuis": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Array of RxNorm CUI codes"
          }
        }
      }
    },
    {
      "name": "lookup_drug",
      "description": "Get drug information by RxNorm code",
      "inputSchema": {
        "type": "object",
        "properties": {
          "rxcui": { "type": "string", "description": "RxNorm CUI code" }
        }
      }
    },
    {
      "name": "clinical_decision_support",
      "description": "Get comprehensive clinical analysis for a patient",
      "inputSchema": {
        "type": "object",
        "properties": {
          "patientId": { "type": "string" }
        }
      }
    }
  ]
}
```

---

## ⚙️ Troubleshooting

### Issue: SSL Certificate Errors
**Solution**: Use `-k` flag with curl or `rejectUnauthorized: false` in Node.js

### Issue: CORS Errors
**Solution**: API has CORS enabled for all origins. If issues persist, check your browser/client settings.

### Issue: 404 Not Found
**Solution**: Check the exact endpoint path. Use `/swagger/v1/swagger.json` to see all available paths.

### Issue: Need to Reseed Data
```bash
curl -k https://localhost:7012/api/DataSeeding/seed
```

---

## 📞 Support Resources

- **Swagger UI**: https://localhost:7012/swagger (Interactive API documentation)
- **Health Check**: https://localhost:7012/health
- **Data Verification**: https://localhost:7012/api/public-test/verify-data
- **Full Endpoint List**: See API_VERIFICATION_REPORT.md

---

**API Status**: ✅ FULLY OPERATIONAL
**MCP Integration**: ✅ READY
**Test Data**: ✅ 85 RESOURCES SEEDED
**Last Updated**: 2025-10-26
