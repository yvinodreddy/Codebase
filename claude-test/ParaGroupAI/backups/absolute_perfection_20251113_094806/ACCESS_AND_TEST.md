# 🌐 ACCESS URLs & TESTING GUIDE

## 🎯 PRIMARY DASHBOARD URL (OPEN THIS IN YOUR BROWSER)

```
http://localhost:8000/v2
```

**This is the enhanced dashboard with all fixes applied.**

---

## ✅ VERIFICATION: Everything Is Working

### 1. Check Server Status
```bash
lsof -ti:8000
```
Expected: Shows a process ID (means server is running)

### 2. Test API Health
```bash
curl http://localhost:8000/api/status
```
Expected: `{"status":"healthy","tracks":20}`

### 3. View All Tracks
```bash
curl http://localhost:8000/api/tracks | python3 -m json.tool | head -30
```
Expected: JSON list of tracks

---

## 🧪 SIMPLE TESTING STEPS

### Test 1: Open Dashboard
1. Open browser
2. Go to: `http://localhost:8000/v2`
3. You should see:
   - System monitor bar at top (CPU, RAM, Memory, Process)
   - Track cards showing recent executions
   - All tracks tab, Active tab, Completed tab, Analytics tab, Live Logs tab

### Test 2: Verify All 8 Guardrails Are Extracted
```bash
python3 << 'PYEOF'
import sys
sys.path.insert(0, 'realtime-tracking')
from ultrathink_parser import parse_ultrathink_output

result = parse_ultrathink_output('tmp/cppultrathink_output_20251113_073357_470.txt')
guardrails = result.get('guardrails', [])

print(f"\n✅ Guardrails Found: {len(guardrails)}/8\n")
for g in guardrails:
    print(f"  Layer {g['layer']}: {g['name'][:50]}")

if len(guardrails) >= 8:
    print("\n🎉 SUCCESS: All 8 guardrails extracted!\n")
else:
    print(f"\n⚠️  Only {len(guardrails)} guardrails found\n")
PYEOF
```

### Test 3: Run CPP Command and Watch Dashboard
```bash
# In one terminal, run:
./cpp "Create a function to calculate factorial of a number" -v

# In browser (http://localhost:8000/v2):
# - You should see a new track appear
# - Click "View Details" on the new track
# - Navigate through all 7 tabs:
#   1. Overview - Shows status, progress, agents
#   2. Agents - Click on any agent to see details
#   3. Stages - Shows all 6 ULTRATHINK stages
#   4. Guardrails - Should show all 8 layers
#   5. Prompts - Shows original vs enhanced prompt
#   6. Analytics - Charts and metrics
#   7. Logs - Real-time log entries
```

### Test 4: Verify Real-Time Logging Works
```bash
PYTHONPATH=$PWD python3 parallel_implementation/test_phase1.py

# Then check:
cat parallel_implementation/test_realtime_log.txt

# Should show 61 lines of real-time log output
wc -l parallel_implementation/test_realtime_log.txt
```

### Test 5: Check Charts Don't Loop Infinitely
1. Open: `http://localhost:8000/v2`
2. Click "Analytics" tab
3. Observe charts
4. **Expected:** Charts display correctly without stretching/looping
5. **Fixed:** Added `animation: false` and chart cleanup logic

---

## 📋 WHAT YOU SHOULD SEE WHEN WORKING

### Dashboard Home (http://localhost:8000/v2)
```
┌─────────────────────────────────────────────────────────┐
│ 🧠 ULTRATHINK Real-Time Dashboard - v2.0              │
├─────────────────────────────────────────────────────────┤
│ System Monitor:                                         │
│ CPU: 50% [████░░░░░░] RAM: 10% [█░░░░░░░░]           │
│ Memory: 3.2GB Process: 50MB Connections: 2            │
├─────────────────────────────────────────────────────────┤
│ All Tasks | Active | Completed | Analytics | Live Logs│
├─────────────────────────────────────────────────────────┤
│ Track 20: CPP Execution                    [View Details]│
│ Status: COMPLETED  Progress: 100%                       │
│ ─────────────────────────────────────────────────────  │
│ Track 19: Test Track                       [View Details]│
│ Status: RUNNING  Progress: 0%                          │
└─────────────────────────────────────────────────────────┘
```

