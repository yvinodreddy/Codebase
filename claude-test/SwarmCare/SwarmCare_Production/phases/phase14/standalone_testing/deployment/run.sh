#!/bin/bash
# One-click execution for Phase 14: Medical Imaging

echo "Starting Phase 14: Medical Imaging Testing Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill existing process on port 8014
lsof -ti:8014 | xargs kill -9 2>/dev/null || true

# Start FastAPI app
python3 app.py &
APP_PID=$!

echo ""
echo "✅ Phase 14 Testing UI ready!"
echo "   🌐 Access at: http://localhost:8014"
echo "   📚 API Docs: http://localhost:8014/docs"
echo ""

# Open browser
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:8014 2>/dev/null &
fi

wait $APP_PID
