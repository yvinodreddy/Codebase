#!/usr/bin/env bash
#
# SWARMCARE PHASE COLLECTOR
# Runs on the integration system to collect and organize phases from all machines
#
# Usage:
#   ./COLLECT_PHASES.sh --source /path/to/packages
#   ./COLLECT_PHASES.sh --validate
#   ./COLLECT_PHASES.sh --status
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTED_DIR="$SCRIPT_DIR/collected_phases"
COLLECTION_LOG="$SCRIPT_DIR/collection.log"
COLLECTION_REPORT="$SCRIPT_DIR/COLLECTION_REPORT.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                    PHASE COLLECTOR                                ║
║        Collect and Organize Phases from All Machines             ║
║                                                                   ║
║   Validates, extracts, and prepares for integration              ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Error handler
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ERROR: $1" >> "$COLLECTION_LOG"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SUCCESS: $1" >> "$COLLECTION_LOG"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) INFO: $1" >> "$COLLECTION_LOG"
}

# Warning message
warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) WARN: $1" >> "$COLLECTION_LOG"
}

# Progress message
progress() {
    echo -e "${MAGENTA}▶ $1${NC}"
}

# Collect phases from source directory
cmd_collect() {
    local source_dir=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --source)
                source_dir="$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    if [[ -z "$source_dir" ]]; then
        error "Missing --source parameter. Provide directory containing machine_XX_phases.tar.gz files"
    fi

    if [[ ! -d "$source_dir" ]]; then
        error "Source directory does not exist: $source_dir"
    fi

    print_banner
    info "Collecting phases from: $source_dir"
    echo ""

    # Create collected directory
    mkdir -p "$COLLECTED_DIR"

    # Initialize collection log
    echo "SWARMCARE PHASE COLLECTION LOG" > "$COLLECTION_LOG"
    echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$COLLECTION_LOG"
    echo "Source: $source_dir" >> "$COLLECTION_LOG"
    echo "" >> "$COLLECTION_LOG"

    # Find all package files
    local packages=($(find "$source_dir" -name "*_phases.tar.gz" -type f))

    if [[ ${#packages[@]} -eq 0 ]]; then
        error "No package files found in $source_dir"
    fi

    info "Found ${#packages[@]} package(s)"
    echo ""

    # Track collected phases
    declare -A phase_sources
    local total_files=0
    local total_size=0

    # Process each package
    for package in "${packages[@]}"; do
        local package_name=$(basename "$package")
        local machine_id="${package_name%_phases.tar.gz}"

        progress "Processing: $package_name"
        echo ""

        # Verify checksum if available
        if [[ -f "${package}.sha256" ]]; then
            info "Verifying checksum..."
            local expected=$(cat "${package}.sha256")
            local actual=$(sha256sum "$package" | cut -d' ' -f1)

            if [[ "$expected" != "$actual" ]]; then
                error "Checksum mismatch for $package_name!"
            fi

            success "Checksum verified"
        else
            warn "No checksum file found for $package_name"
        fi

        # Extract to temporary directory
        local temp_dir=$(mktemp -d)
        info "Extracting to temporary location..."

        tar -xzf "$package" -C "$temp_dir"

        # Find all phase directories
        local phase_dirs=($(find "$temp_dir" -name "phase_*" -type d -maxdepth 1))

        info "Found ${#phase_dirs[@]} phase(s) in package"

        # Move each phase to collected directory
        for phase_dir in "${phase_dirs[@]}"; do
            local phase_name=$(basename "$phase_dir")
            local phase_num=$(echo "$phase_name" | sed 's/phase_//' | sed 's/^0*//')
            local target_dir="$COLLECTED_DIR/$phase_name"

            # Check if phase already collected
            if [[ -d "$target_dir" ]]; then
                warn "Phase $phase_name already exists!"
                echo "    Existing source: ${phase_sources[$phase_name]}"
                echo "    New source: $machine_id"
                echo "    Skipping duplicate..."
            else
                mv "$phase_dir" "$target_dir"
                phase_sources[$phase_name]="$machine_id"

                # Count files and size
                local file_count=$(find "$target_dir" -type f | wc -l)
                local size=$(du -sh "$target_dir" | cut -f1)

                success "Collected $phase_name from $machine_id ($file_count files, $size)"
                ((total_files += file_count))
            fi
        done

        # Clean up temp directory
        rm -rf "$temp_dir"

        echo ""
    done

    # Get total size
    if [[ -d "$COLLECTED_DIR" ]]; then
        total_size=$(du -sh "$COLLECTED_DIR" | cut -f1)
    fi

    # Generate collection report
    generate_report

    echo ""
    success "Collection complete!"
    echo ""
    info "Collected Directory: $COLLECTED_DIR"
    info "Total Phases: ${#phase_sources[@]}"
    info "Total Files: $total_files"
    info "Total Size: $total_size"
    echo ""
    info "Next steps:"
    echo "  1. Validate: $0 --validate"
    echo "  2. Integrate: ./INTEGRATE_ALL.sh"
    echo ""
}

# Validate collected phases
cmd_validate() {
    print_banner
    progress "Validating collected phases..."
    echo ""

    if [[ ! -d "$COLLECTED_DIR" ]]; then
        error "No collected phases found. Run: $0 --source <dir>"
    fi

    local expected_phases=29  # phase_00 to phase_28
    local found_phases=0
    local missing_phases=()
    local invalid_phases=()
    local valid_phases=0

    # Check each phase from 0 to 28
    for ((i=0; i<expected_phases; i++)); do
        local phase_name="phase_$(printf "%02d" $i)"
        local phase_dir="$COLLECTED_DIR/$phase_name"

        if [[ ! -d "$phase_dir" ]]; then
            missing_phases+=($i)
            warn "Missing: $phase_name"
        else
            ((found_phases++))

            # Check for MANIFEST.json
            if [[ ! -f "$phase_dir/MANIFEST.json" ]]; then
                invalid_phases+=($i)
                warn "$phase_name: Missing MANIFEST.json"
            else
                # Validate manifest
                local ready=$(jq -r '.ready_for_integration' "$phase_dir/MANIFEST.json" 2>/dev/null || echo "false")

                if [[ "$ready" == "true" ]]; then
                    ((valid_phases++))
                    success "$phase_name: Valid"
                else
                    invalid_phases+=($i)
                    warn "$phase_name: Not ready for integration"
                fi
            fi
        fi
    done

    echo ""
    echo -e "${CYAN}Validation Summary:${NC}"
    echo "  Expected Phases: $expected_phases"
    echo "  Found Phases: $found_phases"
    echo "  Valid Phases: $valid_phases"
    echo "  Missing Phases: ${#missing_phases[@]}"
    echo "  Invalid Phases: ${#invalid_phases[@]}"
    echo ""

    if [[ ${#missing_phases[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Missing Phases:${NC}"
        for phase in "${missing_phases[@]}"; do
            echo "  - Phase $(printf "%02d" $phase)"
        done
        echo ""
    fi

    if [[ ${#invalid_phases[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Invalid Phases:${NC}"
        for phase in "${invalid_phases[@]}"; do
            echo "  - Phase $(printf "%02d" $phase)"
        done
        echo ""
    fi

    if [[ $valid_phases -eq $expected_phases ]]; then
        success "All phases validated successfully!"
        echo ""
        info "Ready for integration: ./INTEGRATE_ALL.sh"
        return 0
    else
        error "Validation failed. Missing or invalid phases detected."
        return 1
    fi
}

# Show collection status
cmd_status() {
    print_banner

    if [[ ! -d "$COLLECTED_DIR" ]]; then
        warn "No collected phases found"
        echo ""
        info "Start collection with: $0 --source <dir>"
        return
    fi

    info "Collected phases in: $COLLECTED_DIR"
    echo ""

    local phase_count=$(find "$COLLECTED_DIR" -name "phase_*" -type d -maxdepth 1 | wc -l)

    if [[ $phase_count -eq 0 ]]; then
        warn "No phases collected yet"
        return
    fi

    echo -e "${CYAN}Collected Phases:${NC}"
    echo ""

    # List all collected phases
    for ((i=0; i<29; i++)); do
        local phase_name="phase_$(printf "%02d" $i)"
        local phase_dir="$COLLECTED_DIR/$phase_name"

        if [[ -d "$phase_dir" ]]; then
            local file_count=$(find "$phase_dir" -type f | wc -l)
            local size=$(du -sh "$phase_dir" | cut -f1)
            local machine_id="unknown"

            if [[ -f "$phase_dir/MANIFEST.json" ]]; then
                machine_id=$(jq -r '.machine_id' "$phase_dir/MANIFEST.json" 2>/dev/null || echo "unknown")
            fi

            echo -e "  ${GREEN}✓${NC} $phase_name (from $machine_id) - $file_count files, $size"
        else
            echo -e "  ${YELLOW}○${NC} $phase_name - Not collected"
        fi
    done

    echo ""
    echo -e "${CYAN}Summary:${NC}"
    echo "  Collected: $phase_count / 29"
    echo "  Progress: $(( phase_count * 100 / 29 ))%"
    echo ""

    if [[ $phase_count -eq 29 ]]; then
        success "All phases collected!"
        echo ""
        info "Next step: ./INTEGRATE_ALL.sh"
    fi
}

# Generate collection report
generate_report() {
    local phase_list=""
    local phase_count=0

    for ((i=0; i<29; i++)); do
        local phase_name="phase_$(printf "%02d" $i)"
        local phase_dir="$COLLECTED_DIR/$phase_name"

        if [[ -d "$phase_dir" ]]; then
            ((phase_count++))

            local machine_id="unknown"
            local file_count=0
            local ready="false"

            if [[ -f "$phase_dir/MANIFEST.json" ]]; then
                machine_id=$(jq -r '.machine_id' "$phase_dir/MANIFEST.json" 2>/dev/null || echo "unknown")
                ready=$(jq -r '.ready_for_integration' "$phase_dir/MANIFEST.json" 2>/dev/null || echo "false")
            fi

            file_count=$(find "$phase_dir" -type f | wc -l)

            if [[ -n "$phase_list" ]]; then
                phase_list="$phase_list,"
            fi

            phase_list="$phase_list
    {
      \"phase_id\": $i,
      \"phase_name\": \"$phase_name\",
      \"machine_id\": \"$machine_id\",
      \"files\": $file_count,
      \"ready_for_integration\": $ready
    }"
        fi
    done

    cat > "$COLLECTION_REPORT" << EOF
{
  "collected_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "total_phases_expected": 29,
  "total_phases_collected": $phase_count,
  "completion_percentage": $(( phase_count * 100 / 29 )),
  "phases": [$phase_list
  ]
}
EOF

    info "Report saved to: $COLLECTION_REPORT"
}

# Usage
usage() {
    echo -e "${YELLOW}Usage:${NC}"
    echo "  $0 <command> [options]"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}--source <dir>${NC}   Collect phases from directory containing packages"
    echo -e "  ${GREEN}--validate${NC}       Validate all collected phases"
    echo -e "  ${GREEN}--status${NC}         Show collection status"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 --source /path/to/packages"
    echo "  $0 --validate"
    echo "  $0 --status"
    echo ""
}

# Main
main() {
    if [[ $# -eq 0 ]]; then
        print_banner
        usage
        exit 0
    fi

    local command="$1"

    case "$command" in
        --source)
            shift
            cmd_collect --source "$@"
            ;;
        --validate)
            cmd_validate
            ;;
        --status)
            cmd_status
            ;;
        --help|-h|help)
            print_banner
            usage
            exit 0
            ;;
        *)
            error "Unknown command: $command\n\nRun '$0 --help' for usage."
            ;;
    esac
}

main "$@"
