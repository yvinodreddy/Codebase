#!/bin/bash
################################################################################
# STATUS - Show tracker status
# Usage: ./scripts/status.sh [--detailed]
################################################################################

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m'

DETAILED=false
if [ "$1" == "--detailed" ]; then
    DETAILED=true
fi

# Read tracker state
STATE_FILE=".tracker/state.json"

if [ ! -f "$STATE_FILE" ]; then
    echo -e "${RED}❌ Tracker state file not found${NC}"
    exit 1
fi

# Extract key values using Python
CURRENT_PHASE=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['current_phase'])")
PROGRESS=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['progress_percentage'])")
SP_COMPLETED=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['story_points_completed'])")
SP_REMAINING=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['story_points_remaining'])")
STATUS=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['status'])")
LAST_ACTIVITY=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['last_activity'])")

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 SWARMCARE PROJECT STATUS${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Status:       ${GREEN}$STATUS${NC}"
echo -e "  Current:      ${CYAN}Phase $CURRENT_PHASE${NC}"
echo -e "  Progress:     ${GREEN}$PROGRESS%${NC}"
echo -e "  Completed:    ${GREEN}$SP_COMPLETED${NC} / 1362 story points"
echo -e "  Remaining:    ${YELLOW}$SP_REMAINING${NC} story points"
echo -e "  Last:         $LAST_ACTIVITY"
echo ""

# Show progress bar
FILLED=$((PROGRESS / 2))
EMPTY=$((50 - FILLED))
printf "  ["
printf "%${FILLED}s" | tr ' ' '█'
printf "%${EMPTY}s" | tr ' ' '░'
printf "] %3d%%\n" "$PROGRESS"
echo ""

# Show completed phases
echo -e "${BLUE}✅ COMPLETED PHASES:${NC}"
python3 << 'EOF'
import json
with open('.tracker/state.json') as f:
    state = json.load(f)
    completed = state['completed_phases']
    if completed:
        for phase_id in sorted(completed):
            print(f"  ✅ Phase {phase_id:02d}")
    else:
        print("  None yet")
EOF
echo ""

if [ "$DETAILED" == "true" ]; then
    echo -e "${BLUE}📋 ALL PHASES:${NC}"
    python3 << 'EOF'
import json
with open('.tracker/state.json') as f:
    root_state = json.load(f)
with open('.tracker/phase_manifest.json') as f:
    manifest = json.load(f)

completed = root_state['completed_phases']
current = root_state['current_phase']

for phase in manifest['phases']:
    phase_id = phase['phase_id']
    name = phase['name']
    sp = phase['story_points']

    if phase_id in completed:
        status = "✅ COMPLETE"
    elif phase_id == current:
        status = "🔄 IN PROGRESS"
    else:
        status = "⏳ PENDING"

    print(f"  {status:<15} Phase {phase_id:02d}: {name:<45} ({sp:3d} SP)")
EOF
    echo ""
fi

echo -e "${YELLOW}NEXT ACTIONS:${NC}"
if [ "$STATUS" == "NOT_STARTED" ]; then
    echo -e "  Start first phase: ${CYAN}./scripts/start_phase.sh 0${NC}"
elif [ "$STATUS" == "IN_PROGRESS" ]; then
    echo -e "  Continue current: ${CYAN}./scripts/start_phase.sh $CURRENT_PHASE${NC}"
    echo -e "  Or use continue: ${CYAN}./continue${NC}"
elif [ "$STATUS" == "COMPLETED" ]; then
    echo -e "  ${GREEN}All phases complete!${NC}"
    echo -e "  Package phases: ${CYAN}./scripts/package_all.sh${NC}"
fi
echo ""
