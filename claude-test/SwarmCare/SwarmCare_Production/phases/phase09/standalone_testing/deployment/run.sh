#!/bin/bash
# One-click execution for Phase 9: Documentation

echo "Starting Phase 9: Documentation Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8009
lsof -ti:8009 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 9 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8009"
echo "   📚 API Docs: http://localhost:8009/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8009 2>/dev/null &
fi

wait $APP_PID
