# Phase 09: Documentation - Deployment Guide

**Version:** 2.1
**Last Updated:** 2025-10-28
**Status:** Production-Ready ✅

---

## Overview

This guide provides comprehensive instructions for deploying the SwarmCare Documentation system to production.

## Documentation Services

The SwarmCare Documentation system consists of 5 main services:

1. **MkDocs** - User-friendly documentation
2. **Sphinx** - Technical/API documentation
3. **Docusaurus** - Modern documentation site
4. **Swagger UI** - Interactive API documentation
5. **ReDoc** - Beautiful API documentation

---

## Prerequisites

### System Requirements

**Minimum:**
- Kubernetes 1.24+ OR Docker 20.10+
- 4 CPU cores
- 8GB RAM
- 50GB storage

**Recommended for Production:**
- Kubernetes 1.27+
- 8 CPU cores
- 16GB RAM
- 100GB SSD storage

### Software Dependencies

```bash
# Required
- kubectl 1.24+
- helm 3.10+
- docker 20.10+
- docker-compose 2.0+

# Optional but recommended
- nginx (reverse proxy)
- certbot (SSL certificates)
```

---

## Kubernetes Deployment

### Step 1: Create Namespace

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: swarmcare-docs
  labels:
    name: swarmcare-docs
    phase: "09"
EOF
```

### Step 2: Deploy Documentation Services

```bash
# Navigate to deliverables
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase09/deliverables

# Apply Kubernetes manifests
kubectl apply -f kubernetes-deployment.yaml -n swarmcare-docs

# Watch deployment
kubectl get pods -n swarmcare-docs -w
```

### Step 3: Configure Ingress

```bash
# Install cert-manager for SSL
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Configure ingress (already in kubernetes-deployment.yaml)
# Access at: https://docs.swarmcare.io
```

### Step 4: Verify Deployment

```bash
# Check all pods running
kubectl get pods -n swarmcare-docs

# Expected output:
# mkdocs-server-xxx        1/1     Running   0          2m
# sphinx-server-xxx        1/1     Running   0          2m
# api-docs-server-xxx      1/1     Running   0          2m

# Check services
kubectl get svc -n swarmcare-docs

# Test endpoints
curl https://docs.swarmcare.io
curl https://docs.swarmcare.io/api
```

---

## Docker Compose Deployment

### Step 1: Prepare Environment

```bash
cd deliverables

# Create .env file
cat > .env <<EOF
ALGOLIA_APP_ID=your-app-id
ALGOLIA_API_KEY=your-api-key
EOF
```

### Step 2: Start Services

```bash
# Start all documentation services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Step 3: Access Documentation

```bash
# MkDocs
open http://localhost:8000

# Sphinx
open http://localhost:8080

# Docusaurus
open http://localhost:3000

# Swagger UI
open http://localhost:8081

# ReDoc
open http://localhost:8082
```

---

## Configuration

### MkDocs Configuration

Edit `documentation-config.yaml` and update:

```yaml
mkdocs.yml: |
  site_name: Your Site Name
  site_url: https://your-domain.com
  theme:
    name: material
    palette:
      primary: blue
```

### Sphinx Configuration

Edit `documentation-config.yaml` and update:

```python
conf.py: |
  project = 'Your Project'
  copyright = '2025, Your Team'
```

---

## Building Documentation

### Local Build

```bash
# Build all documentation
./build_docs.sh

# Build specific format
mkdocs build
sphinx-build -b html source build
cd docusaurus && npm run build
```

### Automated Build (CI/CD)

```yaml
# GitHub Actions example
name: Build Documentation
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build docs
        run: |
          pip install mkdocs-material
          mkdocs build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## Monitoring & Observability

### Health Checks

```bash
# Check MkDocs
curl http://mkdocs-server/health

# Check Sphinx
curl http://sphinx-server/health

# Check API docs
curl http://api-docs-server/health
```

### Metrics

Documentation services expose metrics on `/metrics`:

- Page views
- Search queries
- Response times
- Error rates

---

## Troubleshooting

### Common Issues

**Issue 1: Pods not starting**

```bash
kubectl describe pod <pod-name> -n swarmcare-docs
kubectl logs <pod-name> -n swarmcare-docs
```

**Issue 2: Documentation not rendering**

```bash
# Check syntax
mkdocs build --strict
sphinx-build -W source build

# Check logs
docker-compose logs mkdocs
```

**Issue 3: Search not working**

```bash
# Verify Algolia configuration
echo $ALGOLIA_APP_ID
echo $ALGOLIA_API_KEY

# Rebuild search index
docker-compose run docsearch-scraper
```

---

## Post-Deployment

### Verification

```bash
# Run verification script
python3 verify_documentation.py --verbose
```

### Performance Testing

```bash
# Test page load times
curl -w "@curl-format.txt" -o /dev/null -s https://docs.swarmcare.io

# Expected: < 500ms
```

---

## Maintenance

### Updates

```bash
# Update images
kubectl set image deployment/mkdocs-server mkdocs=swarmcare/mkdocs:2.2 -n swarmcare-docs

# Rollback if needed
kubectl rollout undo deployment/mkdocs-server -n swarmcare-docs
```

### Backup

```bash
# Backup documentation
kubectl get all -n swarmcare-docs -o yaml > backup.yaml

# Backup content
tar -czf docs-backup.tar.gz docs/
```

---

## Security

### SSL/TLS

```bash
# Certificate auto-renewal with cert-manager
kubectl get certificates -n swarmcare-docs

# Manual renewal if needed
certbot renew
```

### Access Control

```bash
# Add basic auth (if needed)
kubectl create secret generic docs-auth \
  --from-literal=username=admin \
  --from-literal=password=secure-password \
  -n swarmcare-docs
```

---

## Support

For deployment issues:
1. Check logs: `kubectl logs <pod-name>`
2. Check events: `kubectl get events`
3. Run verification: `python3 verify_documentation.py`

---

**Deployment Guide Version:** 2.1
**Last Updated:** 2025-10-28
**Status:** ✅ Production-Ready
