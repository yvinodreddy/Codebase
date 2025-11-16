#!/usr/bin/env bash
#
# QUICK INTEGRATION
# Run this on the integration system to quickly integrate all phases
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║  QUICK INTEGRATION                    ║
║  SwarmCare Integration System          ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo "This script will guide you through the integration process."
echo ""

cd "$START_DIR"

# Step 1: Check for collected packages
echo -e "${BLUE}Step 1: Checking for packages...${NC}"
echo ""

packages_dir="collected_packages"

if [[ ! -d "$packages_dir" ]]; then
    echo -e "${YELLOW}Creating packages directory...${NC}"
    mkdir -p "$packages_dir"
fi

package_count=$(find "$packages_dir" -name "*_phases.tar.gz" 2>/dev/null | wc -l)

if [[ $package_count -eq 0 ]]; then
    echo -e "${RED}No packages found in $packages_dir${NC}"
    echo ""
    echo "Please copy all machine_XX_phases.tar.gz files to this directory first."
    echo ""
    echo "Methods:"
    echo "  - USB: cp /media/usb/machine_*_phases.tar.gz* $packages_dir/"
    echo "  - Network: scp dev-machine:/path/machine_*_phases.tar.gz* $packages_dir/"
    echo "  - Cloud: Download from cloud storage to $packages_dir/"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Found $package_count package(s)${NC}"
echo ""

# Step 2: Collect phases
echo -e "${BLUE}Step 2: Collecting and extracting phases...${NC}"
echo ""

./COLLECT_PHASES.sh --source "$packages_dir"

echo ""

# Step 3: Validate
echo -e "${BLUE}Step 3: Validating collection...${NC}"
echo ""

if ! ./COLLECT_PHASES.sh --validate; then
    echo ""
    echo -e "${RED}Validation failed!${NC}"
    echo "Please fix the issues and re-run this script."
    exit 1
fi

echo ""

# Step 4: Dry run (optional)
echo -e "${YELLOW}Step 4: Dry run (optional)${NC}"
echo ""
read -p "Run dry-run first to see what would happen? [Y/n] " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo ""
    echo "Running dry-run..."
    ./INTEGRATE_ALL.sh --dry-run
    echo ""
fi

# Step 5: Final confirmation
echo ""
echo -e "${YELLOW}Ready for integration!${NC}"
echo ""
echo "This will:"
echo "  ✓ Validate all 29 phases"
echo "  ✓ Create backup of current state"
echo "  ✓ Merge all phases into project"
echo "  ✓ Run integration tests"
echo "  ✓ Generate comprehensive report"
echo ""
read -p "Continue with full integration? [Y/n] " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ -n $REPLY ]]; then
    echo "Integration cancelled"
    exit 0
fi

# Step 6: Run integration
echo ""
echo -e "${BLUE}Step 6: Running integration...${NC}"
echo ""

./INTEGRATE_ALL.sh

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}INTEGRATION COMPLETE!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo "Review the integration report:"
echo "  cat integration_reports/INTEGRATION_REPORT_*.md"
echo ""
echo "Check the project:"
echo "  cd .."
echo "  ls -la"
echo ""
echo -e "${GREEN}Project is now production ready! 🎉${NC}"
echo ""
