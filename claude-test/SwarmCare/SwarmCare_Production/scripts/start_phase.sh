#!/bin/bash
################################################################################
# START PHASE - Run a phase through the tracker
# Usage: ./scripts/start_phase.sh <phase_id>
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ $# -lt 1 ]; then
    echo -e "${RED}Usage: $0 <phase_id>${NC}"
    echo -e "Example: $0 0"
    exit 1
fi

PHASE_ID=$1
PHASE_DIR="phases/phase$(printf "%02d" $PHASE_ID)"
IMPL_FILE="$PHASE_DIR/code/implementation.py"

# Check if phase exists
if [ ! -d "$PHASE_DIR" ]; then
    echo -e "${RED}❌ Phase $PHASE_ID does not exist${NC}"
    exit 1
fi

if [ ! -f "$IMPL_FILE" ]; then
    echo -e "${RED}❌ Implementation file not found: $IMPL_FILE${NC}"
    exit 1
fi

echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 STARTING PHASE $PHASE_ID THROUGH TRACKER${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Mark phase as started in tracker
python3 scripts/sync_tracker.py start $PHASE_ID

echo ""
echo -e "${GREEN}📍 Running implementation...${NC}"
echo ""

# Run the phase
cd "$PHASE_DIR/code"
python3 implementation.py
EXIT_CODE=$?
cd ../../..

echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Phase $PHASE_ID completed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}To mark as complete and move to next phase:${NC}"
    echo -e "  ${CYAN}./scripts/complete_phase.sh $PHASE_ID${NC}"
else
    echo -e "${RED}❌ Phase $PHASE_ID failed with exit code $EXIT_CODE${NC}"
    echo ""
    echo -e "${YELLOW}Check logs and re-run when fixed:${NC}"
    echo -e "  ${CYAN}./scripts/start_phase.sh $PHASE_ID${NC}"
fi

echo ""
