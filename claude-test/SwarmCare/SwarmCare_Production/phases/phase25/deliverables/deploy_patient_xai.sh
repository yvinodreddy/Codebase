#!/bin/bash

################################################################################
# Phase 25: Patient-Facing XAI - Deployment Script
################################################################################

set -e

DEPLOYMENT_TYPE=${1:-docker}

echo "================================================================================"
echo "PHASE 25: PATIENT-FACING XAI DEPLOYMENT"
echo "================================================================================"
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "Started: $(date)"
echo "================================================================================"
echo ""

case $DEPLOYMENT_TYPE in
  docker)
    echo "📦 Deploying with Docker..."
    docker build -t patient-xai:latest -f Dockerfile ..
    docker run -d \
      --name patient-xai \
      -p 8080:8080 \
      -p 9090:9090 \
      -e HIPAA_MODE=enabled \
      -e AUDIT_LOGGING=enabled \
      patient-xai:latest
    echo "✅ Docker deployment complete"
    echo "   Application: http://localhost:8080"
    echo "   Metrics: http://localhost:9090"
    ;;

  docker-compose)
    echo "📦 Deploying with Docker Compose..."
    docker-compose -f docker-compose.patient-xai.yml up -d
    echo "✅ Docker Compose deployment complete"
    echo "   Application: http://localhost:8080"
    echo "   Prometheus: http://localhost:9091"
    ;;

  kubernetes)
    echo "☸️  Deploying to Kubernetes..."
    kubectl apply -f kubernetes-patient-xai.yaml
    echo "✅ Kubernetes deployment complete"
    echo "   Check status: kubectl get pods -n patient-xai"
    echo "   Get service: kubectl get svc -n patient-xai"
    ;;

  standalone)
    echo "🐍 Setting up standalone deployment..."
    cd ..
    echo "✅ Ready to run standalone"
    echo "   Run: python3 code/implementation.py"
    ;;

  *)
    echo "❌ Unknown deployment type: $DEPLOYMENT_TYPE"
    echo ""
    echo "Usage: $0 [docker|docker-compose|kubernetes|standalone]"
    echo ""
    echo "Deployment Options:"
    echo "  docker          - Deploy using Docker"
    echo "  docker-compose  - Deploy using Docker Compose with monitoring"
    echo "  kubernetes      - Deploy to Kubernetes cluster"
    echo "  standalone      - Run as standalone Python application"
    exit 1
    ;;
esac

echo ""
echo "================================================================================"
echo "DEPLOYMENT COMPLETED: $(date)"
echo "================================================================================"
