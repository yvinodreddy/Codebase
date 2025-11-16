#!/bin/bash
# Phase 14 - Standalone Testing Application Startup Script
# This script starts the complete testing application with all services

echo "========================================"
echo "Phase 14: Multi-modal AI - Medical Imaging"
echo "Starting Application..."
echo "========================================"
echo ""

# Check Python version
python3 --version || {
    echo "❌ Python 3 not found!"
    exit 1
}

# Check dependencies
echo "Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null || {
    echo "Installing FastAPI..."
    pip3 install fastapi uvicorn python-multipart
}

python3 -c "import neo4j" 2>/dev/null || {
    echo "Installing Neo4j driver..."
    pip3 install neo4j
}

python3 -c "import redis" 2>/dev/null || {
    echo "Installing Redis..."
    pip3 install redis
}

echo ""
echo "✅ Dependencies ready"
echo ""

# Start application
echo "Starting FastAPI application on port 8014..."
python3 app.py

# Application will be accessible at:
# http://localhost:8014
