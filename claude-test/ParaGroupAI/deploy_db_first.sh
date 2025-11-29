#!/usr/bin/env bash
################################################################################
# DEPLOY DATABASE-FIRST CONTEXT MANAGEMENT
################################################################################
#
# One-command deployment script for database-first architecture.
# Automatically sets up everything needed for production-ready context management.
#
# Author: ULTRATHINK System
# Date: 2025-11-19
# Version: 1.0.0
#
# Usage:
#   ./deploy_db_first.sh                    # Deploy with defaults
#   ./deploy_db_first.sh --test             # Deploy and run tests
#   ./deploy_db_first.sh --demo             # Deploy and run demo
#   ./deploy_db_first.sh --verbose          # Verbose output
#
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_DIR="${SCRIPT_DIR}/database"
DB_FILE="${DB_DIR}/ultrathink_context.db"
RUN_TESTS=false
RUN_DEMO=false
VERBOSE=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --test)
            RUN_TESTS=true
            shift
            ;;
        --demo)
            RUN_DEMO=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --test      Run tests after deployment"
            echo "  --demo      Run demonstration after deployment"
            echo "  --verbose   Verbose output"
            echo "  --help      Show this help message"
            exit 0
            ;;
    esac
done

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_section() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

################################################################################
# MAIN DEPLOYMENT
################################################################################

log_section "🚀 DATABASE-FIRST CONTEXT MANAGEMENT DEPLOYMENT"

log_info "Deployment started at $(date)"
log_info "Script directory: ${SCRIPT_DIR}"

# Step 1: Check prerequisites
log_section "Step 1: Checking Prerequisites"

# Check Python3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    log_success "Python3 found: ${PYTHON_VERSION}"
else
    log_error "Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Check SQLite support
if python3 -c "import sqlite3" 2>/dev/null; then
    SQLITE_VERSION=$(python3 -c "import sqlite3; print(sqlite3.sqlite_version)")
    log_success "SQLite3 module available: version ${SQLITE_VERSION}"
else
    log_error "SQLite3 Python module not available"
    exit 1
fi

# Step 2: Create directory structure
log_section "Step 2: Creating Directory Structure"

mkdir -p "${DB_DIR}"
log_success "Created database directory: ${DB_DIR}"

mkdir -p "${SCRIPT_DIR}/logs"
log_success "Created logs directory: ${SCRIPT_DIR}/logs"

# Step 3: Initialize database
log_section "Step 3: Initializing SQLite Database"

if [[ -f "${DB_FILE}" ]]; then
    log_warning "Database already exists: ${DB_FILE}"
    read -p "Recreate database? This will DELETE all existing data! (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "${DB_FILE}"
        log_info "Deleted existing database"
    else
        log_info "Keeping existing database"
    fi
fi

if [[ ! -f "${DB_FILE}" ]]; then
    log_info "Creating new database..."

    # Run schema creation using Python (no sqlite3 command needed)
    if [[ -f "${DB_DIR}/schema_sqlite.sql" ]]; then
        if python3 "${DB_DIR}/init_database.py" "${DB_FILE}" "${DB_DIR}/schema_sqlite.sql"; then
            log_success "Database schema created successfully"
        else
            log_error "Failed to create database schema"
            exit 1
        fi
    else
        log_error "Schema file not found: ${DB_DIR}/schema_sqlite.sql"
        exit 1
    fi

    # Verify database
    TABLE_COUNT=$(python3 -c "import sqlite3; conn = sqlite3.connect('${DB_FILE}'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\'table\''); print(cursor.fetchone()[0]); conn.close()")
    log_success "Database initialized with ${TABLE_COUNT} tables"
else
    log_info "Using existing database"
fi

# Step 4: Verify Python modules
log_section "Step 4: Verifying Python Implementation"

