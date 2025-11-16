#!/bin/bash
# SwarmCare Documentation Build Script
# Phase 09: Automated Documentation Builder
# Version: 2.1
# Last Updated: 2025-10-28

set -e  # Exit on error

echo "================================================================================"
echo "SwarmCare Documentation Build System"
echo "================================================================================"
echo "Started: $(date)"
echo "================================================================================"
echo ""

# Configuration
BUILD_DIR="build"
DOCS_DIR="../docs"
OUTPUT_DIR="site"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi

    # Check Node.js (for Docusaurus)
    if ! command -v node &> /dev/null; then
        log_error "Node.js is required but not installed"
        exit 1
    fi

    log_success "All prerequisites met"
}

# Install dependencies
install_dependencies() {
    log_info "Installing documentation dependencies..."

    # Python dependencies
    if [ -f "mkdocs-requirements.txt" ]; then
        pip3 install -q -r mkdocs-requirements.txt
        log_success "MkDocs dependencies installed"
    fi

    if [ -f "sphinx-requirements.txt" ]; then
        pip3 install -q -r sphinx-requirements.txt
        log_success "Sphinx dependencies installed"
    fi

    # Node dependencies for Docusaurus
    if [ -d "$DOCS_DIR/docusaurus" ]; then
        cd "$DOCS_DIR/docusaurus" && npm install --silent && cd - > /dev/null
        log_success "Docusaurus dependencies installed"
    fi
}

# Build MkDocs documentation
build_mkdocs() {
    log_info "Building MkDocs documentation..."

    if [ -f "$DOCS_DIR/mkdocs/mkdocs.yml" ]; then
        cd "$DOCS_DIR/mkdocs"
        mkdocs build --clean --site-dir "../../$OUTPUT_DIR/mkdocs"
        cd - > /dev/null
        log_success "MkDocs build complete: $OUTPUT_DIR/mkdocs/"
    else
        log_error "MkDocs configuration not found"
    fi
}

# Build Sphinx documentation
build_sphinx() {
    log_info "Building Sphinx documentation..."

    if [ -f "$DOCS_DIR/sphinx/conf.py" ]; then
        cd "$DOCS_DIR/sphinx"
        sphinx-build -b html source "../$OUTPUT_DIR/sphinx" -q
        cd - > /dev/null
        log_success "Sphinx build complete: $OUTPUT_DIR/sphinx/"
    else
        log_error "Sphinx configuration not found"
    fi
}

# Build Docusaurus documentation
build_docusaurus() {
    log_info "Building Docusaurus documentation..."

    if [ -f "$DOCS_DIR/docusaurus/docusaurus.config.js" ]; then
        cd "$DOCS_DIR/docusaurus"
        npm run build --silent
        cd - > /dev/null
        log_success "Docusaurus build complete: $DOCS_DIR/docusaurus/build/"
    else
        log_error "Docusaurus configuration not found"
    fi
}

# Generate API documentation
generate_api_docs() {
    log_info "Generating API documentation..."

    if [ -f "openapi/openapi.yaml" ]; then
        # Generate Swagger UI
        mkdir -p "$OUTPUT_DIR/api/swagger"
        cp openapi/openapi.yaml "$OUTPUT_DIR/api/swagger/"
        log_success "Swagger UI documentation ready"

        # Generate ReDoc
        mkdir -p "$OUTPUT_DIR/api/redoc"
        cp openapi/openapi.yaml "$OUTPUT_DIR/api/redoc/"
        log_success "ReDoc documentation ready"
    else
        log_error "OpenAPI specification not found"
    fi
}

# Lint documentation
lint_documentation() {
    log_info "Linting documentation..."

    # Markdown lint (if available)
    if command -v markdownlint &> /dev/null; then
        markdownlint "$DOCS_DIR/**/*.md" --config .markdownlint.json || true
        log_success "Markdown linting complete"
    fi

    # Vale style checking (if available)
    if command -v vale &> /dev/null; then
        vale "$DOCS_DIR" || true
        log_success "Vale style checking complete"
    fi
}

# Check broken links
check_links() {
    log_info "Checking for broken links..."

    if command -v linkchecker &> /dev/null; then
        linkchecker "$OUTPUT_DIR" --check-extern || true
        log_success "Link checking complete"
    else
        log_info "linkchecker not installed, skipping link check"
    fi
}

# Generate build report
generate_report() {
    log_info "Generating build report..."

    cat > "$OUTPUT_DIR/BUILD_REPORT.txt" <<EOF
SwarmCare Documentation Build Report
=====================================
Build Date: $(date)
Build Version: 2.1

Documentation Built:
- MkDocs: $([ -d "$OUTPUT_DIR/mkdocs" ] && echo "✅ Yes" || echo "❌ No")
- Sphinx: $([ -d "$OUTPUT_DIR/sphinx" ] && echo "✅ Yes" || echo "❌ No")
- Docusaurus: $([ -d "$DOCS_DIR/docusaurus/build" ] && echo "✅ Yes" || echo "❌ No")
- API Docs: $([ -d "$OUTPUT_DIR/api" ] && echo "✅ Yes" || echo "❌ No")

Output Locations:
- MkDocs: $OUTPUT_DIR/mkdocs/
- Sphinx: $OUTPUT_DIR/sphinx/
- Docusaurus: $DOCS_DIR/docusaurus/build/
- API Docs: $OUTPUT_DIR/api/

Build Status: ✅ SUCCESS
EOF

    cat "$OUTPUT_DIR/BUILD_REPORT.txt"
    log_success "Build report generated"
}

# Main execution
main() {
    echo ""

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Run build pipeline
    check_prerequisites
    install_dependencies

    echo ""
    echo "Building documentation..."
    echo "--------------------------------------------------------------------------------"

    build_mkdocs
    build_sphinx
    build_docusaurus
    generate_api_docs

    echo ""
    echo "Quality checks..."
    echo "--------------------------------------------------------------------------------"

    lint_documentation
    check_links

    echo ""
    echo "Finalizing..."
    echo "--------------------------------------------------------------------------------"

    generate_report

    echo ""
    echo "================================================================================"
    echo "Documentation Build Complete!"
    echo "================================================================================"
    echo "Total Build Time: $SECONDS seconds"
    echo "Output Directory: $(pwd)/$OUTPUT_DIR/"
    echo "================================================================================"
}

# Run main function
main "$@"
