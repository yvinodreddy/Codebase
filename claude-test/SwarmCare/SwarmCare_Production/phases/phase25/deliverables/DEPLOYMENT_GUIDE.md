# Phase 25: Deployment Guide

## Quick Deploy

```bash
cd deliverables
./deploy_patient_xai.sh docker
```

## Docker Deployment

### Build Image

```bash
docker build -t patient-xai:latest -f Dockerfile ..
```

### Run Container

```bash
docker run -d \
  -p 8080:8080 \
  -p 9090:9090 \
  -e HIPAA_MODE=enabled \
  -e AUDIT_LOGGING=enabled \
  --name patient-xai \
  patient-xai:latest
```

### Health Check

```bash
curl http://localhost:8080/health
```

## Docker Compose Deployment

### Start Services

```bash
docker-compose -f docker-compose.patient-xai.yml up -d
```

### View Logs

```bash
docker-compose -f docker-compose.patient-xai.yml logs -f
```

### Stop Services

```bash
docker-compose -f docker-compose.patient-xai.yml down
```

## Kubernetes Deployment

### Deploy to Cluster

```bash
kubectl apply -f kubernetes-patient-xai.yaml
```

### Check Status

```bash
kubectl get pods -n patient-xai
kubectl get svc -n patient-xai
```

### Scale Deployment

```bash
kubectl scale deployment patient-xai -n patient-xai --replicas=5
```

### View Logs

```bash
kubectl logs -f deployment/patient-xai -n patient-xai
```

## Standalone Deployment

### Requirements

- Python 3.8+
- No external dependencies (stdlib only)

### Run Directly

```bash
cd ../code
python3 implementation.py
```

### Configure Environment

```bash
export HIPAA_MODE=enabled
export AUDIT_LOGGING=enabled
export DEFAULT_LANGUAGE=en
export LOG_LEVEL=INFO
```

## Configuration

### Environment Variables

Copy `.env.template` to `.env` and update:

```bash
# HIPAA Compliance
HIPAA_MODE=enabled
PHI_PROTECTION=enabled
AUDIT_LOGGING=enabled

# Performance
MAX_BATCH_SIZE=100
ENABLE_CACHING=true

# Languages
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,es,zh,fr,de
```

### Configuration File

Edit `patient_xai_config.json`:

```json
{
  "defaults": {
    "language": "en",
    "literacy_level": "intermediate",
    "validate_explanations": true
  },
  "performance": {
    "max_batch_size": 100,
    "cache_enabled": true
  }
}
```

## Monitoring

### Metrics Endpoint

```bash
curl http://localhost:9090/metrics
```

### Prometheus

Access Prometheus UI:

```
http://localhost:9091  (Docker Compose)
```

### Health Checks

Application health:

```bash
curl http://localhost:8080/health
```

## Security

### HIPAA Mode

Always enable HIPAA mode in production:

```bash
export HIPAA_MODE=enabled
```

### Audit Logging

Enable audit logging:

```bash
export AUDIT_LOGGING=enabled
```

Logs location: `/var/log/patient-xai/audit.log`

### TLS/SSL

Configure TLS for production:

```bash
# Add to docker run
-v /path/to/certs:/certs \
-e TLS_CERT=/certs/server.crt \
-e TLS_KEY=/certs/server.key
```

## Troubleshooting

### Container Won't Start

Check logs:

```bash
docker logs patient-xai
```

### Performance Issues

Check resource usage:

```bash
docker stats patient-xai
```

Increase resources:

```bash
docker run -m 1g --cpus=2 ...
```

### Connection Issues

Verify ports:

```bash
netstat -tulpn | grep -E '8080|9090'
```

## Production Checklist

- [ ] HIPAA mode enabled
- [ ] Audit logging enabled
- [ ] TLS/SSL configured
- [ ] Resource limits set
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Health checks configured
- [ ] Environment variables set
- [ ] Configuration reviewed
- [ ] Security audit passed

## Scaling

### Horizontal Scaling (Kubernetes)

Automatic scaling configured:

- Min replicas: 3
- Max replicas: 10
- CPU threshold: 70%
- Memory threshold: 80%

Manual scaling:

```bash
kubectl scale deployment patient-xai --replicas=10
```

### Vertical Scaling (Docker)

```bash
docker run -m 2g --cpus=4 ...
```

---

**Status**: ✅ Production Ready
**Last Updated**: 2025-10-31
