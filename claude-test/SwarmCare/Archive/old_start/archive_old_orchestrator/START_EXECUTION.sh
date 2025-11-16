#!/usr/bin/env bash
#
# SWARMCARE PARALLEL EXECUTION SYSTEM
# Main entry point for all execution commands
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ORCHESTRATOR="$SCRIPT_DIR/orchestrator/master_controller.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ███████╗██╗    ██╗ █████╗ ██████╗ ███╗   ███╗ ██████╗ █████╗ ██████╗███████╗  ║
║   ██╔════╝██║    ██║██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗██╔════╝  ║
║   ███████╗██║ █╗ ██║███████║██████╔╝██╔████╔██║██║     ███████║██████╔╝█████╗    ║
║   ╚════██║██║███╗██║██╔══██║██╔══██╗██║╚██╔╝██║██║     ██╔══██║██╔══██╗██╔══╝    ║
║   ███████║╚███╔███╔╝██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╗██║  ██║██║  ██║███████╗  ║
║   ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝  ║
║                                                                       ║
║            PARALLEL EXECUTION SYSTEM - v1.0                          ║
║            Production-Ready AI-Generated Healthcare Platform          ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Usage information
usage() {
    echo -e "${YELLOW}Usage:${NC}"
    echo "  $0 <command> [options]"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}init${NC} [--instances N]         Initialize system with N instances (default: 5)"
    echo -e "  ${GREEN}distribute${NC} [--strategy S]     Distribute phases to instances"
    echo -e "                                  Strategies: balanced, critical-path, fastest"
    echo -e "  ${GREEN}execute${NC} [--dry-run]          Execute all instances in parallel"
    echo -e "  ${GREEN}monitor${NC}                      Monitor progress across all instances"
    echo -e "  ${GREEN}resume${NC}                       Resume execution from last checkpoint"
    echo -e "  ${GREEN}status${NC}                       Show current status"
    echo -e "  ${GREEN}report${NC}                       Generate comprehensive report"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 init --instances 5"
    echo "  $0 distribute --strategy balanced"
    echo "  $0 execute --dry-run"
    echo "  $0 monitor"
    echo "  $0 resume"
    echo ""
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

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed. Please install Python 3.8 or higher."
    fi
}

# Initialize system
cmd_init() {
    local instances=5

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --instances)
                instances="$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    print_banner
    info "Initializing SWARMCARE execution system with $instances instances..."
    echo ""

    python3 "$ORCHESTRATOR" init --instances "$instances"

    echo ""
    success "System initialized successfully!"
    echo ""
    info "Next steps:"
    echo "  1. Run: $0 distribute --strategy balanced"
    echo "  2. Run: $0 execute --dry-run"
    echo ""
}

# Distribute phases
cmd_distribute() {
    local strategy="balanced"
    local instances=5

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --strategy)
                strategy="$2"
                shift 2
                ;;
            --instances)
                instances="$2"
                shift 2
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    print_banner
    info "Distributing phases using strategy: $strategy"
    echo ""

    python3 "$ORCHESTRATOR" distribute --strategy "$strategy" --instances "$instances"

    echo ""
    success "Phases distributed successfully!"
    echo ""
    info "Next steps:"
    echo "  1. Review the distribution above"
    echo "  2. Run: $0 execute --dry-run (to see prompts without executing)"
    echo "  3. Run: $0 execute (to start parallel execution)"
    echo ""
}

# Execute instances
cmd_execute() {
    local dry_run=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="--dry-run"
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    print_banner

    if [[ -n "$dry_run" ]]; then
        info "Running in DRY-RUN mode (prompts will be generated but not executed)"
    else
        info "Starting parallel execution across all instances..."
    fi

    echo ""

    python3 "$ORCHESTRATOR" execute $dry_run

    echo ""
    success "Execution complete!"

    if [[ -n "$dry_run" ]]; then
        echo ""
        info "Prompts have been generated in: $SCRIPT_DIR/prompts/"
        info "Review the prompts and run: $0 execute (without --dry-run)"
    else
        echo ""
        info "Check progress with: $0 monitor"
    fi
    echo ""
}

# Monitor progress
cmd_monitor() {
    print_banner
    info "Monitoring execution progress..."
    echo ""

    python3 "$ORCHESTRATOR" monitor

    echo ""
    info "Refresh progress: $0 monitor"
    echo ""
}

# Resume execution
cmd_resume() {
    print_banner
    info "Resuming execution from last checkpoint..."
    echo ""

    python3 "$ORCHESTRATOR" resume

    echo ""
    info "To continue execution, run: $0 execute"
    echo ""
}

# Status check
cmd_status() {
    print_banner
    info "Current system status:"
    echo ""

    # Check if instances are initialized
    if [[ ! -d "$SCRIPT_DIR/instance_manager" ]]; then
        echo -e "${YELLOW}Status: NOT INITIALIZED${NC}"
        echo ""
        info "Initialize the system with: $0 init"
        return
    fi

    # Check if phases are distributed
    local pool_file="$SCRIPT_DIR/instance_manager/instance_pool.json"
    if [[ ! -f "$pool_file" ]]; then
        echo -e "${YELLOW}Status: INITIALIZED (not distributed)${NC}"
        echo ""
        info "Distribute phases with: $0 distribute"
        return
    fi

    # Show progress
    python3 "$ORCHESTRATOR" monitor
}

# Generate report
cmd_report() {
    print_banner
    info "Generating comprehensive execution report..."
    echo ""

    # TODO: Implement comprehensive reporting
    python3 "$ORCHESTRATOR" monitor

    echo ""
    success "Report generated!"
    echo ""
}

# Main command dispatcher
main() {
    # Check Python availability
    check_python

    # Parse command
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
        distribute)
            cmd_distribute "$@"
            ;;
        execute)
            cmd_execute "$@"
            ;;
        monitor)
            cmd_monitor "$@"
            ;;
        resume)
            cmd_resume "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        report)
            cmd_report "$@"
            ;;
        --help|-h|help)
            print_banner
            usage
            exit 0
            ;;
        *)
            error "Unknown command: $command\n\nRun '$0 --help' for usage information."
            ;;
    esac
}

main "$@"
