#!/bin/bash
###############################################################################
# Phase 24: Production Package Creation Script
# Creates deployment-ready package for Phase 24 deliverables
#
# This script:
# - Validates all deliverables
# - Runs test suite
# - Creates deployment package
# - Generates checksums
# - Creates documentation bundle
#
# Usage:
#   ./create_phase24_package.sh [OPTIONS]
#
# Options:
#   --output-dir DIR    Output directory (default: ./dist)
#   --skip-tests        Skip test execution
#   --verbose           Enable verbose output
#   --include-source    Include source code in package
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHASE_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="./dist"
SKIP_TESTS=false
VERBOSE=false
INCLUDE_SOURCE=false
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="phase24_deliverables_${TIMESTAMP}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --include-source)
            INCLUDE_SOURCE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Print functions
print_header() {
    echo -e "\n${BLUE}======================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}➜${NC} $1"
}

# Main execution
print_header "Phase 24: Production Package Creation"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Output Directory: $OUTPUT_DIR"
echo "Package Name: $PACKAGE_NAME"

# Step 1: Validate environment
print_info "Validating environment..."

if ! command -v python3 &> /dev/null; then
    print_error "python3 not found"
    exit 1
fi
print_success "Python 3 available"

if ! command -v tar &> /dev/null; then
    print_error "tar not found"
    exit 1
fi
print_success "tar available"

# Step 2: Run tests (unless skipped)
if [ "$SKIP_TESTS" = false ]; then
    print_info "Running test suite..."
    cd "$PHASE_DIR"

    if python3 -m pytest tests/ -v --tb=short; then
        print_success "All tests passed"
    else
        print_error "Tests failed"
        exit 1
    fi
else
    print_info "Skipping tests (--skip-tests flag set)"
fi

# Step 3: Create output directory
print_info "Creating package directory..."
PACKAGE_DIR="${OUTPUT_DIR}/${PACKAGE_NAME}"
mkdir -p "$PACKAGE_DIR"/{deliverables,docs,tests,data,scripts}
print_success "Package directory created: $PACKAGE_DIR"

# Step 4: Copy deliverables
print_info "Copying deliverables..."

