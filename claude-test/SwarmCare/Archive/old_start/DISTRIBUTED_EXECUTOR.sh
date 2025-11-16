#!/usr/bin/env bash
#
# SWARMCARE DISTRIBUTED EXECUTOR
# Runs on each development machine to execute assigned phases independently
#
# Usage:
#   ./DISTRIBUTED_EXECUTOR.sh init --machine-id machine_01 --phases "0,1,2"
#   ./DISTRIBUTED_EXECUTOR.sh execute
#   ./DISTRIBUTED_EXECUTOR.sh status
#   ./DISTRIBUTED_EXECUTOR.sh package
#   ./DISTRIBUTED_EXECUTOR.sh validate
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/machine_config.json"
PLAN_FILE="$SCRIPT_DIR/execution_plan.json"
OUTPUT_DIR="$SCRIPT_DIR/output"
PHASES_DIR="$SCRIPT_DIR/phases"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

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
║                 DISTRIBUTED EXECUTOR                              ║
║            SwarmCare Phase Execution System                       ║
║                                                                   ║
║   Execute phases independently on your machine                   ║
║   Package outputs for central integration                        ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Error handler
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Warning message
warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Progress message
progress() {
    echo -e "${MAGENTA}▶ $1${NC}"
}

# Check if config exists
check_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error "Machine not initialized. Run: $0 init --machine-id <id> --phases \"<list>\""
    fi
}