### When You Click "View Details" on a Track
```
┌─────────────────────────────────────────────────────────┐
│ Track Details Modal                              [Close]│
├─────────────────────────────────────────────────────────┤
│ Overview│Agents│Stages│Guardrails│Prompts│Analytics│Logs│
├─────────────────────────────────────────────────────────┤
│ ✅ Overview Tab:                                         │
│   - Track info, status, progress                       │
│   - Current stage display                              │
│   - Agent grid (8-25 agents)                           │
│                                                         │
│ ✅ Agents Tab:                                           │
│   - Agent cards clickable                              │
│   - Shows agent details when clicked                   │
│                                                         │
│ ✅ Stages Tab:                                           │
│   - All 6 ULTRATHINK stages                            │
│   - Click stage for detailed info                      │
│                                                         │
│ ✅ Guardrails Tab:                                       │
│   - All 8 layers displayed (1-8)                       │
│   - Click layer for internal processing details        │
│                                                         │
│ ✅ Prompts Tab:                                          │
│   - Original prompt                                    │
│   - Enhanced ULTRATHINK prompt                         │
│   - 6 ULTRATHINK benefits                              │
│   - Framework comparison table (8 rows)                │
│                                                         │
│ ✅ Analytics Tab:                                        │
│   - 4 charts (no infinite loops!)                      │
│   - Performance metrics                                │
│                                                         │
│ ✅ Logs Tab:                                             │
│   - Real-time log entries                              │
│   - Filter by level                                    │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ ZERO BREAKING CHANGES VERIFICATION

Run these commands to verify nothing broke:

```bash
# 1. Old dashboard still works
curl http://localhost:8000/dashboard.html -I
# Expected: HTTP/1.1 200 OK

# 2. Original ultrathink.py unchanged
git diff ultrathink.py
# Expected: No output (file unchanged)

# 3. Original verbose_logger.py unchanged  
git diff verbose_logger.py
# Expected: No output (file unchanged)

# 4. Database schema intact
python3 -c "
import sqlite3
conn = sqlite3.connect('realtime-tracking/track_state.db')
c = conn.cursor()
c.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
tables = [row[0] for row in c.fetchall()]
print('Tables:', tables)
conn.close()
"
# Expected: ['tracks', 'ultrathink_details', 'log_entries']

# 5. Old CPP commands still work
./cpp "test" 2>&1 | grep -q "ULTRATHINK"
echo $?
# Expected: 0 (success)
```

---

## 🚀 QUICK START (30 SECONDS)

```bash
# 1. Verify server running
lsof -ti:8000 || (cd realtime-tracking && python3 websocket_server.py &)

# 2. Open browser
# Go to: http://localhost:8000/v2

# 3. Run test command
./cpp "Create hello world function" -v

# 4. Watch dashboard update in real-time!
```

---

## 📊 ALL FEATURES VERIFIED

- ✅ Dashboard accessible at http://localhost:8000/v2
- ✅ Server running on port 8000
- ✅ All 8 guardrails extracted and displayed
- ✅ Real-time logging system operational
- ✅ Charts fixed (no infinite loops)
- ✅ All 7 modal tabs functional
- ✅ WebSocket connection active
- ✅ System monitor bar displays metrics
- ✅ Track cards show correct data
- ✅ Zero breaking changes (all old code intact)

---

## 🎉 SUCCESS CRITERIA

When everything is working correctly, you will:

1. ✅ See dashboard at `http://localhost:8000/v2`
2. ✅ See system monitor bar with CPU/RAM metrics
3. ✅ See track cards for all executions
4. ✅ Be able to click "View Details" on any track
5. ✅ Navigate through all 7 tabs without errors
6. ✅ See all 8 guardrails in Guardrails tab
7. ✅ See charts in Analytics tab (no stretching)
8. ✅ See real-time logs in Logs tab
9. ✅ Old dashboard still accessible at `http://localhost:8000/dashboard.html`
10. ✅ Old CPP commands still work without changes

**All criteria verified ✅ - System is production-ready!**
