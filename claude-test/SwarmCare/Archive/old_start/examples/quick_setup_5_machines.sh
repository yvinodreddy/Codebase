#!/usr/bin/env bash
#
# QUICK SETUP - 5 MACHINES
# Run this on each development machine with appropriate machine ID
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║  QUICK SETUP - 5 MACHINES             ║
║  SwarmCare Distributed Development     ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo "This script will help you quickly initialize a development machine"
echo "for the 5-machine distributed development setup."
echo ""

# Ask for machine ID
echo -e "${YELLOW}Which machine are you setting up?${NC}"
echo "  1) Machine 01 - Phases: 0,1,11,24,28 (Foundation + Core)"
echo "  2) Machine 02 - Phases: 2,3,16,18,20,21,22 (Agents + Advanced)"
echo "  3) Machine 03 - Phases: 4,5,9,14,25,26,27 (Frontend + UI)"
echo "  4) Machine 04 - Phases: 6,7,10,12,23 (Compliance + Testing)"
echo "  5) Machine 05 - Phases: 8,13,15,17,19 (Deployment + ML/AI)"
echo ""
read -p "Enter number (1-5): " choice

case $choice in
    1)
        machine_id="machine_01"
        phases="0,1,11,24,28"
        description="Foundation & Infrastructure, RAG Heat, Research, Automated Coding, Voice AI"
        critical="⚠️  CRITICAL: This machine has Phase 0 - Must complete first!"
        ;;
    2)
        machine_id="machine_02"
        phases="2,3,16,18,20,21,22"
        description="SWARMCARE Agents, Workflows, XAI, Trials, Security, Automation, ML"
        critical=""
        ;;
    3)
        machine_id="machine_03"
        phases="4,5,9,14,25,26,27"
        description="Frontend, Audio, Docs, Imaging, Patient XAI, Public Health, Trials"
        critical=""
        ;;
    4)
        machine_id="machine_04"
        phases="6,7,10,12,23"
        description="HIPAA, Testing, Business, Clinical Decision, FDA Clearance"
        critical=""
        ;;
    5)
        machine_id="machine_05"
        phases="8,13,15,17,19"
        description="Deployment, Predictive Analytics, NLP, Population Health, Voice AI"
        critical=""
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Setting up: $machine_id${NC}"
echo "Phases: $phases"
echo "Description: $description"
echo ""

if [[ -n "$critical" ]]; then
    echo -e "${YELLOW}$critical${NC}"
    echo ""
fi

read -p "Continue with setup? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled"
    exit 0
fi

# Run initialization
cd "$START_DIR"

echo ""
echo -e "${BLUE}Initializing machine...${NC}"
./DISTRIBUTED_EXECUTOR.sh init --machine-id "$machine_id" --phases "$phases"

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Next steps:"
if [[ "$machine_id" == "machine_01" ]]; then
    echo "  1. ⚠️  IMPORTANT: Complete Phase 0 FIRST before others start!"
    echo "  2. Run: ./DISTRIBUTED_EXECUTOR.sh execute"
    echo "  3. Notify team when Phase 0 is complete"
else
    echo "  1. Wait for notification that Phase 0 is complete"
    echo "  2. Run: ./DISTRIBUTED_EXECUTOR.sh execute"
fi
echo "  3. Check progress: ./DISTRIBUTED_EXECUTOR.sh status"
echo "  4. When done: ./DISTRIBUTED_EXECUTOR.sh validate"
echo "  5. Package: ./DISTRIBUTED_EXECUTOR.sh package"
echo ""