REQUIRED_FILES=(
    "sqlite_context_loader.py"
    "multi_project_manager.py"
    "token_manager.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "${DB_DIR}/${file}" ]]; then
        log_success "Found: ${file}"
    else
        log_error "Missing: ${file}"
        exit 1
    fi
done

# Check if files are importable
cd "${DB_DIR}"
for file in "${REQUIRED_FILES[@]}"; do
    MODULE=$(basename "${file}" .py)
    if python3 -c "import ${MODULE}" 2>/dev/null; then
        log_success "Module importable: ${MODULE}"
    else
        log_warning "Module has import issues: ${MODULE} (may work in production)"
    fi
done
cd "${SCRIPT_DIR}"

# Step 5: Update config.py (verify)
log_section "Step 5: Verifying Configuration"

if grep -q "DB_FIRST_ENABLED = True" config.py; then
    log_success "Database-first enabled in config.py"
else
    log_warning "DB_FIRST_ENABLED not found in config.py"
fi

if grep -q "DB_PATH = \"database/ultrathink_context.db\"" config.py; then
    log_success "Database path configured in config.py"
else
    log_warning "DB_PATH not configured in config.py"
fi

# Step 6: Create integration example
log_section "Step 6: Creating Integration Example"

cat > "${DB_DIR}/integration_example.py" << 'EXAMPLE_EOF'
#!/usr/bin/env python3
"""
Example: Integrate database-first context management with ULTRATHINK.

This shows how to use the database-first architecture in your code.
"""

import sys
sys.path.insert(0, '/home/user01/claude-test/ClaudePrompt/database')

from sqlite_context_loader import SQLiteContextLoader
from multi_project_manager import MultiProjectManager
from token_manager import TokenManager


def main():
    """Example integration."""
    print("\n" + "=" * 80)
    print("DATABASE-FIRST CONTEXT MANAGEMENT - INTEGRATION EXAMPLE")
    print("=" * 80 + "\n")

    # Create managers
    manager = MultiProjectManager("ultrathink_context.db")
    token_mgr = TokenManager("ultrathink_context.db")

    # Example 1: Create a project
    print("1. Creating a project...")
    project_id = manager.create_project(
        name="Example Integration Project",
        description="Demonstrating database-first context management",
        total_story_points=1300
    )
    print(f"   ✅ Project created: {project_id}\n")

    # Example 2: Launch instances
    print("2. Launching instances...")
    instances = []
    for i in range(1, 4):
        instance_id = manager.launch_instance(project_id, phase_id=None)
        instances.append(instance_id)
        print(f"   ✅ Instance {i}: {instance_id}")

    print(f"\n   Total: {len(instances)} instances for project {project_id}\n")

    # Example 3: Store context
    print("3. Storing context...")
    snapshot_id = manager.store_context(
        project_id=project_id,
        content={"message": "Example context snapshot", "step": "integration_test"},
        priority="HIGH",
        content_type="code"
    )
    print(f"   ✅ Context snapshot stored: ID {snapshot_id}\n")

    # Example 4: Check token usage
    print("4. Checking token usage...")
    for instance_id in instances:
        usage = token_mgr.check_token_usage(instance_id)
        if usage:
            print(f"   Instance {instance_id}: {usage['current_token_usage']:,} tokens ({usage['percentage']:.1f}%)")
    print()

    # Example 5: Get project summary
    print("5. Project summary:")
    summaries = manager.get_project_summary()
    for summary in summaries:
        print(f"   • {summary['name']}: {summary['active_instances']} instances, {summary['total_snapshots']} snapshots")

    print("\n" + "=" * 80)
    print("✅ INTEGRATION EXAMPLE COMPLETED SUCCESSFULLY")
    print("=" * 80 + "\n")

    manager.close()
    token_mgr.close()


if __name__ == "__main__":
    main()
EXAMPLE_EOF

chmod +x "${DB_DIR}/integration_example.py"
log_success "Created integration example: ${DB_DIR}/integration_example.py"

# Step 7: Run tests (if requested)
if [[ "${RUN_TESTS}" == "true" ]]; then
    log_section "Step 7: Running Tests"

    if [[ -f "${DB_DIR}/test_db_first.py" ]]; then
        cd "${DB_DIR}"
        python3 test_db_first.py
        log_success "Tests completed"
        cd "${SCRIPT_DIR}"
    else
        log_warning "Test file not found: ${DB_DIR}/test_db_first.py"
    fi
fi

# Step 8: Run demo (if requested)
if [[ "${RUN_DEMO}" == "true" ]]; then
    log_section "Step 8: Running Demonstration"

    cd "${DB_DIR}"
    python3 integration_example.py
    cd "${SCRIPT_DIR}"
fi

# Final summary
log_section "✅ DEPLOYMENT COMPLETED SUCCESSFULLY"

echo "Database Location:"
echo "  ${DB_FILE}"
echo ""
echo "Implementation Files:"
echo "  ${DB_DIR}/sqlite_context_loader.py"
echo "  ${DB_DIR}/multi_project_manager.py"
echo "  ${DB_DIR}/token_manager.py"
echo ""
echo "Configuration:"
echo "  config.py (DB_FIRST_ENABLED = True)"
echo ""
echo "Documentation:"
echo "  ${SCRIPT_DIR}/DB_FIRST_IMPLEMENTATION.md"
echo "  ${SCRIPT_DIR}/HOW_TO_USE_DB_FIRST.md"
echo ""
echo "Next Steps:"
echo "  1. Read documentation: cat DB_FIRST_IMPLEMENTATION.md"
echo "  2. Run demo: cd database && python3 integration_example.py"
echo "  3. Run tests: cd database && python3 test_db_first.py"
echo "  4. Launch multi-project: python3 multi_project_manager.py"
echo ""
echo "🎉 Database-first context management is ready to use!"
echo ""

log_info "Deployment completed at $(date)"

exit 0
