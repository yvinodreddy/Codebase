#!/bin/bash
################################################################################
# Phase 00: Foundation - Production-Ready Startup Script
# Starts the complete testing dashboard with all features
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}     Phase 00: Foundation Testing Dashboard - Production Ready${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration
PORT=8000
HOST="0.0.0.0"

################################################################################
# Pre-flight Checks
################################################################################

echo -e "${YELLOW}[1/6] Running Pre-flight Checks...${NC}"

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}❌ Port $PORT is already in use${NC}"
    echo -e "${YELLOW}   Killing process on port $PORT...${NC}"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
    echo -e "${GREEN}   ✅ Port freed${NC}"
fi

# Check Docker services
echo -e "${YELLOW}[2/6] Checking Docker Services...${NC}"
if docker ps --filter "name=swarmcare-neo4j" --filter "status=running" | grep -q swarmcare-neo4j; then
    echo -e "${GREEN}   ✅ Neo4j is running${NC}"
else
    echo -e "${RED}   ⚠️  Neo4j is not running (optional)${NC}"
fi

if docker ps --filter "name=swarmcare-redis" --filter "status=running" | grep -q swarmcare-redis; then
    echo -e "${GREEN}   ✅ Redis is running${NC}"
else
    echo -e "${RED}   ⚠️  Redis is not running (optional)${NC}"
fi

# Check Python dependencies
echo -e "${YELLOW}[3/6] Checking Python Dependencies...${NC}"
python3 -c "import fastapi, uvicorn, pydantic, neo4j, redis" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ All Python dependencies installed${NC}"
else
    echo -e "${YELLOW}   Installing dependencies...${NC}"
    pip3 install --break-system-packages fastapi uvicorn pydantic python-multipart neo4j redis python-dotenv
    echo -e "${GREEN}   ✅ Dependencies installed${NC}"
fi

################################################################################
# Initialize Unified Tracker
################################################################################

echo -e "${YELLOW}[4/6] Initializing Unified Tracker...${NC}"
python3 unified_tracker.py update-metrics >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Unified tracker initialized${NC}"
else
    echo -e "${RED}   ❌ Failed to initialize tracker${NC}"
    exit 1
fi

################################################################################
# Run Tests
################################################################################

echo -e "${YELLOW}[5/6] Running Comprehensive Tests...${NC}"
python3 comprehensive_test.py 2>&1 | grep -E "(✅|❌|SUMMARY|Pass Rate|Production Ready)" | head -20
TEST_EXIT_CODE=${PIPESTATUS[0]}

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}   ✅ All tests passed!${NC}"
else
    echo -e "${YELLOW}   ⚠️  Some tests failed, but continuing...${NC}"
fi

################################################################################
# Start Application
################################################################################

echo -e "${YELLOW}[6/6] Starting FastAPI Application...${NC}"
echo ""
echo -e "${BLUE}================================================================================${NC}"
echo -e "${GREEN}   🚀 Application Starting...${NC}"
echo ""
echo -e "${GREEN}   📊 Dashboard:      http://localhost:$PORT${NC}"
echo -e "${GREEN}   📚 API Docs:       http://localhost:$PORT/docs${NC}"
echo -e "${GREEN}   ❤️  Health Check:  http://localhost:$PORT/api/health${NC}"
echo ""
echo -e "${BLUE}================================================================================${NC}"
echo ""
echo -e "${YELLOW}   Press Ctrl+C to stop the application${NC}"
echo ""

# Start the application
python3 app.py

# Cleanup on exit
trap "echo -e '\n${YELLOW}Shutting down...${NC}'" EXIT
