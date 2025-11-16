#!/bin/bash
# One-click execution for Phase 23: FDA Clearance

echo "Starting Phase 23: FDA Clearance Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8023
lsof -ti:8023 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 23 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8023"
echo "   📚 API Docs: http://localhost:8023/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8023 2>/dev/null &
fi

wait $APP_PID
