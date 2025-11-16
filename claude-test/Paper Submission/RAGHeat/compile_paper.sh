#!/bin/bash

##############################################################################
# Tesla Stock Heat Diffusion Model - Automated Compilation Script
# Production-ready paper compilation with full validation
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PAPER_NAME="tesla_heat_diffusion_model"
WORK_DIR="/home/user01/claude-test/Paper Submission/RAGHeat"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Tesla Stock Heat Diffusion Model - Paper Compiler            ║${NC}"
echo -e "${BLUE}║  Production-Ready Academic Paper Generation                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Change to working directory
cd "${WORK_DIR}" || exit 1

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for LaTeX installation
echo -e "${YELLOW}[1/6]${NC} Checking for LaTeX installation..."
if command_exists pdflatex; then
    echo -e "${GREEN}✓${NC} pdflatex found: $(which pdflatex)"
elif command_exists xelatex; then
    echo -e "${GREEN}✓${NC} xelatex found: $(which xelatex)"
    LATEX_CMD="xelatex"
elif command_exists lualatex; then
    echo -e "${GREEN}✓${NC} lualatex found: $(which lualatex)"
    LATEX_CMD="lualatex"
else
    echo -e "${RED}✗${NC} No LaTeX compiler found!"
    echo ""
    echo -e "${YELLOW}Please install LaTeX:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  macOS: brew install --cask mactex"
    echo "  Windows: Download from https://miktex.org/"
    echo ""
    exit 1
fi

# Set default LaTeX command
LATEX_CMD="${LATEX_CMD:-pdflatex}"

# Check if source file exists
echo -e "${YELLOW}[2/6]${NC} Verifying source file..."
if [ ! -f "${PAPER_NAME}.tex" ]; then
    echo -e "${RED}✗${NC} Source file ${PAPER_NAME}.tex not found!"
    exit 1
fi
echo -e "${GREEN}✓${NC} Source file found: ${PAPER_NAME}.tex"

# Check for screenshot reference
echo -e "${YELLOW}[3/6]${NC} Checking reference images..."
if [ ! -f "Screenshot 2025-11-08 at 12.36.13 PM.png" ]; then
    echo -e "${YELLOW}⚠${NC} Screenshot not found (optional)"
else
    echo -e "${GREEN}✓${NC} Screenshot reference found"

    # Resize if needed
    if command_exists identify && command_exists convert; then
        SIZE=$(identify -format "%wx%h" "Screenshot 2025-11-08 at 12.36.13 PM.png")
        echo "  Image size: $SIZE"

        if command_exists python3; then
            echo "  Running image optimization..."
            python3 resize_issues.py 2>/dev/null || true
        fi
    fi
fi

# Clean previous build artifacts
echo -e "${YELLOW}[4/6]${NC} Cleaning previous build artifacts..."
rm -f "${PAPER_NAME}.aux" "${PAPER_NAME}.log" "${PAPER_NAME}.out" \
      "${PAPER_NAME}.bbl" "${PAPER_NAME}.blg" "${PAPER_NAME}.toc" \
      "${PAPER_NAME}.synctex.gz"
echo -e "${GREEN}✓${NC} Build directory cleaned"

# Compile LaTeX (multiple passes for references)
echo -e "${YELLOW}[5/6]${NC} Compiling LaTeX document..."
echo "  Using: ${LATEX_CMD}"

for PASS in 1 2 3; do
    echo -e "  Pass ${PASS}/3..."
    ${LATEX_CMD} -interaction=nonstopmode -halt-on-error "${PAPER_NAME}.tex" > /dev/null 2>&1 || {
        echo -e "${RED}✗${NC} Compilation failed on pass ${PASS}"
        echo ""
        echo "Error details:"
        tail -20 "${PAPER_NAME}.log"
        exit 1
    }
done

echo -e "${GREEN}✓${NC} Compilation successful!"

# Verify PDF output
echo -e "${YELLOW}[6/6]${NC} Verifying PDF output..."
if [ ! -f "${PAPER_NAME}.pdf" ]; then
    echo -e "${RED}✗${NC} PDF not generated!"
    exit 1
fi

PDF_SIZE=$(du -h "${PAPER_NAME}.pdf" | cut -f1)
echo -e "${GREEN}✓${NC} PDF generated: ${PAPER_NAME}.pdf (${PDF_SIZE})"

# Display PDF info if pdfinfo is available
if command_exists pdfinfo; then
    PAGES=$(pdfinfo "${PAPER_NAME}.pdf" | grep "Pages:" | awk '{print $2}')
    echo "  Pages: ${PAGES}"
fi

# Optional: Generate diagrams if Python is available
echo ""
echo -e "${BLUE}[OPTIONAL]${NC} Generate additional diagrams?"
if command_exists python3; then
    echo "Python3 found. To generate diagrams, run:"
    echo "  python3 generate_diagrams.py"
else
    echo "Python3 not found. Diagrams generation skipped."
fi

# Success summary
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ COMPILATION SUCCESSFUL                                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Output:${NC} ${PAPER_NAME}.pdf"
echo -e "${GREEN}Size:${NC} ${PDF_SIZE}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Review PDF: open ${PAPER_NAME}.pdf"
echo "  2. Generate diagrams: python3 generate_diagrams.py"
echo "  3. Submit to conference/journal"
echo ""
echo -e "${YELLOW}Paper Highlights:${NC}"
echo "  • Comprehensive 10-category factor taxonomy"
echo "  • Heat diffusion equations with Σwᵢ = 1.0 constraint"
echo "  • Dynamic weight optimization (HMM + Kalman)"
echo "  • Neo4j implementation with < 1.7s latency"
echo "  • Sharpe ratio: 0.63, Info ratio: 0.43"
echo ""
echo -e "${GREEN}✓ Production ready!${NC}"
echo ""
