#!/bin/bash
# One-click execution for Phase 10: Business Development

echo "Starting Phase 10: Business Development Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8010
lsof -ti:8010 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 10 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8010"
echo "   📚 API Docs: http://localhost:8010/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8010 2>/dev/null &
fi

wait $APP_PID