# Copy scripts
cp "$SCRIPT_DIR"/*.py "$PACKAGE_DIR/scripts/" 2>/dev/null || true
cp "$SCRIPT_DIR"/*.sh "$PACKAGE_DIR/scripts/" 2>/dev/null || true
SCRIPT_COUNT=$(find "$PACKAGE_DIR/scripts" -type f | wc -l)
print_success "Copied $SCRIPT_COUNT scripts"

# Copy JSON data files
cp "$SCRIPT_DIR"/*.json "$PACKAGE_DIR/data/" 2>/dev/null || true
DATA_COUNT=$(find "$PACKAGE_DIR/data" -type f | wc -l)
print_success "Copied $DATA_COUNT data files"

# Copy documentation
cp "$SCRIPT_DIR"/*.md "$PACKAGE_DIR/docs/" 2>/dev/null || true
DOC_COUNT=$(find "$PACKAGE_DIR/docs" -type f | wc -l)
print_success "Copied $DOC_COUNT documentation files"

# Step 5: Include source code if requested
if [ "$INCLUDE_SOURCE" = true ]; then
    print_info "Including source code..."
    mkdir -p "$PACKAGE_DIR/source"
    cp -r "$PHASE_DIR/code" "$PACKAGE_DIR/source/"
    cp -r "$PHASE_DIR/tests" "$PACKAGE_DIR/source/"
    print_success "Source code included"
fi

# Step 6: Generate manifest
print_info "Generating manifest..."
MANIFEST_FILE="$PACKAGE_DIR/MANIFEST.txt"

cat > "$MANIFEST_FILE" << EOF
Phase 24: 100% Automated Coding & EHR Integration
Production Package Manifest

Generated: $(date '+%Y-%m-%d %H:%M:%S')
Package: $PACKAGE_NAME

Contents:
=========

Scripts:
EOF

find "$PACKAGE_DIR/scripts" -type f -exec basename {} \; | sort >> "$MANIFEST_FILE"

cat >> "$MANIFEST_FILE" << EOF

Data Files:
EOF

find "$PACKAGE_DIR/data" -type f -exec basename {} \; | sort >> "$MANIFEST_FILE"

cat >> "$MANIFEST_FILE" << EOF

Documentation:
EOF

find "$PACKAGE_DIR/docs" -type f -exec basename {} \; | sort >> "$MANIFEST_FILE"

print_success "Manifest generated"

# Step 7: Generate checksums
print_info "Generating checksums..."
CHECKSUM_FILE="$PACKAGE_DIR/SHA256SUMS"

cd "$PACKAGE_DIR"
find . -type f ! -name "SHA256SUMS" -exec sha256sum {} \; > SHA256SUMS
cd - > /dev/null

CHECKSUM_COUNT=$(wc -l < "$CHECKSUM_FILE")
print_success "Generated checksums for $CHECKSUM_COUNT files"

# Step 8: Set executable permissions
print_info "Setting executable permissions..."
chmod +x "$PACKAGE_DIR/scripts"/*.py 2>/dev/null || true
chmod +x "$PACKAGE_DIR/scripts"/*.sh 2>/dev/null || true
print_success "Permissions set"

# Step 9: Create README for package
print_info "Creating package README..."
cat > "$PACKAGE_DIR/README.txt" << 'EOF'
Phase 24: 100% Automated Coding & EHR Integration
Production Deliverables Package

OVERVIEW
========
This package contains production-ready deliverables for Phase 24 of the
SwarmCare system, implementing 100% automated medical coding and integration
with 8 major EHR systems.

EHR SYSTEMS SUPPORTED
====================
- Epic (Epic Systems)
- Cerner (Oracle Health)
- Allscripts
- athenahealth
- eClinicalWorks
- NextGen Healthcare
- MEDITECH
- Practice Fusion

AUTOMATED CODING
================
- ICD-10 diagnosis codes
- CPT procedure codes
- HCPCS supply codes

DIRECTORY STRUCTURE
===================
scripts/        - Executable Python scripts and shell scripts
data/          - JSON configuration and sample data files
docs/          - Comprehensive documentation (Markdown)
source/        - Source code (if included with --include-source)

QUICK START
===========
1. Review documentation in docs/README.md
2. Setup EHR integrations:
   python3 scripts/setup_ehr_integrations.py --test

3. Validate connections:
   python3 scripts/validate_ehr_connections.py --detailed

4. Generate billing reports:
   python3 scripts/generate_billing_reports.py --encounters 100

5. Export data:
   python3 scripts/export_integration_data.py --format all

VERIFICATION
============
To verify package integrity:
  sha256sum -c SHA256SUMS

REQUIREMENTS
============
- Python 3.8 or higher
- pytest (for testing)
- Network access to EHR systems

SUPPORT
=======
For issues or questions, refer to the comprehensive documentation in the
docs/ directory.

EOF

print_success "Package README created"

# Step 10: Create tarball
print_info "Creating tarball..."
cd "$OUTPUT_DIR"
TARBALL_NAME="${PACKAGE_NAME}.tar.gz"
tar -czf "$TARBALL_NAME" "$PACKAGE_NAME"
TARBALL_SIZE=$(du -h "$TARBALL_NAME" | cut -f1)
cd - > /dev/null

print_success "Tarball created: $TARBALL_NAME ($TARBALL_SIZE)"

# Step 11: Generate final checksum for tarball
print_info "Generating tarball checksum..."
cd "$OUTPUT_DIR"
sha256sum "$TARBALL_NAME" > "${TARBALL_NAME}.sha256"
TARBALL_CHECKSUM=$(cat "${TARBALL_NAME}.sha256" | cut -d' ' -f1)
cd - > /dev/null

print_success "Checksum: $TARBALL_CHECKSUM"

# Step 12: Generate deployment summary
print_info "Generating deployment summary..."
SUMMARY_FILE="${OUTPUT_DIR}/deployment_summary.txt"

cat > "$SUMMARY_FILE" << EOF
Phase 24: Deployment Package Summary
=====================================

Package Information:
--------------------
Name: $PACKAGE_NAME
Created: $(date '+%Y-%m-%d %H:%M:%S')
Tarball: $TARBALL_NAME
Size: $TARBALL_SIZE
SHA256: $TARBALL_CHECKSUM

Contents:
---------
Scripts: $SCRIPT_COUNT
Data Files: $DATA_COUNT
Documentation: $DOC_COUNT
Total Files: $CHECKSUM_COUNT

Deployment Steps:
-----------------
1. Extract package:
   tar -xzf $TARBALL_NAME

2. Navigate to package:
   cd $PACKAGE_NAME

3. Verify integrity:
   sha256sum -c SHA256SUMS

4. Review documentation:
   cat docs/README.md

5. Run setup:
   python3 scripts/setup_ehr_integrations.py --test

Verification:
-------------
All files have been checksummed (SHA256SUMS)
Package integrity can be verified
All scripts have executable permissions

Status: READY FOR DEPLOYMENT
EOF

print_success "Deployment summary created"

# Final summary
print_header "Package Creation Complete"
echo "Package Directory: $PACKAGE_DIR"
echo "Tarball: ${OUTPUT_DIR}/${TARBALL_NAME}"
echo "Size: $TARBALL_SIZE"
echo ""
echo "Contents:"
echo "  - Scripts: $SCRIPT_COUNT"
echo "  - Data Files: $DATA_COUNT"
echo "  - Documentation: $DOC_COUNT"
echo "  - Total Files: $CHECKSUM_COUNT"
echo ""
echo "Next Steps:"
echo "  1. Review: cat ${OUTPUT_DIR}/deployment_summary.txt"
echo "  2. Extract: tar -xzf ${OUTPUT_DIR}/${TARBALL_NAME}"
echo "  3. Deploy: Follow instructions in package README.txt"
echo ""
print_success "Package is ready for deployment!"

exit 0
