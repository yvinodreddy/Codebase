#!/bin/bash
################################################################################
# COMPLETE PHASE - Mark phase as complete and sync to tracker
# Usage: ./scripts/complete_phase.sh <phase_id>
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

echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ COMPLETING PHASE $PHASE_ID${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Mark phase as completed
python3 scripts/sync_tracker.py complete $PHASE_ID

echo ""
echo -e "${GREEN}🎉 Phase $PHASE_ID marked as COMPLETE!${NC}"
echo ""

# Show next phase
NEXT_PHASE=$((PHASE_ID + 1))
if [ $NEXT_PHASE -lt 29 ]; then
    echo -e "${YELLOW}Next: Start Phase $NEXT_PHASE${NC}"
    echo -e "  ${CYAN}./scripts/start_phase.sh $NEXT_PHASE${NC}"
    echo ""
    echo -e "${YELLOW}Or check overall status:${NC}"
    echo -e "  ${CYAN}./scripts/status.sh${NC}"
else
    echo -e "${GREEN}🏆 ALL 29 PHASES COMPLETE! CONGRATULATIONS!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Package all phases: ${CYAN}./scripts/package_all.sh${NC}"
    echo -e "  2. Run final validation: ${CYAN}python3 comprehensive_validation_tests.py${NC}"
fi

echo ""
