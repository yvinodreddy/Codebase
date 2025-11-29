#!/bin/bash
################################################################################
# ULTRATHINK 10-Track Master Execution Launcher
# Production-ready parallel execution system with real-time tracking
#
# ZERO BREAKING CHANGES:
# - New file in root directory
# - Does not modify existing code or files
# - All new components in separate directories (realtime-tracking/, tracks/, web-dashboard/)
# - Optional feature - existing system continues to work without this
################################################################################

set -e

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
WEB_PORT=8000
LOG_DIR="logs"
DB_PATH="realtime-tracking/track_state.db"

# Print banner
print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "================================================================================"
    echo "                ULTRATHINK 10-TRACK MASTER EXECUTION LAUNCHER"
    echo "                   Real-Time Parallel Execution System"
    echo "================================================================================"
    echo -e "${NC}"
}

# Print step header
print_step() {
    local step=$1
    local message=$2
    echo -e "${BLUE}${BOLD}[$step]${NC} ${message}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check dependencies
check_dependencies() {
    print_step "1/9" "Checking dependencies..."

    local missing_deps=()

    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi

    # Check SQLite (Python module is sufficient - command-line tool not required)
    if ! python3 -c "import sqlite3" 2>/dev/null; then
        missing_deps+=("python3-sqlite3")
    fi

    # Check pip packages
    if ! python3 -c "import fastapi" 2>/dev/null; then
        print_warning "FastAPI not installed"
        echo "Installing FastAPI and dependencies..."
        pip3 install fastapi uvicorn --quiet
    fi

    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        echo "Please install missing dependencies and try again"
        exit 1
    fi

    print_success "All dependencies satisfied"
}

# Setup directories
setup_directories() {
    print_step "2/9" "Setting up directory structure..."

    mkdir -p "$LOG_DIR"
    mkdir -p tracks
    mkdir -p realtime-tracking
    mkdir -p web-dashboard
    mkdir -p tmp

    print_success "Directory structure created"
}

# Initialize database
initialize_database() {
    print_step "3/9" "Initializing SQLite database..."

    if [ ! -f "$DB_PATH" ]; then
        python3 realtime-tracking/setup_database.py
        print_success "Database initialized"
    else
        print_warning "Database already exists, skipping initialization"
        echo "To recreate database, delete: $DB_PATH"
    fi
}

# Start WebSocket server
start_websocket_server() {
    print_step "4/9" "Starting WebSocket server..."

    # Check if server is already running
    if lsof -ti:$WEB_PORT > /dev/null 2>&1; then
        print_warning "Port $WEB_PORT already in use"
        echo "Kill existing process? (y/n)"
        read -r response
        if [ "$response" = "y" ]; then
            kill $(lsof -ti:$WEB_PORT) 2>/dev/null || true
            sleep 2
        else
            print_error "Cannot start server, port $WEB_PORT is in use"
            exit 1
        fi
    fi

    # Start server in background
    nohup python3 realtime-tracking/websocket_server.py > logs/websocket_server.log 2>&1 &
    WEB_SERVER_PID=$!
    echo $WEB_SERVER_PID > tmp/websocket_server.pid

    # Wait for server to start
    echo -n "Waiting for server to start"
    for i in {1..10}; do
        if curl -s http://localhost:$WEB_PORT/health > /dev/null 2>&1; then
            echo ""
            print_success "WebSocket server started (PID: $WEB_SERVER_PID)"
            return 0
        fi
        echo -n "."
        sleep 1
    done

    echo ""
    print_error "WebSocket server failed to start"
    exit 1
}

# Verify track scripts
verify_track_scripts() {
    print_step "5/9" "Verifying track execution scripts..."

    for i in {1..10}; do
        if [ ! -f "tracks/track${i}.sh" ]; then
            print_error "Missing track script: tracks/track${i}.sh"
            exit 1
        fi

        if [ ! -x "tracks/track${i}.sh" ]; then
            chmod +x "tracks/track${i}.sh"
        fi
    done

    print_success "All 10 track scripts verified"
}

# Launch parallel tracks
launch_tracks() {
    print_step "6/9" "Launching 10 parallel tracks..."

    echo ""
    echo -e "${CYAN}Starting track execution in parallel...${NC}"
    echo ""

    declare -a TRACK_PIDS

    for i in {1..10}; do
        ./tracks/track${i}.sh > "$LOG_DIR/track${i}.log" 2>&1 &
        TRACK_PIDS[$i]=$!
        echo -e "${GREEN}✓${NC} Track $i started (PID: ${TRACK_PIDS[$i]})"
        sleep 0.5  # Stagger starts slightly
    done

    # Save PIDs to file
    printf "%s\n" "${TRACK_PIDS[@]}" > tmp/track_pids.txt

    echo ""
    print_success "All 10 tracks launched successfully"
    echo ""
}

# Display access information
display_access_info() {
    print_step "7/9" "System ready!"

    echo ""
    echo -e "${CYAN}${BOLD}================================================================================"
    echo "                            ACCESS INFORMATION"
    echo "================================================================================${NC}"
    echo ""
    echo -e "${BOLD}Web Dashboard:${NC}     http://localhost:$WEB_PORT"
    echo -e "${BOLD}WebSocket API:${NC}     ws://localhost:$WEB_PORT/ws"
    echo -e "${BOLD}REST API:${NC}          http://localhost:$WEB_PORT/api/tracks"
    echo -e "${BOLD}API Documentation:${NC} http://localhost:$WEB_PORT/docs"
    echo -e "${BOLD}Health Check:${NC}      http://localhost:$WEB_PORT/health"
    echo ""
    echo -e "${BOLD}Log Files:${NC}         $LOG_DIR/track*.log"
    echo -e "${BOLD}Database:${NC}          $DB_PATH"
    echo -e "${BOLD}Server Log:${NC}        logs/websocket_server.log"
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
}

# Open browser
open_browser() {
    print_step "8/9" "Opening web dashboard..."

    sleep 3  # Give server time to fully initialize

    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:$WEB_PORT" 2>/dev/null &
        print_success "Dashboard opened in browser"
    elif command -v open &> /dev/null; then
        open "http://localhost:$WEB_PORT" &
        print_success "Dashboard opened in browser"
    else
        print_warning "Could not auto-open browser"
        echo "Please manually open: http://localhost:$WEB_PORT"
    fi

    echo ""
}

# Monitor execution
monitor_execution() {
    print_step "9/9" "Monitoring track execution..."

    echo ""
    echo -e "${CYAN}${BOLD}================================================================================"
    echo "                         REAL-TIME MONITORING ACTIVE"
    echo "================================================================================${NC}"
    echo ""
    echo -e "View live progress at: ${BOLD}http://localhost:$WEB_PORT${NC}"
    echo ""
    echo "Press Ctrl+C to view shutdown menu"
    echo ""

    # Read PIDs from file
    mapfile -t TRACK_PIDS < tmp/track_pids.txt

    # Monitor tracks
    while true; do
        sleep 5

        # Check if all tracks completed
        local all_completed=true
        for pid in "${TRACK_PIDS[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then
                all_completed=false
                break
            fi
        done

        if [ "$all_completed" = true ]; then
            echo ""
            echo -e "${GREEN}${BOLD}================================================================================"
            echo "                       ALL TRACKS COMPLETED!"
            echo "================================================================================${NC}"
            echo ""
            show_completion_summary
            break
        fi
    done
}

# Show completion summary
show_completion_summary() {
    echo "Fetching completion statistics..."
    echo ""

    # Query database for statistics
    local stats=$(sqlite3 "$DB_PATH" << EOF
.mode list
.separator "|"
SELECT
    SUM(CASE WHEN status='COMPLETED' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) as failed,
    ROUND(AVG(progress), 1) as avg_progress
FROM tracks;
EOF
)

    IFS='|' read -r completed failed avg_progress <<< "$stats"

    echo -e "${BOLD}Execution Summary:${NC}"
    echo -e "  ✅ Completed: ${GREEN}$completed${NC}/10"
    echo -e "  ❌ Failed:    ${RED}$failed${NC}/10"
    echo -e "  📊 Progress:  ${CYAN}$avg_progress%${NC}"
    echo ""

    echo "View detailed results at: http://localhost:$WEB_PORT"
    echo ""
    echo "Keep server running? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        cleanup
    else
        echo ""
        echo "Server is still running. Press Ctrl+C to stop."
        wait
    fi
}

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"

    # Stop WebSocket server
    if [ -f tmp/websocket_server.pid ]; then
        local pid=$(cat tmp/websocket_server.pid)
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
            echo "✓ WebSocket server stopped"
        fi
        rm -f tmp/websocket_server.pid
    fi

    # Stop any remaining tracks
    if [ -f tmp/track_pids.txt ]; then
        while read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
            fi
        done < tmp/track_pids.txt
        rm -f tmp/track_pids.txt
        echo "✓ All tracks stopped"
    fi

    echo ""
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Trap Ctrl+C
trap cleanup EXIT INT TERM

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    print_banner

    check_dependencies
    setup_directories
    initialize_database
    start_websocket_server
    verify_track_scripts
    launch_tracks
    display_access_info
    open_browser
    monitor_execution
}

# Run main function
main
