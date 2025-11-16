# Phase 12: Clinical Decision Support - Production Deployment Guide

## 🚀 Production Deployment - Complete Guide

**Version:** 1.0
**Last Updated:** October 31, 2025
**Status:** Production Ready

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Monitoring & Observability](#monitoring--observability)
7. [Security Configuration](#security-configuration)
8. [HIPAA Compliance Setup](#hipaa-compliance-setup)
9. [Performance Tuning](#performance-tuning)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 1 GB free space
- OS: Linux, macOS, Windows

**Recommended (Production):**
- CPU: 4+ cores
- RAM: 8 GB
- Disk: 10 GB free space
- OS: Linux (Ubuntu 20.04+ / RHEL 8+)

### Software Requirements

**Required:**
- Python 3.7 or higher
- pip (Python package manager)

**Optional (for containers):**
- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.20+
- kubectl CLI

**Optional (for enhanced features):**
- Azure Content Safety API credentials
- Medical ontology database
- EHR integration credentials

---

## Installation Methods

### Method 1: Standalone Python Module (Fastest)

**Best for:** Testing, development, small deployments

```bash
# Navigate to phase12 directory
cd phases/phase12/code

# Verify installation
python3 -c "from clinical_decision_support import assess_patient; print('✅ Ready')"

# Run quick test
python3 clinical_decision_support.py
```

**Usage:**
```python
from clinical_decision_support import assess_patient

assessment = assess_patient(
    patient_id="PT001",
    temperature_c=38.5,
    heart_rate=110,
    respiratory_rate=24,
    systolic_bp=95,
    oxygen_sat=91,
    lactate=3.2
)

print(f"Alerts: {assessment['alert_count']['total']}")
```

### Method 2: Docker Container (Recommended)

**Best for:** Production, easy scaling, consistent environments

```bash
# Build Docker image
docker build -t swarmcare-clinical-decision-support:v1.0 .

# Run container
docker run -d \
  --name clinical-decision-support \
  -p 8080:8080 \
  -e CONTENT_SAFETY_ENDPOINT="your-endpoint" \
  -e CONTENT_SAFETY_KEY="your-key" \
  swarmcare-clinical-decision-support:v1.0

# Verify health
curl http://localhost:8080/health
```

### Method 3: Docker Compose (Multi-service)

**Best for:** Development, integration testing

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f clinical-decision-support

# Stop services
docker-compose down
```

### Method 4: Kubernetes (Enterprise)

**Best for:** Large-scale production, high availability

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes-deployment.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services

# Check logs
kubectl logs -f deployment/clinical-decision-support
```

---

## Configuration

### Environment Variables

```bash
# Optional: Azure Content Safety (for guardrails)
export CONTENT_SAFETY_ENDPOINT="https://your-endpoint.cognitiveservices.azure.com/"
export CONTENT_SAFETY_KEY="your-api-key"

# Optional: Logging configuration
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export AUDIT_LOG_PATH="/var/log/clinical-decision-support/audit.log"

# Optional: Performance tuning
export MAX_WORKERS=4
export REQUEST_TIMEOUT=30

# Optional: HIPAA compliance
export ENCRYPT_AUDIT_LOGS="true"
export PHI_DEIDENTIFICATION="true"
```

### Configuration File (config.yaml)

Create `config.yaml` for advanced configuration:

```yaml
# Clinical Decision Support Configuration

clinical_decision_support:
  # Alert thresholds
  alerts:
    news2_critical_threshold: 7
    news2_high_threshold: 5
    qsofa_sepsis_threshold: 2

  # Drug interaction database
  drug_interactions:
    database_path: "/opt/cds/drug_db.json"
    update_frequency: "daily"

  # Audit logging
  audit:
    enabled: true
    encryption: true
    retention_days: 2555  # 7 years HIPAA requirement
    log_path: "/var/log/cds/audit.log"

  # Performance
  performance:
    max_concurrent_assessments: 100
    assessment_timeout_ms: 1000

  # Security
  security:
    require_authentication: true
    encrypt_patient_data: true
    tls_enabled: true
```

---

## Docker Deployment

### Building the Docker Image

```bash
# Build from Dockerfile
docker build -t swarmcare-cds:1.0 -f deliverables/Dockerfile .

# Tag for registry
docker tag swarmcare-cds:1.0 your-registry.com/swarmcare-cds:1.0

# Push to registry
docker push your-registry.com/swarmcare-cds:1.0
```

### Running Container

**Development:**
```bash
docker run -it --rm \
  --name cds-dev \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -p 8080:8080 \
  swarmcare-cds:1.0
```

**Production:**
```bash
docker run -d \
  --name cds-prod \
  --restart unless-stopped \
  -v /opt/cds/config.yaml:/app/config.yaml \
  -v /var/log/cds:/var/log/cds \
  -p 8080:8080 \
  --memory="4g" \
  --cpus="2" \
  --health-cmd="python3 -c 'from clinical_decision_support import assess_patient'" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  swarmcare-cds:1.0
```

### Docker Compose Stack

```bash
# Start stack
docker-compose -f deliverables/docker-compose.yml up -d

# Scale service
docker-compose up -d --scale clinical-decision-support=3

# View logs
docker-compose logs -f

# Stop stack
docker-compose down
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Verify cluster access
kubectl cluster-info
kubectl get nodes

# Create namespace
kubectl create namespace clinical-decision-support
kubectl config set-context --current --namespace=clinical-decision-support
```

### Deploy to Kubernetes

```bash
# Apply all resources
kubectl apply -f deliverables/kubernetes-deployment.yaml

# Verify deployment
kubectl get all

# Check pod status
kubectl get pods -w

# View logs
kubectl logs -f deployment/clinical-decision-support
```

### Service Exposure

**Internal (ClusterIP):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: clinical-decision-support
spec:
  type: ClusterIP
  ports:
  - port: 8080
    targetPort: 8080
```

**External (LoadBalancer):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: clinical-decision-support
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
```

### Horizontal Pod Autoscaling

```bash
# Create HPA
kubectl autoscale deployment clinical-decision-support \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Verify HPA
kubectl get hpa
```

### Rolling Updates

```bash
# Update image
kubectl set image deployment/clinical-decision-support \
  clinical-decision-support=swarmcare-cds:1.1

# Monitor rollout
kubectl rollout status deployment/clinical-decision-support

# Rollback if needed
kubectl rollout undo deployment/clinical-decision-support
```

---

## Monitoring & Observability

### Health Checks

**HTTP Health Endpoint:**
```python
@app.route('/health')
def health_check():
    return {
        "status": "healthy",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }
```

**Readiness Probe:**
```python
@app.route('/ready')
def readiness_check():
    # Verify database connections, etc.
    return {"ready": True}
```

### Logging

**Application Logs:**
```bash
# Docker
docker logs -f clinical-decision-support

# Kubernetes
kubectl logs -f deployment/clinical-decision-support

# Log aggregation (ELK Stack)
# Configure Filebeat to ship logs to Elasticsearch
```

**Audit Logs:**
```bash
# View audit trail
tail -f /var/log/cds/audit.log

# Search audit logs
grep "CRITICAL" /var/log/cds/audit.log
```

### Metrics

**Prometheus Integration:**
```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
assessments_total = Counter('cds_assessments_total', 'Total assessments')
assessment_duration = Histogram('cds_assessment_duration_seconds', 'Assessment duration')
critical_alerts = Counter('cds_critical_alerts_total', 'Critical alerts')
```

**Grafana Dashboard:**
- Import dashboard template from `deliverables/grafana-dashboard.json`
- Key metrics: throughput, latency, alert distribution, error rate

---

## Security Configuration

### TLS/SSL Setup

**Generate Certificates:**
```bash
# Self-signed (development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Let's Encrypt (production)
certbot certonly --standalone -d cds.yourdomain.com
```

**Configure TLS:**
```python
# Flask with TLS
app.run(
    host='0.0.0.0',
    port=8443,
    ssl_context=('cert.pem', 'key.pem')
)
```

### Authentication

**API Key Authentication:**
```python
from functools import wraps
from flask import request, abort

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.environ.get('API_KEY'):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/assess')
@require_api_key
def assess():
    # Protected endpoint
    pass
```

### Network Security

**Kubernetes Network Policy:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: clinical-decision-support-netpol
spec:
  podSelector:
    matchLabels:
      app: clinical-decision-support
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: medical-systems
    ports:
    - protocol: TCP
      port: 8080
```

---

## HIPAA Compliance Setup

### Audit Logging

**Enable encrypted audit logs:**
```python
import json
import hashlib
from cryptography.fernet import Fernet

class HIPAACompliantLogger:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def log_assessment(self, assessment):
        # Create audit entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "patient_id_hash": hashlib.sha256(
                assessment['patient_id'].encode()
            ).hexdigest(),
            "action": "CLINICAL_ASSESSMENT",
            "user": "system",
            "alerts": assessment['alert_count']['total']
        }

        # Encrypt and write
        encrypted = self.cipher.encrypt(
            json.dumps(audit_entry).encode()
        )
        with open('/var/log/cds/audit.log', 'ab') as f:
            f.write(encrypted + b'\n')
```

### Data Retention

**Automated retention policy:**
```bash
# Cron job to delete logs older than 7 years
0 0 * * 0 find /var/log/cds/ -type f -mtime +2555 -delete
```

### Access Controls

**Role-Based Access Control (RBAC):**
```python
ROLES = {
    "physician": ["assess_patient", "view_alerts", "view_audit"],
    "nurse": ["assess_patient", "view_alerts"],
    "admin": ["assess_patient", "view_alerts", "view_audit", "manage_system"],
    "auditor": ["view_audit"]
}

def check_permission(user_role, action):
    return action in ROLES.get(user_role, [])
```

---

## Performance Tuning

### Optimization Settings

**Python GIL workaround (multi-processing):**
```python
from multiprocessing import Pool

def parallel_assessments(patient_list):
    with Pool(processes=4) as pool:
        results = pool.map(assess_patient_worker, patient_list)
    return results
```

**Caching frequent calculations:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_news2_cached(vitals_tuple):
    vitals = VitalSigns(*vitals_tuple)
    return calculate_news2(vitals)
```

### Load Balancing

**Nginx Configuration:**
```nginx
upstream clinical_decision_support {
    least_conn;
    server cds1:8080;
    server cds2:8080;
    server cds3:8080;
}

server {
    listen 80;
    server_name cds.yourdomain.com;

    location / {
        proxy_pass http://clinical_decision_support;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Troubleshooting

### Common Issues

**Issue 1: Guardrails warning message**
```
WARNING: Guardrails not available: CONTENT_SAFETY_ENDPOINT not set
```
**Solution:**
```bash
export CONTENT_SAFETY_ENDPOINT="https://your-endpoint.cognitiveservices.azure.com/"
export CONTENT_SAFETY_KEY="your-api-key"
```

**Issue 2: Performance degradation**
```
Assessments taking >100ms
```
**Solution:**
- Check system resources (CPU, memory)
- Enable caching
- Scale horizontally
- Profile with `cProfile`

**Issue 3: Import errors**
```
ModuleNotFoundError: No module named 'clinical_decision_support'
```
**Solution:**
```bash
# Ensure correct Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/phase12/code"
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL="DEBUG"
python3 code/clinical_decision_support.py

# Run verification tests
python3 deliverables/verify_clinical_system.py
```

### Health Monitoring

```bash
# Check system status
curl http://localhost:8080/health

# View real-time metrics
curl http://localhost:8080/metrics

# Test assessment endpoint
curl -X POST http://localhost:8080/assess \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "PT001", "temperature_c": 38.5}'
```

---

## Production Checklist

### Pre-Deployment

- [ ] All tests passing (unit + integration)
- [ ] Performance benchmarks met
- [ ] Security audit completed
- [ ] HIPAA compliance verified
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team training completed

### Deployment

- [ ] Deploy to staging environment
- [ ] Run smoke tests
- [ ] Validate integrations
- [ ] Load testing
- [ ] Security scan
- [ ] Deploy to production
- [ ] Verify health checks
- [ ] Monitor for 24 hours

### Post-Deployment

- [ ] Monitor metrics
- [ ] Check audit logs
- [ ] Verify performance
- [ ] User acceptance testing
- [ ] Document lessons learned
- [ ] Plan next iteration

---

## Support

### Getting Help

**Documentation:** `docs/CLINICAL_DECISION_SUPPORT_GUIDE.md`
**Verification:** `python3 deliverables/verify_clinical_system.py`
**Issues:** GitHub issue tracker
**Email:** support@swarmcare.ai

### Emergency Contact

**Critical Production Issues:** On-call engineering team
**Security Incidents:** security@swarmcare.ai
**HIPAA Compliance:** compliance@swarmcare.ai

---

**Deployment Guide Version:** 1.0
**Last Updated:** October 31, 2025
**Next Review:** January 31, 2026

✅ **Ready for Production Deployment**
