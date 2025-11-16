#!/bin/bash
# One-click execution for Phase 18: Clinical Trials

echo "Starting Phase 18: Clinical Trials Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8018
lsof -ti:8018 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 18 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8018"
echo "   📚 API Docs: http://localhost:8018/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8018 2>/dev/null &
fi

wait $APP_PID
