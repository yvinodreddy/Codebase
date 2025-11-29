#!/bin/bash
################################################################################
# COMPLETE TESTING GUIDE - Access URLs and Test All Changes
################################################################################

echo "================================================================================"
echo "🧪 TESTING ALL CHANGES - STEP BY STEP GUIDE"
echo "================================================================================"
echo ""

# Step 1: Check WebSocket server is running
echo "Step 1: Checking WebSocket Server..."
if lsof -ti:8000 > /dev/null 2>&1; then
    PID=$(lsof -ti:8000)
    echo "✅ WebSocket server is RUNNING (PID: $PID)"
else
    echo "⚠️  WebSocket server NOT running. Starting it now..."
    cd /home/user01/claude-test/ClaudePrompt/realtime-tracking
    python3 websocket_server.py &
    SERVER_PID=$!
    echo "✅ Started server (PID: $SERVER_PID)"
    sleep 3
    cd /home/user01/claude-test/ClaudePrompt
fi

echo ""
echo "================================================================================"
echo "🌐 DASHBOARD URLs - OPEN IN YOUR BROWSER"
echo "================================================================================"
echo ""
echo "📊 Dashboard v2 (with all fixes):"
echo "   http://localhost:8000/v2"
echo ""
echo "📊 Original Dashboard (for comparison):"
echo "   http://localhost:8000/dashboard.html"
echo ""
echo "🔧 API Health Check:"
echo "   http://localhost:8000/api/status"
echo ""
echo "📈 System Monitor API:"
echo "   http://localhost:8000/api/system/monitor"
echo ""
echo "📋 Tracks API:"
echo "   http://localhost:8000/api/tracks"
echo ""

echo "================================================================================"
echo "🧪 TEST 1: Real-Time Logging System"
echo "================================================================================"
echo ""
echo "Running real-time logging test..."
cd /home/user01/claude-test/ClaudePrompt
PYTHONPATH=/home/user01/claude-test/ClaudePrompt:$PYTHONPATH python3 parallel_implementation/test_phase1.py 2>&1 | head -20

echo ""
echo "✅ Test completed! Check the log file:"
echo "   cat parallel_implementation/test_realtime_log.txt"
echo ""

echo "================================================================================"
echo "🧪 TEST 2: Run Actual CPP Command and Watch Dashboard"
echo "================================================================================"
echo ""
echo "To test real CPP execution with dashboard updates:"
echo ""
echo "1. Open browser to: http://localhost:8000/v2"
echo ""
echo "2. Run this command:"
echo "   ./cpp \"Create a simple function to add two numbers\" -v"
echo ""
echo "3. Watch the dashboard - you should see:"
echo "   - New track appear (Track 20 or higher)"
echo "   - Progress updating in real-time"
echo "   - Click 'View Details' to see all information"
echo ""

echo "================================================================================"
echo "🧪 TEST 3: Verify All New Files Exist"
echo "================================================================================"
echo ""
FILES=(
    "realtime_verbose_logger.py"
    "stage_progress_tracker.py"
    "realtime_db_updates.py"
    "realtime_log_monitor.py"
    "enhanced_websocket_broadcast.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        echo "✅ $file ($SIZE)"
    else
        echo "❌ $file MISSING"
    fi
done

echo ""
echo "================================================================================"
echo "🧪 TEST 4: Verify Parser Extracts All 8 Guardrails"
echo "================================================================================"
echo ""
echo "Testing guardrails parser..."
python3 -c "
import sys
sys.path.insert(0, 'realtime-tracking')
from ultrathink_parser import parse_ultrathink_output
result = parse_ultrathink_output('tmp/cppultrathink_output_20251113_073357_470.txt')
guardrails = result.get('guardrails', [])
print(f'Guardrails found: {len(guardrails)}')
for g in guardrails[:8]:
    print(f\"  Layer {g.get('layer')}: {g.get('name')} - {g.get('status')}\")
if len(guardrails) >= 8:
    print('✅ All 8 guardrails extracted successfully!')
else:
    print(f'⚠️  Only {len(guardrails)} guardrails found (expected 8)')
"

echo ""
echo "================================================================================"
echo "🧪 TEST 5: Check Database Tracks"
echo "================================================================================"
echo ""
echo "Recent tracks in database:"
python3 -c "
import sqlite3
conn = sqlite3.connect('realtime-tracking/track_state.db')
c = conn.cursor()
c.execute('SELECT id, name, status, progress FROM tracks ORDER BY id DESC LIMIT 5')
rows = c.fetchall()
for row in rows:
    print(f'  Track {row[0]}: {row[1]} - {row[2]} ({row[3]}%)')
conn.close()
"

echo ""
echo "================================================================================"
echo "📖 QUICK TESTING COMMANDS"
echo "================================================================================"
echo ""
echo "Test real-time logging:"
echo "  PYTHONPATH=\$PWD python3 parallel_implementation/test_phase1.py"
echo ""
echo "Run CPP and watch dashboard:"
echo "  ./cpp \"test prompt\" -v"
echo "  # Then open: http://localhost:8000/v2"
echo ""
echo "View test log file:"
echo "  cat parallel_implementation/test_realtime_log.txt"
echo ""
echo "Check server logs:"
echo "  tail -f realtime-tracking/server.log"
echo ""
echo "Monitor phases (if running parallel script):"
echo "  bash MONITOR_PHASES.sh"
echo ""
echo "View implementation results:"
echo "  cat IMPLEMENTATION_RESULTS.md"
echo ""

echo "================================================================================"
echo "✅ TESTING GUIDE COMPLETE"
echo "================================================================================"
echo ""
echo "Primary URL to test: http://localhost:8000/v2"
echo ""
echo "Next: Open the URL in your browser and run a CPP command to see live updates!"
echo "================================================================================"
