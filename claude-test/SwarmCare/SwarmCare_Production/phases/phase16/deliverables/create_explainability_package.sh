#!/bin/bash
#
# Create Explainability Package Script
# Packages all deliverables into a distributable archive
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHASE_DIR="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="swarmcare_explainability_phase16_${TIMESTAMP}"
TEMP_DIR="/tmp/${PACKAGE_NAME}"
OUTPUT_FILE="${SCRIPT_DIR}/${PACKAGE_NAME}.zip"

echo "======================================================================"
echo "SwarmCare Phase 16 - Explainability Package Creator"
echo "======================================================================"
echo ""

# Create temporary directory
echo -e "${YELLOW}Creating temporary package directory...${NC}"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Create package structure
mkdir -p "$TEMP_DIR/scripts"
mkdir -p "$TEMP_DIR/data"
mkdir -p "$TEMP_DIR/reports"
mkdir -p "$TEMP_DIR/docs"

echo -e "${GREEN}✓${NC} Package structure created"

# Copy scripts
echo -e "${YELLOW}Copying production scripts...${NC}"
if [ -f "$SCRIPT_DIR/generate_explanations.py" ]; then
    cp "$SCRIPT_DIR/generate_explanations.py" "$TEMP_DIR/scripts/"
    echo -e "${GREEN}✓${NC} generate_explanations.py"
fi

if [ -f "$SCRIPT_DIR/validate_explanations.py" ]; then
    cp "$SCRIPT_DIR/validate_explanations.py" "$TEMP_DIR/scripts/"
    echo -e "${GREEN}✓${NC} validate_explanations.py"
fi

if [ -f "$SCRIPT_DIR/export_explanations.py" ]; then
    cp "$SCRIPT_DIR/export_explanations.py" "$TEMP_DIR/scripts/"
    echo -e "${GREEN}✓${NC} export_explanations.py"
fi

if [ -f "$SCRIPT_DIR/create_explainability_package.sh" ]; then
    cp "$SCRIPT_DIR/create_explainability_package.sh" "$TEMP_DIR/scripts/"
    echo -e "${GREEN}✓${NC} create_explainability_package.sh"
fi

# Copy data files
echo -e "${YELLOW}Copying data files...${NC}"
for file in "$SCRIPT_DIR"/*.json; do
    if [ -f "$file" ]; then
        cp "$file" "$TEMP_DIR/data/"
        echo -e "${GREEN}✓${NC} $(basename "$file")"
    fi
done

# Copy code implementation if exists
if [ -d "$PHASE_DIR/code" ]; then
    echo -e "${YELLOW}Copying implementation code...${NC}"
    cp -r "$PHASE_DIR/code" "$TEMP_DIR/"
    echo -e "${GREEN}✓${NC} Implementation code copied"
fi

# Copy documentation if exists
if [ -d "$PHASE_DIR/docs" ]; then
    echo -e "${YELLOW}Copying documentation...${NC}"
    cp -r "$PHASE_DIR/docs/"* "$TEMP_DIR/docs/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Documentation copied"
fi

# Copy README if exists
if [ -f "$PHASE_DIR/README.md" ]; then
    cp "$PHASE_DIR/README.md" "$TEMP_DIR/"
    echo -e "${GREEN}✓${NC} README.md copied"
fi

# Create package README
echo -e "${YELLOW}Creating package README...${NC}"
cat > "$TEMP_DIR/README.md" << 'EOF'
# SwarmCare Phase 16: Explainable AI & Interpretability Package

This package contains all deliverables for Phase 16 of the SwarmCare project.

## Contents

### Scripts (./scripts/)
- `generate_explanations.py` - Generate SHAP, LIME, attention, and decision explanations
- `validate_explanations.py` - Validate explanation quality and correctness
- `export_explanations.py` - Export explanations to JSON, HTML, or PDF formats
- `create_explainability_package.sh` - Create distribution package

### Data Files (./data/)
- `shap_explanations_data.json` - Sample SHAP explanations
- `lime_explanations_data.json` - Sample LIME explanations
- `attention_visualizations_data.json` - Sample attention visualizations
- `decision_explanations_data.json` - Sample decision explanations
- `feature_importance_data.json` - Feature importance rankings
- `explainability_metrics.json` - Performance metrics
- `clinical_use_cases.json` - Clinical use case examples
- `explanation_templates.json` - Explanation templates

## Quick Start

### Generate Explanations
```bash
python3 scripts/generate_explanations.py --model swarmcare_v1 --count 10 --output ./output/
```

### Validate Explanations
```bash
python3 scripts/validate_explanations.py --all ./output/ --report validation_report.json
```

### Export to HTML
```bash
python3 scripts/export_explanations.py --format html --input ./output/shap_explanations.json --output report.html
```

## Requirements
- Python 3.7+
- Standard library only (no external dependencies for basic functionality)

## Documentation
See `./docs/` for detailed documentation and technical specifications.

## License
Copyright SwarmCare 2025. All rights reserved.
EOF

echo -e "${GREEN}✓${NC} Package README created"

# Create installation instructions
cat > "$TEMP_DIR/INSTALL.txt" << 'EOF'
SwarmCare Phase 16 - Installation Instructions
===============================================

1. Extract this archive to your desired location
2. Make scripts executable:
   chmod +x scripts/*.py scripts/*.sh

3. Run scripts from the package root directory
4. For help on any script, use --help flag:
   python3 scripts/generate_explanations.py --help

For full documentation, see README.md
EOF

echo -e "${GREEN}✓${NC} Installation instructions created"

# Create manifest file
echo -e "${YELLOW}Creating package manifest...${NC}"
cat > "$TEMP_DIR/MANIFEST.txt" << EOF
SwarmCare Phase 16 Explainability Package
Package: ${PACKAGE_NAME}
Created: $(date)
Platform: $(uname -s)

Contents:
EOF

# List all files in package
find "$TEMP_DIR" -type f -exec basename {} \; | sort | while read file; do
    echo "  - $file" >> "$TEMP_DIR/MANIFEST.txt"
done

echo -e "${GREEN}✓${NC} Manifest created"

# Create the ZIP archive
echo -e "${YELLOW}Creating ZIP archive...${NC}"
cd "$(dirname "$TEMP_DIR")"
zip -r "$OUTPUT_FILE" "$(basename "$TEMP_DIR")" > /dev/null 2>&1

if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo -e "${GREEN}✓${NC} Archive created successfully"
    echo ""
    echo "======================================================================"
    echo "Package Details:"
    echo "======================================================================"
    echo "Name: ${PACKAGE_NAME}.zip"
    echo "Location: $OUTPUT_FILE"
    echo "Size: $FILE_SIZE"
    echo "======================================================================"
else
    echo -e "${RED}✗${NC} Failed to create archive"
    exit 1
fi

# Cleanup
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"
echo -e "${GREEN}✓${NC} Cleanup complete"

echo ""
echo -e "${GREEN}Package creation completed successfully!${NC}"
echo ""
echo "To extract and use:"
echo "  unzip ${PACKAGE_NAME}.zip"
echo "  cd ${PACKAGE_NAME}"
echo "  chmod +x scripts/*.py scripts/*.sh"
echo ""
