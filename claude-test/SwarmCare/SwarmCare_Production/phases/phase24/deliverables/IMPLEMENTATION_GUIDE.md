# Phase 24: Implementation Guide
## Detailed Usage and API Documentation

**Version**: 1.0.0  
**Last Updated**: October 31, 2025

---

## Quick Start

### Installation
```bash
# Navigate to phase24 directory
cd /path/to/SwarmCare/phases/phase24

# Install dependencies (if needed)
pip install -r requirements.txt

# Make scripts executable
chmod +x deliverables/*.py deliverables/*.sh
```

### First Run
```bash
# 1. Setup EHR integrations
python3 deliverables/setup_ehr_integrations.py --test

# 2. Validate connections
python3 deliverables/validate_ehr_connections.py --detailed

# 3. Generate sample billing report
python3 deliverables/generate_billing_reports.py --encounters 10
```

---

## Production Scripts Documentation

### 1. setup_ehr_integrations.py

**Purpose**: Configure connections to all 11 EHR systems (100% market coverage)

**Usage**:
```bash
python3 setup_ehr_integrations.py [OPTIONS]
```

**Options**:
- `--system SYSTEM` - Setup specific EHR system (default: all)
- `--test` - Test connections after setup
- `--verbose` - Enable verbose logging
- `--output FILE` - Save configuration to file (default: ehr_configuration.json)

**Examples**:
```bash
# Setup all systems with testing
python3 setup_ehr_integrations.py --test

# Setup only Epic
python3 setup_ehr_integrations.py --system Epic --verbose

# Setup and save to custom file
python3 setup_ehr_integrations.py --output /path/to/config.json
```

**Output**: JSON configuration file with all system details

---

### 2. generate_billing_reports.py

**Purpose**: Generate comprehensive billing reports and analytics

**Usage**:
```bash
python3 generate_billing_reports.py [OPTIONS]
```

**Options**:
- `--encounters N` - Number of encounters to process (default: 100)
- `--format FORMAT` - Output format: json, csv, all (default: json)
- `--output DIR` - Output directory (default: ./reports)
- `--summary` - Generate summary report only
- `--verbose` - Enable verbose logging

**Examples**:
```bash
# Generate report for 100 encounters in JSON
python3 generate_billing_reports.py --encounters 100

# Generate all formats for 200 encounters
python3 generate_billing_reports.py --encounters 200 --format all

# Generate summary only
python3 generate_billing_reports.py --summary
```

**Output**: Billing reports with claims, charges, and analytics

---

### 3. validate_ehr_connections.py

**Purpose**: Validate EHR connections and perform health checks

**Usage**:
```bash
python3 validate_ehr_connections.py [OPTIONS]
```

**Options**:
- `--system SYSTEM` - Validate specific system (default: all)
- `--timeout SECONDS` - Connection timeout (default: 30)
- `--detailed` - Show detailed validation results
- `--output FILE` - Save results to file (JSON)
- `--continuous` - Run continuous monitoring
- `--interval SECONDS` - Monitoring interval (default: 60)

**Examples**:
```bash
# Validate all systems
python3 validate_ehr_connections.py --detailed

# Continuous monitoring
python3 validate_ehr_connections.py --continuous --interval 300

# Validate single system and save
python3 validate_ehr_connections.py --system Epic --output epic_validation.json
```

**Output**: Validation report with health status for each system

---

### 4. export_integration_data.py

**Purpose**: Export EHR and billing data in multiple formats

**Usage**:
```bash
python3 export_integration_data.py [OPTIONS]
```

**Options**:
- `--data-type TYPE` - Data type: encounters, billing, codes, all
- `--format FORMAT` - Export format: json, csv, hl7, fhir, all
- `--output-dir DIR` - Output directory (default: ./exports)
- `--encounters N` - Number of encounters (default: 100)
- `--include-metadata` - Include metadata in exports
- `--compress` - Compress output files (gzip)

**Examples**:
```bash
# Export FHIR bundle
python3 export_integration_data.py --format fhir --encounters 50

# Export all formats with compression
python3 export_integration_data.py --format all --compress

# Export with metadata
python3 export_integration_data.py --format json --include-metadata
```

**Output**: Exported data files in specified formats

---

### 5. create_phase24_package.sh

**Purpose**: Create deployment-ready package

**Usage**:
```bash
./create_phase24_package.sh [OPTIONS]
```

**Options**:
- `--output-dir DIR` - Output directory (default: ./dist)
- `--skip-tests` - Skip test execution
- `--verbose` - Enable verbose output
- `--include-source` - Include source code in package

**Examples**:
```bash
# Create standard package
./create_phase24_package.sh

# Create package with source code
./create_phase24_package.sh --include-source

# Create without running tests
./create_phase24_package.sh --skip-tests --output-dir /tmp/dist
```

**Output**: Compressed tarball with all deliverables and checksums

---

## Python API Documentation

### EHRIntegrationEngine Class

```python
from code.implementation import EHRIntegrationEngine

# Initialize engine
engine = EHRIntegrationEngine()

# Integrate all systems
result = engine.integrate_all_systems()
print(f"Connected to {result['connected_count']} systems")

# Verify connections
status = engine.verify_all_connections()
for system, details in status.items():
    print(f"{system}: {details['connected']}")
```

### AutomatedCodingSystem Class

```python
from code.implementation import AutomatedCodingSystem

# Initialize coding system
coder = AutomatedCodingSystem()

# Generate codes for encounters
codes = coder.generate_codes_for_encounters(encounter_count=100)
print(f"Generated {codes['total_codes']} codes")
print(f"Accuracy: {codes['coding_accuracy']}")

# Validate codes
validation = coder.validate_codes(['I10', 'E11.9', '99213'])
print(f"Valid codes: {validation['valid_codes']}")
```

### BillingEngine Class

```python
from code.implementation import BillingEngine

# Initialize billing engine
billing = BillingEngine()

# Generate billing records
records = billing.generate_billing_records(encounter_count=100)
print(f"Total value: ${records['total_value']}")
print(f"Average claim: ${records['avg_claim_value']}")
```

---

## Configuration

### Environment Variables
```bash
# Database
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=swarmcare

# EHR Credentials
export EPIC_CLIENT_ID=your_client_id
export EPIC_CLIENT_SECRET=your_secret
export CERNER_API_KEY=your_api_key

# Logging
export LOG_LEVEL=INFO
export LOG_FILE=/var/log/swarmcare/phase24.log
```

### Configuration Files

See `configuration_templates.json` for complete templates.

---

## Error Handling

All scripts include comprehensive error handling:
```python
try:
    result = engine.integrate_all_systems()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
except AuthenticationError as e:
    logger.error(f"Authentication failed: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

---

## Best Practices

1. **Always validate connections** before processing
2. **Use verbose mode** during initial setup
3. **Monitor logs** for errors and warnings
4. **Save configurations** for reproducibility
5. **Test with small datasets** before production runs
6. **Enable compression** for large exports
7. **Use continuous monitoring** in production

---

For more details, see:
- EHR_INTEGRATION_GUIDE.md for EHR-specific details
- BILLING_SYSTEM_GUIDE.md for billing workflows
- DEPLOYMENT_GUIDE.md for production deployment
