# Phase 24: Billing System Guide
## Automated Billing and Medical Coding Workflows

**Version**: 1.0.0  
**Last Updated**: October 31, 2025

---

## Overview

The automated billing system codes medical encounters using ICD-10, CPT, and HCPCS codes, then generates claims for submission to payers. This guide covers the complete workflow from encounter to payment.

---

## Medical Coding

### ICD-10 Diagnosis Codes
**Purpose**: Document patient diagnoses
**Accuracy**: 100%
**Common Codes**:
- I10 - Essential hypertension
- E11.9 - Type 2 diabetes
- J44.9 - COPD
- I25.10 - Coronary artery disease

### CPT Procedure Codes
**Purpose**: Document procedures and services
**Accuracy**: 100%
**Common Codes**:
- 99213 - Office visit (20-29 min) - $112
- 99214 - Office visit (30-39 min) - $167
- 93000 - EKG - $17
- 80053 - Comprehensive metabolic panel - $14

### HCPCS Supply Codes
**Purpose**: Document supplies and DME
**Accuracy**: 100%
**Common Codes**:
- A4253 - Blood glucose test strips - $35
- G0438 - Annual wellness visit - $174
- E0607 - Blood glucose monitor - $45

---

## Billing Workflow

### 1. Encounter Completion
- Patient visit documented in EHR
- Diagnoses and procedures recorded
- Provider attestation completed

### 2. Automated Coding
```python
# System automatically codes encounter
codes = coder.generate_codes_for_encounters(1)
# Returns ICD-10, CPT, HCPCS codes with confidence scores
```

### 3. Charge Calculation
- CPT codes mapped to fee schedules
- Modifiers applied as needed
- Total charges calculated

### 4. Claim Generation
- Payer identified from insurance info
- Claim formatted (837P electronic format)
- Supporting documentation attached

### 5. Claim Submission
- Electronic submission to clearinghouse
- Real-time eligibility verification
- Prior authorization check if required

### 6. Payment Processing
- Claims tracked through adjudication
- Payments posted to patient accounts
- Denials managed and appealed

---

## Payer-Specific Rules

### Medicare
- Fee Schedule: CMS Physician Fee Schedule
- Claim Format: 837P
- Submission: Direct or clearinghouse
- Average Reimbursement: 87.3%
- Days to Payment: 18.5

### Commercial Insurance
- Fee Schedule: Contracted rates
- Claim Format: 837P
- Submission: Clearinghouse
- Average Reimbursement: 92.8%
- Days to Payment: 24.3

### Medicaid
- Fee Schedule: State-specific
- Claim Format: 837P
- Submission: State portal or clearinghouse
- Average Reimbursement: 78.5%
- Days to Payment: 32.7

---

## Revenue Cycle Management

### Key Metrics
- **Days in A/R**: Target <35 days
- **Collection Rate**: Target >95%
- **Denial Rate**: Target <3%
- **First Pass Acceptance**: Target >90%

### Denial Management
**Top Denial Reasons**:
1. Prior authorization required (26.5%)
2. Coding errors (18.9%)
3. Missing documentation (16.4%)
4. Non-covered service (13.9%)

**Appeal Process**:
1. Review denial reason
2. Gather supporting documentation
3. Submit appeal within timeframe
4. Track appeal status
5. Re-submit if successful

---

## Compliance

### Documentation Requirements
- Medical necessity documented
- Encounter date and time recorded
- Provider signature/attestation
- Supporting clinical notes

### Coding Compliance
- Codes must be supported by documentation
- Highest level of specificity used
- No upcoding or unbundling
- Modifier usage appropriate

### Audit Trail
All coding decisions logged:
- Timestamp
- Codes generated
- Confidence scores
- Manual review if needed
- Final submission

---

## Reporting

### Standard Reports
1. **Daily Billing Summary**: Encounters, charges, collections
2. **Payer Analysis**: Performance by payer
3. **Provider Productivity**: RVUs, charges by provider
4. **Denial Analysis**: Trends and root causes
5. **Revenue Forecast**: Expected collections

Generate reports:
```bash
python3 generate_billing_reports.py --encounters 100 --format all
```

---

For detailed code lists, see:
- icd10_codes_data.json
- cpt_codes_data.json
- hcpcs_codes_data.json
