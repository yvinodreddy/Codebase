#!/bin/bash
# One-click execution for Phase 0: Foundation
# This script starts all services, loads test data, and opens the testing UI

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                  PHASE 0: FOUNDATION - TESTING ENVIRONMENT                   ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Navigate to project root (we're in standalone_testing/deployment/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
STANDALONE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PHASE_DIR="$(cd "$STANDALONE_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$PHASE_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Check if .env exists (optional - will use defaults if not present)
if [ -f .env ]; then
    echo "✅ Loading environment from .env"
    source .env
else
    echo "ℹ️  No .env file found, using defaults"
fi

# Try to start Docker services (optional)
echo "📦 Step 1: Starting Docker services (optional)..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d neo4j redis 2>/dev/null && echo "✅ Docker services started" || echo "⚠️  Docker services not available (optional)"
else
    echo "ℹ️  Docker not available - skipping (Neo4j and Redis are optional for basic testing)"
fi

# Only wait if Docker started successfully
if docker ps &> /dev/null && docker ps | grep -q "neo4j\|redis"; then
    echo "⏳ Step 2: Waiting for services to be healthy (10 seconds)..."
    sleep 10
    echo "🔍 Step 3: Verifying services..."
    docker ps | grep -E "neo4j|redis" || echo "ℹ️  Services starting..."
fi

echo "🌱 Step 4: Seeding test data..."
if [ -f "phases/phase00/standalone_testing/test_data/seeding_scripts/seed_all.py" ]; then
    python3 phases/phase00/standalone_testing/test_data/seeding_scripts/seed_all.py 2>/dev/null || echo "ℹ️  Data seeding skipped (Neo4j not available)"
else
    echo "⚠️  Seeding script not found, skipping data seeding"
fi

echo "🚀 Step 5: Starting testing UI..."
cd phases/phase00/standalone_testing/deployment

# Kill any existing process on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start FastAPI app in background
python3 app.py &
APP_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 0 Testing Environment Ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🌐 Testing UI:       http://localhost:8000"
echo "  📚 API Docs:         http://localhost:8000/docs"
echo "  🏥 Neo4j Browser:    http://localhost:7474"
echo "  🔧 Health Check:     http://localhost:8000/api/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Open browser (works on most Linux systems with xdg-open)
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8000 2>/dev/null &
fi

# Wait for app process
wait $APP_PID
