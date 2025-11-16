# Phase 13: Deployment Guide

**Phase:** 13 - Predictive Analytics & ML Models
**Version:** 1.0
**Last Updated:** 2025-10-31

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Deployment Steps](#deployment-steps)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Procedures](#rollback-procedures)
9. [Monitoring](#monitoring)

---

## Prerequisites

### System Requirements

- **Operating System:** Linux (Ubuntu 20.04+ recommended) or WSL2
- **Python:** 3.10 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** Minimum 1GB free
- **CPU:** Multi-core recommended for faster training

### Required Software

```bash
# Python 3
python3 --version  # Should be 3.10+

# pip
pip3 --version

# Git (for version control)
git --version
```

### Access Requirements

- File system read/write access to deployment directory
- Sufficient permissions to install Python packages
- Network access (if deploying to remote servers)

---

## Environment Setup

### Option 1: Using System Python (with --break-system-packages)

```bash
# Install required packages
pip3 install --break-system-packages \
    scikit-learn \
    numpy \
    pandas \
    joblib \
    pytest \
    pytest-cov
```

### Option 2: Using Virtual Environment (Recommended for Development)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install required packages
pip install scikit-learn numpy pandas joblib pytest pytest-cov

# Verify installation
python -c "import sklearn, numpy, pandas, joblib; print('All packages installed')"
```

### Option 3: Using Docker (Recommended for Production)

```dockerfile
# Dockerfile (if not exists, create this)
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    scikit-learn==1.7.2 \
    numpy==2.3.4 \
    pandas==2.3.3 \
    joblib==1.5.2 \
    pytest==8.4.2 \
    pytest-cov==7.0.0

# Copy phase files
COPY . /app/

# Run tests on build
RUN python -m pytest tests/ -v

CMD ["python", "code/implementation.py"]
```

```bash
# Build Docker image
docker build -t swarmcare-phase13:latest .

# Run container
docker run -v $(pwd)/models:/app/models swarmcare-phase13:latest
```

---

## Installation

### Step 1: Clone/Copy Phase Files

```bash
# Navigate to SwarmCare project
cd /path/to/SwarmCare/SwarmCare_Production/phases/phase13

# Verify structure
ls -la
# Should see: code/, tests/, models/, docs/, deliverables/, .state/
```

### Step 2: Install Dependencies

```bash
# Verify Python version
python3 --version

# Install required packages
pip3 install --break-system-packages -r requirements.txt
# OR manually:
pip3 install --break-system-packages scikit-learn numpy pandas joblib pytest
```

### Step 3: Verify Installation

```bash
# Run quick verification
python3 -c "
from code.implementation import Phase13Implementation
impl = Phase13Implementation()
print('✅ Installation successful')
"
```

---

## Configuration

### Environment Variables (Optional)

```bash
# Set environment variables if using agent framework
export CONTENT_SAFETY_ENDPOINT="your-endpoint"  # Optional
export CONTENT_SAFETY_KEY="your-key"  # Optional

# These are optional - system works without them with graceful degradation
```

### Model Configuration

Models are pre-configured with production-ready hyperparameters:

**Readmission Model:**
- n_estimators: 100
- max_depth: 10
- min_samples_split: 5
- class_weight: balanced

**Length of Stay Model:**
- n_estimators: 100
- max_depth: 12
- min_samples_split: 5

**Mortality Model:**
- n_estimators: 100
- max_depth: 10
- min_samples_split: 5
- class_weight: balanced

To modify, edit `code/implementation.py` (lines 143-149, 204-210, 257-263).

---

## Deployment Steps

### Quick Deployment (Automated)

```bash
# One-command production deployment
bash deliverables/PRODUCTION_DEPLOYMENT.sh
```

This script will:
1. Run pre-deployment validation
2. Train all models
3. Execute comprehensive tests
4. Verify model persistence
5. Validate HIPAA compliance
6. Update phase state
7. Generate deployment report

### Manual Deployment (Step-by-Step)

#### Step 1: Pre-Deployment Validation

```bash
# Run automated validation
bash tests/automated_validation.sh
```

Expected output: `✓ PHASE 13: PRODUCTION READY - ALL VALIDATIONS PASSED`

#### Step 2: Train Models

```bash
# Train all three models
python3 code/implementation.py
```

Expected output:
```
✅ Readmission Model - ROC AUC: 0.9355
✅ Length of Stay Model - R²: 0.5056
✅ Mortality Risk Model - ROC AUC: 0.9967
RESULT: SUCCESS ✅
```

#### Step 3: Run Tests

```bash
# Execute comprehensive test suite
python3 tests/test_phase13.py
```

Expected output: `Tests Run: 27 | Success Rate: 100.00%`

#### Step 4: Verify Models

```bash
# Check models are saved
ls -lh models/
# Should see: readmission_model.pkl, los_model.pkl, mortality_model.pkl
```

#### Step 5: Update State

The implementation automatically updates `.state/phase_state.json` to COMPLETED status.

Verify:
```bash
cat .state/phase_state.json | grep status
# Should show: "status": "COMPLETED"
```

---

## Verification

### Quick Verification

```bash
# Run automated validation
bash tests/automated_validation.sh

# Expected: 36/36 checks passing
```

### Detailed Verification

#### 1. Model Verification

```python
# Python verification script
from code.implementation import Phase13Implementation
import joblib

# Load models
readmission = joblib.load('models/readmission_model.pkl')
los = joblib.load('models/los_model.pkl')
mortality = joblib.load('models/mortality_model.pkl')

# Verify models are trained
assert readmission.is_trained, "Readmission model not trained"
assert los.is_trained, "LOS model not trained"
assert mortality.is_trained, "Mortality model not trained"

print("✅ All models verified")
```

#### 2. Prediction Verification

```python
# Test predictions
impl = Phase13Implementation()

# Load existing models
impl.load_models()

# Generate test data
test_data = impl.generate_synthetic_data(n_samples=10)

# Make predictions
predictions = impl.predict_patient_outcomes(test_data)

# Verify predictions structure
assert 'readmission_risk' in predictions
assert 'length_of_stay_days' in predictions
assert 'mortality_risk' in predictions
assert predictions['patient_count'] == 10

print("✅ Predictions verified")
```

#### 3. HIPAA Compliance Verification

```python
# Verify HIPAA compliance
import pandas as pd

# Create test data with PHI
data_with_phi = pd.DataFrame({
    'patient_id': ['P001', 'P002'],
    'patient_name': ['John Doe', 'Jane Smith'],
    'ssn': ['123-45-6789', '987-65-4321'],
    'age': [45, 67],
    'gender': ['M', 'F'],
    'admission_type': ['Emergency', 'Elective'],
    'length_of_stay': [3, 5],
    'diagnosis_count': [2, 5],
    'procedure_count': [1, 3],
    'comorbidity_score': [4, 8],
    'previous_admissions': [0, 3]
})

# Anonymize
validator = impl.validator
anonymized = validator.anonymize_patient_data(data_with_phi)

# Verify PHI removed
assert 'patient_name' not in anonymized.columns
assert 'ssn' not in anonymized.columns
assert anonymized.iloc[0]['patient_id'] != 'P001'  # Should be hashed

print("✅ HIPAA compliance verified")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Package Installation Fails

**Error:** `externally-managed-environment`

**Solution:**
```bash
# Use --break-system-packages flag
pip3 install --break-system-packages <package-name>

# OR use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install <package-name>
```

#### Issue 2: Import Errors

**Error:** `ModuleNotFoundError: No module named 'sklearn'`

**Solution:**
```bash
# Verify packages installed
pip3 list | grep -E "scikit|numpy|pandas"

# Reinstall if needed
pip3 install --break-system-packages scikit-learn numpy pandas joblib
```

#### Issue 3: Framework Import Warnings

**Warning:** `⚠️ Framework init warning: CONTENT_SAFETY_ENDPOINT...`

**Solution:** This is expected and harmless. The system works with graceful degradation.
```python
# Optional: Set environment variables to suppress warning
export CONTENT_SAFETY_ENDPOINT="not-required"
export CONTENT_SAFETY_KEY="not-required"
```

#### Issue 4: Model Training Slow

**Symptom:** Training takes > 60 seconds

**Solution:**
```python
# Reduce n_estimators temporarily for testing
# Edit code/implementation.py

# Change from:
n_estimators=100

# To:
n_estimators=50  # Faster training for testing
```

#### Issue 5: Test Failures

**Error:** Tests fail after modification

**Solution:**
```bash
# Re-run tests with verbose output
python3 tests/test_phase13.py -v

# Check specific test
python3 -m pytest tests/test_phase13.py::TestClass::test_name -v

# Verify models exist
ls -la models/
```

---

## Rollback Procedures

### Scenario 1: Failed Deployment

```bash
# Stop current process
# Ctrl+C if running

# Check last known good state
cat .state/phase_state.json

# Restore from backup if needed
cp .state/phase_state.json.backup .state/phase_state.json

# Re-run deployment
bash deliverables/PRODUCTION_DEPLOYMENT.sh
```

### Scenario 2: Corrupt Models

```bash
# Remove corrupt models
rm models/*.pkl

# Retrain fresh models
python3 code/implementation.py

# Verify
ls -lh models/
python3 tests/test_phase13.py
```

### Scenario 3: Code Issues

```bash
# Revert to last commit (if using git)
git checkout HEAD -- code/implementation.py

# OR restore from backup
cp code/implementation.py.backup code/implementation.py

# Re-run tests
python3 tests/test_phase13.py
```

---

## Monitoring

### Production Monitoring Checklist

#### 1. Model Performance

```python
# Monitor model metrics
from code.implementation import Phase13Implementation

impl = Phase13Implementation()

# Get current stats
stats = impl.get_stats()
print(f"Models trained: {stats['models']}")
print(f"Status: {stats['status']}")
```

#### 2. Prediction Monitoring

```python
# Log all predictions for monitoring
import logging

logging.basicConfig(
    filename='predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Make predictions and log
predictions = impl.predict_patient_outcomes(patient_data)
logging.info(f"Predictions made: {predictions['patient_count']}")
```

#### 3. Error Monitoring

```bash
# Monitor error logs
tail -f /var/log/phase13/errors.log

# Or check recent errors
grep "ERROR" /var/log/phase13/*.log | tail -20
```

#### 4. System Health

```bash
# Check disk space for models
du -sh models/

# Check memory usage
free -h

# Monitor CPU during training
top -p $(pgrep -f implementation.py)
```

### Automated Monitoring

```bash
# Schedule periodic validation (cron job example)
# Add to crontab: crontab -e

# Run validation every hour
0 * * * * cd /path/to/phase13 && bash tests/automated_validation.sh >> /var/log/phase13/validation.log 2>&1

# Weekly full deployment test
0 0 * * 0 cd /path/to/phase13 && bash deliverables/PRODUCTION_DEPLOYMENT.sh >> /var/log/phase13/weekly_test.log 2>&1
```

---

## Production Best Practices

### 1. Data Handling

- ✅ Always anonymize patient data before processing
- ✅ Validate all inputs before model inference
- ✅ Log all data processing operations
- ✅ Monitor for data quality issues

### 2. Model Management

- ✅ Version control models with timestamps
- ✅ Monitor model performance over time
- ✅ Retrain periodically with new data
- ✅ Validate models before deployment

### 3. Security

- ✅ Restrict access to model files
- ✅ Encrypt sensitive data at rest
- ✅ Use TLS for data in transit (if applicable)
- ✅ Regular security audits

### 4. Compliance

- ✅ Maintain HIPAA compliance
- ✅ Document all data processing
- ✅ Audit trail for all operations
- ✅ Regular compliance reviews

---

## Support & Resources

### Documentation

- **Implementation Guide:** `docs/IMPLEMENTATION_GUIDE.md`
- **Execution Summary:** `deliverables/EXECUTION_SUMMARY.md`
- **Verification Report:** `deliverables/VERIFICATION_REPORT.md`
- **Deliverables Manifest:** `deliverables/DELIVERABLES_MANIFEST.md`

### Testing

- **Run All Tests:** `python3 tests/test_phase13.py`
- **Automated Validation:** `bash tests/automated_validation.sh`
- **Production Deployment:** `bash deliverables/PRODUCTION_DEPLOYMENT.sh`

### Contact

For deployment issues or questions:
1. Check troubleshooting section above
2. Review verification report
3. Run automated validation
4. Check logs for detailed error messages

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2025-10-31
**Status:** ✅ Production Ready
