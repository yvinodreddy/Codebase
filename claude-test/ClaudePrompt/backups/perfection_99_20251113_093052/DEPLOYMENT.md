# ULTRATHINK Production Deployment Guide

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -xvs

# Start API server
cd api
uvicorn main:app --reload
```

### Docker Deployment
```bash
# Build image
docker build -t ultrathink:latest .

# Run with Docker Compose
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

### Production Deployment

#### Prerequisites
- Docker 20.10+
- docker-compose 2.0+
- 4GB RAM minimum
- 10GB disk space

#### Environment Variables
```bash
# Required
export ANTHROPIC_API_KEY=your_key_here

# Optional
export REDIS_URL=redis://localhost:6379
export LOG_LEVEL=INFO
export MAX_WORKERS=4
```

#### Deploy to Production
```bash
# Build production image
docker build -t ultrathink:production -f Dockerfile .

# Start services
docker-compose -f docker-compose.yml up -d

# Verify deployment
curl http://localhost:8000/ready
```

## Monitoring

### Health Checks
- Liveness: `GET /health`
- Readiness: `GET /ready`
- Metrics: `GET /v1/status`

### Prometheus Metrics
Available at port 9090 when running with docker-compose.

### Logs
```bash
# View API logs
docker-compose logs -f app

# View Redis logs
docker-compose logs -f redis
```

## Scaling

### Horizontal Scaling
```yaml
# docker-compose.override.yml
services:
  app:
    deploy:
      replicas: 3
```

### Load Balancing
Use nginx or cloud load balancer:
```nginx
upstream ultrathink {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}
```

## Troubleshooting

### Common Issues

**Issue:** API returns 503
**Solution:** Check orchestrator initialization

**Issue:** High latency
**Solution:** Enable caching, increase workers

**Issue:** Out of memory
**Solution:** Increase container memory limit

## Security

### Best Practices
1. Use API keys for authentication
2. Enable HTTPS in production
3. Rotate secrets regularly
4. Monitor security scans
5. Keep dependencies updated

## Backup & Recovery

### Backup
```bash
# Backup configuration
tar -czf backup.tar.gz . --exclude=venv --exclude=__pycache__

# Backup Redis data
docker exec ultrathink_redis redis-cli BGSAVE
```

### Recovery
```bash
# Restore from backup
tar -xzf backup.tar.gz

# Restart services
docker-compose restart
```
