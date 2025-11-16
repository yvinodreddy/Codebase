#!/bin/bash
# One-click execution for Phase 7: Testing Framework

echo "Starting Phase 7: Testing Framework Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8007
lsof -ti:8007 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 7 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8007"
echo "   📚 API Docs: http://localhost:8007/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8007 2>/dev/null &
fi

wait $APP_PID
