#!/bin/bash
# One-click execution for Phase 27: Trial Lifecycle

echo "Starting Phase 27: Trial Lifecycle Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8027
lsof -ti:8027 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 27 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8027"
echo "   📚 API Docs: http://localhost:8027/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8027 2>/dev/null &
fi

wait $APP_PID
