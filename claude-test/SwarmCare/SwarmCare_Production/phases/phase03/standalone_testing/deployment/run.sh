#!/bin/bash
# One-click execution for Phase 3: Workflow Orchestration

echo "Starting Phase 3: Workflow Orchestration Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8003
lsof -ti:8003 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 3 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8003"
echo "   📚 API Docs: http://localhost:8003/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8003 2>/dev/null &
fi

wait $APP_PID
