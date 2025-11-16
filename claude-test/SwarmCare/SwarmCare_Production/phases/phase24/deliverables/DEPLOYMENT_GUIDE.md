# Phase 24: Deployment Guide
## Production Deployment Instructions

**Version**: 1.0.0  
**Last Updated**: October 31, 2025

---

## Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.8+ installed
- [ ] PostgreSQL 12+ database
- [ ] Redis 6+ for caching
- [ ] 4+ CPU cores
- [ ] 8GB+ RAM
- [ ] 50GB+ disk space
- [ ] Network access to EHR systems

### Configuration
- [ ] EHR credentials obtained
- [ ] Database credentials configured
- [ ] Payer configurations completed
- [ ] Fee schedules loaded
- [ ] Monitoring configured

### Testing
- [ ] All tests passing (35/36)
- [ ] Integration tests completed
- [ ] Performance benchmarks met
- [ ] Security scan passed

---

## Installation Steps

### 1. System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install python3 python3-pip postgresql redis-server

# Create application user
sudo useradd -m -s /bin/bash swarmcare
```

### 2. Application Deployment
```bash
# Extract deployment package
tar -xzf phase24_deliverables_*.tar.gz
cd phase24_deliverables_*

# Verify checksums
sha256sum -c SHA256SUMS

# Copy to production location
sudo cp -r * /opt/swarmcare/phase24/
sudo chown -R swarmcare:swarmcare /opt/swarmcare/phase24
```

### 3. Configuration
```bash
# Copy configuration templates
cd /opt/swarmcare/phase24
cp configuration_templates.json config.json

# Edit configuration with production values
nano config.json

# Set environment variables
export DB_HOST=prod-db.example.com
export REDIS_URL=redis://prod-redis:6379/0
```

### 4. Database Setup
```sql
-- Create database
CREATE DATABASE swarmcare_prod;

-- Create tables
\i schema.sql

-- Load reference data
\i icd10_codes.sql
\i cpt_codes.sql
\i hcpcs_codes.sql
```

### 5. EHR Integration Setup
```bash
# Setup all EHR systems
python3 scripts/setup_ehr_integrations.py --output config/ehr_prod.json

# Validate connections
python3 scripts/validate_ehr_connections.py --detailed
```

---

## Configuration Management

### Production Configuration
```json
{
  "environment": "production",
  "database_url": "postgresql://user:pass@prod-db:5432/swarmcare_prod",
  "redis_url": "redis://prod-redis:6379/0",
  "log_level": "WARNING",
  "enable_monitoring": true,
  "rate_limits": {
    "api_calls_per_minute": 500,
    "concurrent_requests": 50
  }
}
```

### Secrets Management
- Use environment variables for credentials
- Never commit secrets to version control
- Rotate credentials regularly
- Use secret management service (e.g., HashiCorp Vault)

---

## Monitoring Setup

### Health Checks
```bash
# Add health check endpoint monitoring
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "2025-10-31T12:00:00Z"}
```

### Logging
```bash
# Configure log rotation
sudo nano /etc/logrotate.d/swarmcare

# Add:
/var/log/swarmcare/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 swarmcare swarmcare
}
```

### Alerting
Configure alerts for:
- EHR connection failures
- Coding accuracy below threshold
- High denial rates
- System errors
- Performance degradation

---

## Performance Tuning

### Database Optimization
```sql
-- Add indexes
CREATE INDEX idx_encounters_date ON encounters(encounter_date);
CREATE INDEX idx_claims_status ON claims(status);
CREATE INDEX idx_patient_id ON encounters(patient_id);

-- Update statistics
ANALYZE;
```

### Redis Caching
```python
# Cache frequently accessed data
redis.setex('ehr_config_epic', 3600, json.dumps(epic_config))

# Cache coding rules
redis.setex('coding_rules_icd10', 3600, json.dumps(rules))
```

---

## Backup & Recovery

### Backup Strategy
```bash
# Daily database backup
pg_dump swarmcare_prod | gzip > backup_$(date +%Y%m%d).sql.gz

# Weekly full backup including files
tar -czf backup_full_$(date +%Y%m%d).tar.gz /opt/swarmcare
```

### Recovery Procedure
```bash
# Restore database
gunzip < backup_20251031.sql.gz | psql swarmcare_prod

# Restore files
tar -xzf backup_full_20251031.tar.gz -C /
```

---

## Rollback Procedure

If deployment fails:
```bash
# 1. Stop application
sudo systemctl stop swarmcare

# 2. Restore previous version
sudo cp -r /opt/swarmcare/phase24.backup/* /opt/swarmcare/phase24/

# 3. Restore database
gunzip < backup_previous.sql.gz | psql swarmcare_prod

# 4. Restart application
sudo systemctl start swarmcare

# 5. Verify
python3 scripts/validate_ehr_connections.py
```

---

## Post-Deployment Verification

### Smoke Tests
```bash
# Test EHR connectivity
python3 scripts/validate_ehr_connections.py --detailed

# Test billing generation
python3 scripts/generate_billing_reports.py --encounters 10

# Test data export
python3 scripts/export_integration_data.py --format json --encounters 5
```

### Monitoring First 24 Hours
- Check error logs every 2 hours
- Monitor system resources
- Verify claim submissions
- Track coding accuracy
- Monitor EHR API calls

---

## Troubleshooting

### Common Issues

**Issue**: EHR connection timeout
**Solution**: Check network connectivity, verify credentials, increase timeout

**Issue**: High denial rate
**Solution**: Review coding rules, validate documentation, check payer requirements

**Issue**: Slow performance
**Solution**: Check database indexes, increase cache size, optimize queries

---

## Support Contacts

- **Technical Support**: support@swarmcare.com
- **On-Call**: +1-555-0100
- **Documentation**: /opt/swarmcare/docs/

---

For detailed performance monitoring, see PERFORMANCE_REPORT.md
