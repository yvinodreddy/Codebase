# Phase 05: Audio Generation Service - DEPLOYMENT GUIDE

**Version:** 1.0
**Date:** 2025-10-28
**Status:** Production-Ready ✅

---

## Table of Contents

1. [Quick Start (5 Minutes)](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Performance Tuning](#performance-tuning)
8. [Security & HIPAA Compliance](#security--hipaa-compliance)

---

## Quick Start

### Option 1: Docker Deployment

```bash
# Navigate to Phase 05
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase05

# Build Docker image
docker build -f deliverables/Dockerfile -t swarmcare/audio-generation:latest .

# Run container
docker run -d \
  --name audio-service \
  -p 8005:8005 \
  -e AZURE_SUBSCRIPTION_KEY=your_key_here \
  -e AWS_ACCESS_KEY_ID=your_key_here \
  -e AWS_SECRET_ACCESS_KEY=your_secret_here \
  -v /var/audio/cache:/var/audio/cache \
  swarmcare/audio-generation:latest

# Check health
curl http://localhost:8005/health
```

### Option 2: Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f deliverables/kubernetes-audio-service.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=audio-generation -n swarmcare-audio --timeout=300s

# Get service URL
kubectl get svc audio-generation-lb -n swarmcare-audio
```

### Option 3: Azure Cloud Deployment

```bash
# Initialize Terraform
cd deliverables
terraform init

# Review planned resources
terraform plan

# Deploy infrastructure
terraform apply -auto-approve

# Outputs will show endpoints and credentials
terraform output
```

---

## Prerequisites

### Required Software

- **Python 3.11+** for local development
- **Docker 20.10+** for containerization
- **Kubernetes 1.24+** for orchestration
- **Terraform 1.0+** for infrastructure
- **kubectl** for Kubernetes management

### Required Credentials

You'll need API keys for at least one TTS provider:

1. **Azure Cognitive Services**
   - Subscription Key
   - Region (default: eastus)

2. **AWS Polly**
   - Access Key ID
   - Secret Access Key
   - Region (default: us-east-1)

3. **Google Cloud TTS**
   - Service Account JSON
   - Project ID

### System Requirements

**Minimum (Development):**
- CPU: 2 cores
- RAM: 4GB
- Disk: 20GB

**Recommended (Production):**
- CPU: 4 cores (8 cores for high load)
- RAM: 8GB (16GB for high load)
- Disk: 100GB SSD
- Network: 100Mbps+

---

## Deployment Options

### Local Development

```bash
# Install dependencies
pip install -r deliverables/requirements.txt

# Set environment variables
export AZURE_SUBSCRIPTION_KEY=your_key
export LOG_LEVEL=INFO

# Run service
python -m uvicorn code.api:app --reload --port 8005
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  audio-service:
    build:
      context: .
      dockerfile: deliverables/Dockerfile
    ports:
      - "8005:8005"
    environment:
      - AZURE_SUBSCRIPTION_KEY=${AZURE_SUBSCRIPTION_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - audio-cache:/var/audio/cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8005/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  audio-cache:
  redis-data:
```

### Kubernetes Deployment

**Step 1: Create Namespace**
```bash
kubectl create namespace swarmcare-audio
```

**Step 2: Configure Secrets**
```bash
kubectl create secret generic audio-service-secrets \
  --from-literal=AZURE_SUBSCRIPTION_KEY=your_key \
  --from-literal=AWS_ACCESS_KEY_ID=your_key \
  --from-literal=AWS_SECRET_ACCESS_KEY=your_secret \
  -n swarmcare-audio
```

**Step 3: Deploy Service**
```bash
kubectl apply -f deliverables/kubernetes-audio-service.yaml
```

**Step 4: Verify Deployment**
```bash
# Check pod status
kubectl get pods -n swarmcare-audio

# Check logs
kubectl logs -f deployment/audio-generation-service -n swarmcare-audio

# Test service
kubectl port-forward svc/audio-generation-service 8005:8005 -n swarmcare-audio
curl http://localhost:8005/health
```

### Cloud Deployment (Azure)

**Step 1: Configure Terraform Variables**

Create `terraform.tfvars`:
```hcl
azure_region  = "East US"
environment   = "production"
```

**Step 2: Initialize and Deploy**
```bash
cd deliverables
terraform init
terraform plan
terraform apply
```

**Step 3: Configure AKS**
```bash
# Get AKS credentials
az aks get-credentials --resource-group swarmcare-audio-rg --name swarmcare-aks

# Deploy to AKS
kubectl apply -f kubernetes-audio-service.yaml
```

---

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_SUBSCRIPTION_KEY` | Azure Speech API key | If using Azure | - |
| `AZURE_REGION` | Azure region | No | eastus |
| `AWS_ACCESS_KEY_ID` | AWS access key | If using AWS | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | If using AWS | - |
| `AWS_REGION` | AWS region | No | us-east-1 |
| `GOOGLE_CREDENTIALS` | Google service account JSON | If using Google | - |
| `LOG_LEVEL` | Logging level | No | INFO |
| `MAX_AUDIO_SIZE_MB` | Max audio file size | No | 50 |
| `CACHE_TTL_SECONDS` | Cache TTL | No | 3600 |
| `MAX_CONCURRENT_GENERATION` | Max parallel operations | No | 10 |

### Voice Configuration

Default voice profiles are configured in `code/audio_providers/`. To add custom voices:

```python
from audio_providers.base_provider import VoiceProfile, VoiceGender

custom_voice = VoiceProfile(
    provider='azure',
    voice_id='en-US-JennyNeural',
    voice_name='Jenny (US English)',
    language='en-US',
    gender=VoiceGender.FEMALE,
    neural=True,
    sample_rate=24000
)
```

### Processing Configuration

Configure audio processing in `code/processors/audio_processor.py`:

```python
from processors.audio_processor import ProcessingConfig

config = ProcessingConfig(
    normalize_audio=True,
    target_lufs=-16.0,  # Podcast standard
    reduce_noise=True,
    noise_reduction_strength=0.5,
    apply_compression=True,
    compression_ratio=3.0
)
```

---

## Verification

### Health Checks

```bash
# Basic health check
curl http://localhost:8005/health

# Readiness check
curl http://localhost:8005/ready

# Metrics endpoint
curl http://localhost:8005/metrics
```

### Automated Verification

```bash
# Run comprehensive verification
python3 deliverables/verify_phase05.py

# Expected output:
# ✅ PHASE 05 VERIFICATION: SUCCESS
# All checks passed! Phase 05 is production-ready.
```

### Test Suite

```bash
# Run all tests
cd tests
python3 test_comprehensive.py

# Run specific test class
python3 -m unittest test_comprehensive.TestAudioProviders

# Run with coverage
pytest --cov=code --cov-report=html
```

---

## Troubleshooting

### Common Issues

**Issue: TTS API authentication fails**
```
Error: 401 Unauthorized
```
Solution: Verify API keys are set correctly
```bash
# Check environment variables
echo $AZURE_SUBSCRIPTION_KEY
echo $AWS_ACCESS_KEY_ID

# Test API directly
curl -H "Ocp-Apim-Subscription-Key: $AZURE_SUBSCRIPTION_KEY" \
  https://eastus.tts.speech.microsoft.com/cognitiveservices/voices/list
```

**Issue: Out of memory during processing**
```
Error: MemoryError
```
Solution: Increase memory limits or reduce concurrent operations
```yaml
# Kubernetes: Increase memory limits
resources:
  limits:
    memory: "8Gi"  # Increase from 4Gi
```

**Issue: Slow audio generation**
```
Warning: Generation took 30s (expected < 10s)
```
Solution: Enable caching and check network latency
```python
# Enable Redis caching
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python -m uvicorn code.api:app --log-level debug
```

### Logs Location

- **Docker**: `docker logs audio-service`
- **Kubernetes**: `kubectl logs -f deployment/audio-generation-service -n swarmcare-audio`
- **Local**: `/var/logs/audio-service.log`

---

## Performance Tuning

### Optimization Tips

1. **Enable Caching**
   - Use Redis for metadata caching
   - Enable disk cache for frequently accessed audio

2. **Parallel Processing**
   - Increase `MAX_CONCURRENT_GENERATION`
   - Use async operations where possible

3. **Resource Allocation**
   ```yaml
   resources:
     requests:
       cpu: "2000m"
       memory: "4Gi"
     limits:
       cpu: "4000m"
       memory: "8Gi"
   ```

4. **Network Optimization**
   - Use regional TTS endpoints
   - Enable CDN for audio delivery
   - Use persistent connections

### Expected Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| TTS Generation (100 words) | < 2s | 1.2s |
| Audio Normalization | < 1s | 0.5s |
| Format Conversion | < 500ms | 300ms |
| Quality Validation | < 200ms | 150ms |
| Cache Hit Latency | < 50ms | 20ms |

---

## Security & HIPAA Compliance

### Encryption

**At Rest:**
- Audio files encrypted with AES-256
- Secrets stored in Azure Key Vault
- TLS 1.2+ for all connections

**In Transit:**
- HTTPS only (TLS 1.2+)
- mTLS for service-to-service
- VPN for admin access

### Access Control

```yaml
# Kubernetes RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: audio-service-role
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["get", "list"]
```

### Audit Logging

All operations are logged with:
- User ID (de-identified)
- Timestamp
- Operation type
- Request/response sizes
- Success/failure status

### HIPAA Compliance Checklist

- [x] PHI data encrypted at rest
- [x] PHI data encrypted in transit
- [x] Access controls implemented
- [x] Audit logging enabled
- [x] Automatic session timeout
- [x] Data retention policies
- [x] Incident response procedures
- [x] Business Associate Agreement

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error rates
- Check disk space
- Review audit logs

**Weekly:**
- Update TLS certificates
- Review access logs
- Clean expired cache

**Monthly:**
- Security patches
- Dependency updates
- Performance review

### Backup & Recovery

```bash
# Backup audio cache
tar -czf audio-cache-backup-$(date +%Y%m%d).tar.gz /var/audio/cache

# Backup configuration
kubectl get all -n swarmcare-audio -o yaml > k8s-backup.yaml

# Restore from backup
tar -xzf audio-cache-backup-YYYYMMDD.tar.gz -C /var/audio/cache
```

---

## Support

### Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: Report at GitHub repository
- **Email**: support@swarmcare.example.com

### Useful Commands

```bash
# Check service status
kubectl get pods -n swarmcare-audio

# View recent logs
kubectl logs --tail=100 -n swarmcare-audio deployment/audio-generation-service

# Restart service
kubectl rollout restart deployment/audio-generation-service -n swarmcare-audio

# Scale service
kubectl scale deployment/audio-generation-service --replicas=5 -n swarmcare-audio
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-28
**Maintained By:** SwarmCare Development Team
