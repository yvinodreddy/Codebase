#!/bin/bash
# Phase 27: Clinical Trial Lifecycle Deployment Script

set -e

echo "=================================="
echo "Clinical Trial Lifecycle Deployment"
echo "=================================="
echo

DEPLOYMENT_TYPE=${1:-"standalone"}

case $DEPLOYMENT_TYPE in
  "docker")
    echo "🐳 Deploying with Docker..."
    docker build -t clinical-trial-system -f Dockerfile ..
    docker run -d -p 8000:8000 --name clinical-trial clinical-trial-system
    echo "✅ Deployed on http://localhost:8000"
    ;;
  
  "docker-compose")
    echo "🐳 Deploying with Docker Compose..."
    docker-compose -f docker-compose.clinical-trial.yml up -d
    echo "✅ Deployed with database"
    ;;
  
  "kubernetes")
    echo "☸️  Deploying to Kubernetes..."
    kubectl apply -f kubernetes-clinical-trial.yaml
    echo "✅ Deployed to Kubernetes"
    ;;
  
  "standalone")
    echo "📦 Standalone deployment..."
    cd ../code
    python3 -c "
from implementation import Phase27Implementation
impl = Phase27Implementation()
print('✅ System initialized')
print(f'Phase: {impl.phase_name}')
print(f'Framework: {impl.framework_version}')
"
    ;;
  
  *)
    echo "Usage: $0 [docker|docker-compose|kubernetes|standalone]"
    exit 1
    ;;
esac