# Initialize machine
cmd_init() {
    local machine_id=""
    local phases=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --machine-id)
                machine_id="$2"
                shift 2
                ;;
            --phases)
                phases="$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    if [[ -z "$machine_id" ]]; then
        error "Missing --machine-id parameter"
    fi

    if [[ -z "$phases" ]]; then
        error "Missing --phases parameter (e.g., \"0,1,2\")"
    fi

    print_banner
    info "Initializing machine: $machine_id"
    info "Assigned phases: $phases"
    echo ""

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Parse phases into array
    IFS=',' read -ra PHASE_ARRAY <<< "$phases"

    # Create machine config
    cat > "$CONFIG_FILE" << EOF
{
  "machine_id": "$machine_id",
  "assigned_phases": [$(echo "$phases" | sed 's/,/, /g')],
  "initialized_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "INITIALIZED",
  "output_directory": "$OUTPUT_DIR"
}
EOF

    # Create execution plan
    local phase_list=""
    for phase in "${PHASE_ARRAY[@]}"; do
        phase=$(echo "$phase" | xargs)  # trim whitespace
        phase_file=$(ls "$PHASES_DIR"/phase_${phase}_*.json 2>/dev/null | head -n 1)

        if [[ -z "$phase_file" ]]; then
            error "Phase $phase definition not found in $PHASES_DIR"
        fi

        if [[ -n "$phase_list" ]]; then
            phase_list="$phase_list,"
        fi

        phase_list="$phase_list
    {
      \"phase_id\": $phase,
      \"phase_file\": \"$phase_file\",
      \"status\": \"PENDING\",
      \"output_dir\": \"$OUTPUT_DIR/phase_$(printf "%02d" $phase)\"
    }"
    done

    cat > "$PLAN_FILE" << EOF
{
  "machine_id": "$machine_id",
  "total_phases": ${#PHASE_ARRAY[@]},
  "phases": [$phase_list
  ],
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

    success "Machine initialized successfully!"
    echo ""
    info "Configuration saved to: $CONFIG_FILE"
    info "Execution plan saved to: $PLAN_FILE"
    echo ""
    info "Next steps:"
    echo "  1. Review execution plan: cat $PLAN_FILE"
    echo "  2. Execute phases: $0 execute"
    echo ""
}

# Execute all assigned phases
cmd_execute() {
    check_config

    if [[ ! -f "$PLAN_FILE" ]]; then
        error "Execution plan not found. Re-run init."
    fi

    print_banner

    local machine_id=$(jq -r '.machine_id' "$CONFIG_FILE")
    local total_phases=$(jq -r '.total_phases' "$PLAN_FILE")

    info "Machine: $machine_id"
    info "Total phases to execute: $total_phases"
    echo ""

    # Get all phases from plan
    local phase_count=$(jq -r '.phases | length' "$PLAN_FILE")

    for ((i=0; i<$phase_count; i++)); do
        local phase_id=$(jq -r ".phases[$i].phase_id" "$PLAN_FILE")
        local phase_file=$(jq -r ".phases[$i].phase_file" "$PLAN_FILE")
        local output_dir=$(jq -r ".phases[$i].output_dir" "$PLAN_FILE")
        local status=$(jq -r ".phases[$i].status" "$PLAN_FILE")

        if [[ "$status" == "COMPLETED" ]]; then
            success "Phase $phase_id already completed, skipping..."
            continue
        fi

        progress "Executing Phase $(printf "%02d" $phase_id)..."
        echo ""

        # Create output directory for this phase
        mkdir -p "$output_dir"
        mkdir -p "$output_dir/backend"
        mkdir -p "$output_dir/frontend"
        mkdir -p "$output_dir/tests"
        mkdir -p "$output_dir/docs"

        # Load phase definition
        local phase_name=$(jq -r '.name' "$phase_file")
        local story_points=$(jq -r '.story_points' "$phase_file")

        info "Phase Name: $phase_name"
        info "Story Points: $story_points"
        info "Output Directory: $output_dir"
        echo ""

        # Find and display the prompt for this phase
        local prompt_file=$(ls "$PROMPTS_DIR"/instance_*_phase_${phase_id}_prompt.md 2>/dev/null | head -n 1)

        if [[ -z "$prompt_file" ]]; then
            warn "No prompt file found for phase $phase_id"
            info "Creating generic prompt from phase definition..."

            # Generate basic prompt from phase definition
            cat > "$output_dir/PHASE_PROMPT.md" << PROMPT_EOF
# Phase $(printf "%02d" $phase_id): $phase_name

## Story Points
$story_points

## Phase Definition
\`\`\`json
$(cat "$phase_file")
\`\`\`

## Instructions
Please implement all user stories defined in this phase according to the specifications.
Generate all necessary code, tests, and documentation.

PROMPT_EOF
        else
            cp "$prompt_file" "$output_dir/PHASE_PROMPT.md"
        fi

        echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}PROMPT FOR PHASE $(printf "%02d" $phase_id)${NC}"
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
        cat "$output_dir/PHASE_PROMPT.md"
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
        echo ""

        warn "MANUAL ACTION REQUIRED:"
        echo "  1. Copy the above prompt to your Claude Code instance"
        echo "  2. Let Claude Code generate all code for this phase"
        echo "  3. Save all generated files to: $output_dir"
        echo "  4. Run tests and validate the phase"
        echo "  5. When complete, press ENTER to continue..."
        echo ""
        read -p "Press ENTER when Phase $phase_id is complete..."

        # Create manifest for this phase
        progress "Creating manifest for phase $phase_id..."

        # Count generated files
        local file_count=$(find "$output_dir" -type f | wc -l)

        # Create manifest
        cat > "$output_dir/MANIFEST.json" << MANIFEST_EOF
{
  "phase_id": $phase_id,
  "phase_name": "$phase_name",
  "machine_id": "$machine_id",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "story_points": $story_points,
  "files_generated": $file_count,
  "output_directory": "$output_dir",
  "validation_status": "PENDING",
  "ready_for_integration": false
}
MANIFEST_EOF

        # Update execution plan
        local tmp_file=$(mktemp)
        jq ".phases[$i].status = \"COMPLETED\" | .phases[$i].completed_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$PLAN_FILE" > "$tmp_file"
        mv "$tmp_file" "$PLAN_FILE"

        success "Phase $phase_id completed!"
        echo ""
    done

    success "All phases executed successfully!"
    echo ""
    info "Next steps:"
    echo "  1. Validate: $0 validate"
    echo "  2. Package for transfer: $0 package"
    echo ""
}

# Show status
cmd_status() {
    check_config

    print_banner

    local machine_id=$(jq -r '.machine_id' "$CONFIG_FILE")

    echo -e "${CYAN}Machine ID: $machine_id${NC}"
    echo ""

    if [[ ! -f "$PLAN_FILE" ]]; then
        warn "No execution plan found"
        return
    fi

    local phase_count=$(jq -r '.phases | length' "$PLAN_FILE")
    local completed=0
    local pending=0

    echo -e "${YELLOW}Phase Status:${NC}"
    echo ""

    for ((i=0; i<$phase_count; i++)); do
        local phase_id=$(jq -r ".phases[$i].phase_id" "$PLAN_FILE")
        local status=$(jq -r ".phases[$i].status" "$PLAN_FILE")

        if [[ "$status" == "COMPLETED" ]]; then
            echo -e "  ${GREEN}✓${NC} Phase $(printf "%02d" $phase_id): COMPLETED"
            ((completed++))
        else
            echo -e "  ${YELLOW}○${NC} Phase $(printf "%02d" $phase_id): PENDING"
            ((pending++))
        fi
    done

    echo ""
    echo -e "${CYAN}Summary:${NC}"
    echo "  Total Phases: $phase_count"
    echo "  Completed: $completed"
    echo "  Pending: $pending"
    echo "  Progress: $(( completed * 100 / phase_count ))%"
    echo ""
}

# Validate phases
cmd_validate() {
    check_config

    print_banner
    progress "Validating all phases..."
    echo ""

    if [[ ! -f "$PLAN_FILE" ]]; then
        error "No execution plan found"
    fi

    local phase_count=$(jq -r '.phases | length' "$PLAN_FILE")
    local all_valid=true

    for ((i=0; i<$phase_count; i++)); do
        local phase_id=$(jq -r ".phases[$i].phase_id" "$PLAN_FILE")
        local output_dir=$(jq -r ".phases[$i].output_dir" "$PLAN_FILE")
        local status=$(jq -r ".phases[$i].status" "$PLAN_FILE")

        if [[ "$status" != "COMPLETED" ]]; then
            warn "Phase $(printf "%02d" $phase_id): Not completed yet"
            all_valid=false
            continue
        fi

        # Check if manifest exists
        if [[ ! -f "$output_dir/MANIFEST.json" ]]; then
            error "Phase $(printf "%02d" $phase_id): Missing MANIFEST.json"
            all_valid=false
            continue
        fi

        # Check if output directory has files
        local file_count=$(find "$output_dir" -type f | wc -l)
        if [[ $file_count -lt 2 ]]; then  # At least MANIFEST.json + 1 other file
            warn "Phase $(printf "%02d" $phase_id): No files generated ($file_count files found)"
            all_valid=false
            continue
        fi

        # Update manifest validation status
        local tmp_file=$(mktemp)
        jq '.validation_status = "VALIDATED" | .ready_for_integration = true | .validated_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' "$output_dir/MANIFEST.json" > "$tmp_file"
        mv "$tmp_file" "$output_dir/MANIFEST.json"

        success "Phase $(printf "%02d" $phase_id): Valid ($file_count files)"
    done

    echo ""

    if [[ "$all_valid" == "true" ]]; then
        success "All phases validated successfully!"
        echo ""
        info "Ready for packaging"
    else
        error "Some phases failed validation. Please review and fix."
    fi
}

# Package for transfer
cmd_package() {
    check_config

    print_banner
    progress "Packaging phases for transfer..."
    echo ""

    # First validate
    cmd_validate

    local machine_id=$(jq -r '.machine_id' "$CONFIG_FILE")
    local package_name="${machine_id}_phases.tar.gz"
    local package_path="$SCRIPT_DIR/$package_name"

    # Create package
    info "Creating package: $package_name"

    cd "$OUTPUT_DIR"
    tar -czf "$package_path" phase_*/
    cd - > /dev/null

    # Get package size
    local size=$(du -h "$package_path" | cut -f1)

    success "Package created successfully!"
    echo ""
    info "Package: $package_path"
    info "Size: $size"
    echo ""
    info "Transfer this file to the integration system:"
    echo "  - USB drive copy"
    echo "  - scp $package_name integration_system:/path/to/collected/"
    echo "  - Cloud upload (Dropbox, Google Drive, etc.)"
    echo ""

    # Create checksum
    local checksum=$(sha256sum "$package_path" | cut -d' ' -f1)
    echo "$checksum" > "${package_path}.sha256"

    info "Checksum: $checksum"
    info "Checksum file: ${package_path}.sha256"
    echo ""

    success "Ready for integration!"
}

# Usage
usage() {
    echo -e "${YELLOW}Usage:${NC}"
    echo "  $0 <command> [options]"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}init${NC}      Initialize machine with assigned phases"
    echo "              --machine-id <id>   Machine identifier (e.g., machine_01)"
    echo "              --phases \"<list>\"   Comma-separated phase numbers (e.g., \"0,1,2\")"
    echo ""
    echo -e "  ${GREEN}execute${NC}   Execute all assigned phases"
    echo ""
    echo -e "  ${GREEN}status${NC}    Show execution status"
    echo ""
    echo -e "  ${GREEN}validate${NC}  Validate all completed phases"
    echo ""
    echo -e "  ${GREEN}package${NC}   Package phases for transfer to integration system"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 init --machine-id machine_01 --phases \"0,1,2\""
    echo "  $0 execute"
    echo "  $0 status"
    echo "  $0 validate"
    echo "  $0 package"
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
    shift

    case "$command" in
        init)
            cmd_init "$@"
            ;;
        execute)
            cmd_execute "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        validate)
            cmd_validate "$@"
            ;;
        package)
            cmd_package "$@"
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
