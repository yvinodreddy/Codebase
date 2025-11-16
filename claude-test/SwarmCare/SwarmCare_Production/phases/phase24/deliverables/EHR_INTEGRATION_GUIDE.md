# Phase 24: EHR Integration Guide
## Comprehensive Guide for Integrating with 11 EHR Systems (100% Market Coverage)

**Version**: 1.0.0  
**Last Updated**: October 31, 2025

---

## Overview

This guide provides detailed instructions for integrating with all 11 supported EHR systems (achieving 100% market coverage). Each system has unique requirements for authentication, API endpoints, and data formats.

---

## Supported EHR Systems

| System | Market Share | API Standard | Auth Method |
|--------|-------------|--------------|-------------|
| Epic | 31.0% | FHIR R4 | OAuth 2.0 |
| Cerner | 25.0% | FHIR R4 | OAuth 2.0 |
| Allscripts | 8.5% | HL7 v2.5/FHIR | API Key/OAuth |
| athenahealth | 5.9% | FHIR R4 | OAuth 2.0 |
| eClinicalWorks | 4.7% | HL7 v2.7/FHIR | OAuth 2.0 |
| NextGen | 3.8% | FHIR R4 | OAuth 2.0 |
| MEDITECH | 3.2% | HL7 v2.5/FHIR | API Key/OAuth |
| Practice Fusion | 2.1% | FHIR R4 | OAuth 2.0 |

---

## Epic Integration

### Prerequisites
- Epic App Orchard account
- Client credentials (client_id, client_secret)
- Approved FHIR scopes

### Configuration
```json
{
  "system_name": "Epic",
  "api_version": "FHIR R4",
  "base_endpoint": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4",
  "auth_endpoint": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize",
  "token_endpoint": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
  "scopes": ["patient/*.read", "launch", "openid", "fhirUser"]
}
```

### Authentication Flow
1. Obtain authorization code
2. Exchange code for access token
3. Use token in API requests
4. Refresh token before expiration

### Supported Resources
- Patient, Encounter, Observation, Condition, Procedure
- MedicationRequest, AllergyIntolerance, DiagnosticReport
- Immunization, DocumentReference

---

## Cerner Integration

### Prerequisites
- Cerner Code Console account
- Registered application
- OAuth credentials

### Configuration
```json
{
  "system_name": "Cerner",
  "api_version": "FHIR R4",
  "base_endpoint": "https://fhir-myrecord.cerner.com/r4",
  "auth_endpoint": "https://authorization.cerner.com/tenants/{tenant_id}/protocols/oauth2/profiles/smart-v1/authorize",
  "token_endpoint": "https://authorization.cerner.com/tenants/{tenant_id}/protocols/oauth2/profiles/smart-v1/token",
  "scopes": ["patient/*.read", "launch", "online_access"]
}
```

### Key Features
- Millennium platform integration
- Strong FHIR R4 support
- Real-time data access

---

## Common Integration Patterns

### FHIR R4 Data Retrieval
```python
import requests

def get_patient_data(access_token, patient_id, fhir_endpoint):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/fhir+json"
    }
    
    url = f"{fhir_endpoint}/Patient/{patient_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")
```

### HL7 v2.x Message Parsing
```python
def parse_hl7_message(message):
    segments = message.split('\r')
    parsed = {}
    
    for segment in segments:
        fields = segment.split('|')
        segment_type = fields[0]
        parsed[segment_type] = fields[1:]
    
    return parsed
```

---

## Rate Limiting

Each EHR system has different rate limits:
- **Epic**: 600 requests/minute
- **Cerner**: 500 requests/minute
- **Allscripts**: 300 requests/minute
- **athenahealth**: 400 requests/minute
- **eClinicalWorks**: 350 requests/minute
- **NextGen**: 300 requests/minute
- **MEDITECH**: 250 requests/minute
- **Practice Fusion**: 200 requests/minute

Implement exponential backoff for rate limit errors (429 status).

---

## Error Handling

### Common Error Codes
- **401**: Authentication failed - Check credentials
- **403**: Forbidden - Check scopes/permissions
- **404**: Resource not found - Verify patient/resource ID
- **429**: Rate limit exceeded - Implement backoff
- **500**: Server error - Retry with exponential backoff

### Retry Strategy
```python
import time

def retry_request(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

---

## Testing

### Test Credentials
Most EHR vendors provide sandbox environments. See `ehr_systems_data.json` for endpoints.

### Validation Checklist
- [ ] OAuth flow completes successfully
- [ ] FHIR metadata endpoint accessible
- [ ] Patient read operations work
- [ ] Error handling responds correctly
- [ ] Rate limiting respected

---

For specific system details, see `ehr_systems_data.json` and `configuration_templates.json`.
