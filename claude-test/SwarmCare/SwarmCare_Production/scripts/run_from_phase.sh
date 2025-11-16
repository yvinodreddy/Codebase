#!/bin/bash
################################################################################
# RUN FROM PHASE - Execute current phase from within phase directory
# Usage: From any phase directory, run: ../../scripts/run_from_phase.sh
# Or use: ../../continue (if symlinked)
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Detect which phase we're in
CURRENT_DIR=$(pwd)
PHASE_NAME=$(basename "$CURRENT_DIR")

# Extract phase number
if [[ $PHASE_NAME =~ phase([0-9]+) ]]; then
    PHASE_ID=${BASH_REMATCH[1]}
    # Remove leading zero
    PHASE_ID=$((10#$PHASE_ID))
else
    echo -e "${RED}❌ Cannot determine phase number from directory: $PHASE_NAME${NC}"
    echo -e "${YELLOW}Are you in a phase directory (phases/phaseXX)?${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}📍 Detected: Phase $PHASE_ID${NC}"
echo ""

# Find root directory
if [ -f "../../continue" ]; then
    ROOT_DIR="../../"
elif [ -f "../../../continue" ]; then
    ROOT_DIR="../../../"
else
    echo -e "${RED}❌ Cannot find root directory${NC}"
    exit 1
fi

# Run phase through tracker
cd "$ROOT_DIR"
./scripts/start_phase.sh $PHASE_ID
