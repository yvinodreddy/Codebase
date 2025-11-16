# Phase 17: Deployment Guide

## Quick Deploy

```bash
cd deliverables
./deploy_population_health.sh docker
```

## Docker Deployment

```bash
docker build -t population-health:latest -f Dockerfile ..
docker run -d -p 8080:8080 -p 9090:9090 population-health:latest
```

## Docker Compose Deployment

```bash
docker-compose -f docker-compose.population-health.yml up -d
```

## Kubernetes Deployment

```bash
kubectl apply -f kubernetes-population-health.yaml
```

## Configuration

1. Copy `.env.template` to `.env`
2. Update with your settings
3. Verify HIPAA_MODE=enabled

## Health Check

```bash
curl http://localhost:8080/health
```

## Monitoring

- Metrics: http://localhost:9090/metrics
- Logs: `docker logs -f population-health`

**Status**: ✅ Production Ready
