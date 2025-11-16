#!/bin/bash

# RAGHEAT - Resume Implementation Script
# Automatically resume project from where you left off

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     RAGHEAT - Resume Implementation           ║${NC}"
echo -e "${BLUE}║     AI-Generative Financial Intelligence      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if PROJECT_STATE.json exists
if [ ! -f "PROJECT_STATE.json" ]; then
    echo -e "${RED}ERROR: PROJECT_STATE.json not found!${NC}"
    echo "Please run from the project root directory."
    exit 1
fi

# Parse current state using Python (more reliable than jq)
read -r CURRENT_PHASE PHASE_NAME PROGRESS <<< $(python3 <<EOF
import json
with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)
    phase = state['current_phase']
    print(f"{phase['phase_number']} {phase['phase_name']} {phase['progress_percentage']}")
EOF
)

echo -e "${GREEN}Current Status:${NC}"
echo -e "  Phase: ${YELLOW}PHASE $CURRENT_PHASE${NC}"
echo -e "  Name: ${YELLOW}$PHASE_NAME${NC}"
echo -e "  Progress: ${YELLOW}${PROGRESS}%${NC}"
echo ""

# Get next actions
echo -e "${GREEN}Next Actions:${NC}"
python3 <<EOF
import json
with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)
    actions = state.get('next_actions', [])
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
EOF
echo ""

# Show blockers if any
BLOCKERS=$(python3 <<EOF
import json
with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)
    blockers = state.get('blockers', [])
    print(len(blockers))
EOF
)

if [ "$BLOCKERS" -gt 0 ]; then
    echo -e "${RED}⚠️  BLOCKERS DETECTED:${NC}"
    python3 <<EOF
import json
with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)
    blockers = state.get('blockers', [])
    for i, blocker in enumerate(blockers, 1):
        print(f"  {i}. {blocker}")
EOF
    echo ""
fi

# Show progress bar
echo -e "${GREEN}Overall Progress:${NC}"
python3 <<EOF
import json
with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)
    total = state['total_tasks']
    completed = state['completed_tasks']
    percentage = state['overall_progress_percentage']

    bar_length = 50
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)

    print(f"  [{bar}] {percentage:.1f}%")
    print(f"  Tasks: {completed}/{total} completed")
EOF
echo ""

# Suggest next command based on phase
echo -e "${GREEN}Suggested Next Command:${NC}"

case $CURRENT_PHASE in
    0)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 0 (Initialization). Next: Create complete directory structure.\"${NC}"
        ;;
    1)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 1 (Foundation). Check PROJECT_STATE.json for current day.\"${NC}"
        ;;
    2)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 2 (Core Algorithms). Implement heat diffusion engine.\"${NC}"
        ;;
    3)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 3 (Multi-Agent System). Implement AI agents.\"${NC}"
        ;;
    4)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 4 (Frontend). Build React dashboard.\"${NC}"
        ;;
    5)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 5 (Integration & Testing). Run integration tests.\"${NC}"
        ;;
    6)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT Phase 6 (Production Deployment). Deploy to production.\"${NC}"
        ;;
    *)
        echo -e "  ${YELLOW}claude-code \"Continue RAGHEAT implementation. Check PROJECT_STATE.json for details.\"${NC}"
        ;;
esac
echo ""

# Check for Git changes (if in a Git repo)
if [ -d ".git" ]; then
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Uncommitted changes detected!${NC}"
        echo "  Consider committing before continuing:"
        echo "  git add . && git commit -m \"Progress update\""
        echo ""
    fi
fi

# Offer to auto-start with Claude Code (interactive mode)
read -p "$(echo -e ${GREEN}Start Claude Code now? [y/N]:${NC} )" -n 1 -r
echo
if [[ $RPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Launching Claude Code...${NC}"

    # Create context message for Claude
    CONTEXT_MSG="Continue RAGHEAT implementation.

Current Phase: PHASE $CURRENT_PHASE - $PHASE_NAME
Progress: ${PROGRESS}%

Please:
1. Read PROJECT_STATE.json to see current status
2. Read IMPLEMENTATION_PLAN_WORLD_CLASS.md for next steps
3. Continue from where we left off
4. Update PROJECT_STATE.json as you complete tasks

Ready to continue?"

    # This would launch Claude Code if available
    # For now, just display the message
    echo ""
    echo -e "${BLUE}Copy this message for Claude Code:${NC}"
    echo "─────────────────────────────────────────────"
    echo "$CONTEXT_MSG"
    echo "─────────────────────────────────────────────"
else
    echo -e "${GREEN}Run the suggested command above when ready.${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}Resume script complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
