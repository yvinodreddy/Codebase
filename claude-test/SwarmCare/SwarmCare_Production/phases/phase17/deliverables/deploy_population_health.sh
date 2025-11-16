#!/bin/bash
set -e
echo "🚀 Deploying Population Health Management System"
echo "Mode: ${1:-docker}"

case "${1:-docker}" in
  docker)
    echo "Building Docker image..."
    docker build -t population-health:latest -f Dockerfile ..
    echo "Running container..."
    docker run -d --name population-health -p 8080:8080 -p 9090:9090 population-health:latest
    echo "✅ Deployed via Docker"
    ;;
  docker-compose)
    echo "Starting services..."
    docker-compose -f docker-compose.population-health.yml up -d
    echo "✅ Deployed via Docker Compose"
    ;;
  k8s|kubernetes)
    echo "Applying Kubernetes manifests..."
    kubectl apply -f kubernetes-population-health.yaml
    echo "✅ Deployed to Kubernetes"
    ;;
  local)
    echo "Starting local deployment..."
    cd ../code && python3 implementation.py &
    echo "✅ Deployed locally"
    ;;
  *)
    echo "Usage: $0 [docker|docker-compose|k8s|local]"
    exit 1
    ;;
esac
