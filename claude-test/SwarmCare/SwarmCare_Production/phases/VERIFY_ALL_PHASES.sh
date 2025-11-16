#!/bin/bash
# Master Verification Script for All 29 Phases
# Verifies that all phases have complete standalone testing structure

echo "================================================================================"
echo "                 MASTER PHASE VERIFICATION SCRIPT"
echo "                     SwarmCare - All 29 Phases"
echo "================================================================================"
echo ""

TOTAL_PHASES=29
VERIFIED_PHASES=0
FAILED_PHASES=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to verify a single phase
verify_phase() {
    local phase_num=$1
    local phase_name=$2
    local port=$3

    echo ""
    echo "--------------------------------------------------------------------------------"
    echo "Phase $phase_num: $phase_name (Port $port)"
    echo "--------------------------------------------------------------------------------"

    local phase_dir="phase$(printf "%02d" $phase_num)"
    local all_good=true

    # Check directory structure
    echo -n "  Checking directory structure... "
    if [ -d "$phase_dir/standalone_testing" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing standalone_testing${NC}"
        all_good=false
    fi

    # Check app.py
    echo -n "  Checking app.py... "
    if [ -f "$phase_dir/standalone_testing/deployment/app.py" ]; then
        local size=$(wc -l < "$phase_dir/standalone_testing/deployment/app.py")
        if [ $size -gt 100 ]; then
            echo -e "${GREEN}✅ ($size lines)${NC}"
        else
            echo -e "${YELLOW}⚠️  ($size lines - seems small)${NC}"
        fi
    else
        echo -e "${RED}❌ Missing${NC}"
        all_good=false
    fi

    # Check unified_tracker.py
    echo -n "  Checking unified_tracker.py... "
    if [ -f "$phase_dir/standalone_testing/deployment/unified_tracker.py" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing${NC}"
        all_good=false
    fi

    # Check comprehensive_test.py
    echo -n "  Checking comprehensive_test.py... "
    if [ -f "$phase_dir/standalone_testing/deployment/comprehensive_test.py" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing${NC}"
        all_good=false
    fi

    # Check START_APPLICATION.sh
    echo -n "  Checking START_APPLICATION.sh... "
    if [ -f "$phase_dir/standalone_testing/deployment/START_APPLICATION.sh" ] && [ -x "$phase_dir/standalone_testing/deployment/START_APPLICATION.sh" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing or not executable${NC}"
        all_good=false
    fi

    # Check user_stories.json
    echo -n "  Checking user_stories.json... "
    if [ -f "$phase_dir/standalone_testing/requirements/user_stories.json" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing${NC}"
        all_good=false
    fi

    # Check phase_state.json
    echo -n "  Checking .state/phase_state.json... "
    if [ -f "$phase_dir/.state/phase_state.json" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌ Missing${NC}"
        all_good=false
    fi

    # Check documentation
    echo -n "  Checking documentation... "
    if [ -f "$phase_dir/standalone_testing/deployment/ACCESS_GUIDE.md" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${YELLOW}⚠️  ACCESS_GUIDE.md missing${NC}"
    fi

    # Overall status
    if [ "$all_good" = true ]; then
        echo -e "  ${GREEN}Status: ✅ COMPLETE${NC}"
        ((VERIFIED_PHASES++))
    else
        echo -e "  ${RED}Status: ❌ INCOMPLETE${NC}"
        ((FAILED_PHASES++))
    fi
}

# Verify all phases
verify_phase 0 "Foundation & Infrastructure" 8000
verify_phase 1 "RAG Heat System" 8001
verify_phase 2 "SWARMCARE Agents" 8002
verify_phase 3 "Workflow Orchestration" 8003
verify_phase 4 "Frontend Application" 8004
verify_phase 5 "Audio Generation" 8005
verify_phase 6 "HIPAA Compliance" 8006
verify_phase 7 "Testing & QA" 8007
verify_phase 8 "Production Deployment" 8008
verify_phase 9 "Documentation" 8009
verify_phase 10 "Business & Partnerships" 8010
verify_phase 11 "Research & Publications" 8011
verify_phase 12 "Real-time Clinical Decision Support" 8012
verify_phase 13 "Predictive Analytics & ML Models" 8013
verify_phase 14 "Multi-modal AI - Medical Imaging" 8014
verify_phase 15 "Advanced Medical NLP & Auto-Coding" 8015
verify_phase 16 "Explainable AI & Interpretability" 8016
verify_phase 17 "Population Health Management" 8017
verify_phase 18 "Clinical Trial Matching" 8018
verify_phase 19 "Voice AI & Ambient Intelligence" 8019
verify_phase 20 "Security Certifications (SOC 2, HITRUST)" 8020
verify_phase 21 "Closed-Loop Clinical Automation" 8021
verify_phase 22 "Continuous Learning & Federated ML" 8022
verify_phase 23 "FDA Clearance & PACS Integration" 8023
verify_phase 24 "100% Automated Coding & EHR Integration" 8024
verify_phase 25 "Validated Patient-Facing XAI" 8025
verify_phase 26 "Real-time CDC & Public Health Integration" 8026
verify_phase 27 "Full Trial Lifecycle (EDC, eConsent, AE)" 8027
verify_phase 28 "Ultra-fast Offline Voice AI" 8028

# Final summary
echo ""
echo "================================================================================"
echo "                         VERIFICATION SUMMARY"
echo "================================================================================"
echo ""
echo "Total Phases:      $TOTAL_PHASES"
echo -e "Verified:          ${GREEN}$VERIFIED_PHASES${NC}"
echo -e "Failed:            ${RED}$FAILED_PHASES${NC}"
echo -e "Success Rate:      $(echo "scale=1; $VERIFIED_PHASES * 100 / $TOTAL_PHASES" | bc)%"
echo ""

if [ $FAILED_PHASES -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════════"
    echo "                    ✅ ALL PHASES VERIFIED SUCCESSFULLY ✅"
    echo -e "═══════════════════════════════════════════════════════════════════════════════${NC}"
else
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════════════════"
    echo "                    ⚠️  SOME PHASES NEED ATTENTION ⚠️"
    echo -e "═══════════════════════════════════════════════════════════════════════════════${NC}"
fi

echo ""
echo "To start a specific phase:"
echo "  cd phaseXX/standalone_testing/deployment && ./START_APPLICATION.sh"
echo ""
echo "To access a phase:"
echo "  http://localhost:PORT"
echo ""
echo "Ports:"
echo "  Phase 00: http://localhost:8000"
echo "  Phase 01: http://localhost:8001"
echo "  Phase 02: http://localhost:8002"
echo "  ..."
echo "  Phase 28: http://localhost:8028"
echo ""
echo "================================================================================"
