#!/usr/bin/env bash
#
# ClaudePrompt/ULTRATHINK Framework - System Discovery Script
#
# This script collects comprehensive system configuration information
# to enable tailored deployment of the ClaudePrompt project.
#
# Usage: bash system_discovery.sh > system_config.txt
#
# Run this on your NEW system to gather configuration data.
#

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Print section header
print_section() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

# Print info line
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1: $2"
}

# Print success line
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Print warning line
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# ============================================================================
# SYSTEM DISCOVERY STARTS HERE
# ============================================================================

print_section "CLAUDEPROMPT SYSTEM DISCOVERY REPORT"
echo "Generated: $(date)"
echo "Purpose: Gather system configuration for ClaudePrompt deployment"
echo ""

# ============================================================================
# 1. OPERATING SYSTEM INFORMATION
# ============================================================================

print_section "1. OPERATING SYSTEM INFORMATION"

print_info "OS Type" "$(uname -s)"
print_info "OS Version" "$(uname -r)"
print_info "Architecture" "$(uname -m)"
print_info "Hostname" "$(hostname)"

if [ -f /etc/os-release ]; then
    echo ""
    echo "Distribution Details:"
    cat /etc/os-release
fi

if command -v lsb_release &>/dev/null; then
    echo ""
    echo "LSB Release Info:"
    lsb_release -a 2>/dev/null || true
fi

# Check if running in VM
echo ""
if command -v systemd-detect-virt &>/dev/null; then
    VIRT_TYPE=$(systemd-detect-virt)
    if [ "$VIRT_TYPE" != "none" ]; then
        print_info "Virtualization" "$VIRT_TYPE"
    else
        print_info "Virtualization" "Not detected (bare metal)"
    fi
fi

# Check for UTM specifically
if grep -qi "utm" /proc/cpuinfo 2>/dev/null || grep -qi "qemu" /proc/cpuinfo 2>/dev/null; then
    print_warning "UTM/QEMU virtualization detected"
fi

# ============================================================================
# 2. USER AND HOME DIRECTORY
# ============================================================================

print_section "2. USER AND HOME DIRECTORY INFORMATION"

print_info "Current User" "$USER"
print_info "Home Directory" "$HOME"
print_info "Working Directory" "$PWD"
print_info "User ID" "$(id -u)"
print_info "Group ID" "$(id -g)"
print_info "All Groups" "$(groups)"

echo ""
echo "Home Directory Permissions:"
ls -la "$HOME" | head -n 1

echo ""
echo "Disk Space - Home Directory:"
df -h "$HOME"

# ============================================================================
# 3. SHELL CONFIGURATION
# ============================================================================

print_section "3. SHELL CONFIGURATION"

print_info "Current Shell" "$SHELL"
print_info "Bash Version" "$BASH_VERSION"

echo ""
echo "Shell Configuration Files:"
for file in ~/.bashrc ~/.bash_profile ~/.profile ~/.zshrc; do
    if [ -f "$file" ]; then
        print_success "Found: $file ($(wc -l < "$file") lines)"
    fi
done

echo ""
echo "Current Aliases:"
alias 2>/dev/null || echo "No aliases defined"

echo ""
echo "Current Environment Variables (filtered):"
env | grep -E "^(PATH|HOME|USER|SHELL|LANG|LC_|CLAUDE|ANTHROPIC|PYTHON)" | sort

# ============================================================================
# 4. PYTHON INSTALLATION
# ============================================================================

print_section "4. PYTHON INSTALLATION"

if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    print_success "Python3 installed: $PY_VERSION"
    print_info "Python3 Path" "$(which python3)"

    # Python version details
    echo ""
    python3 -c "import sys; print(f'Python Executable: {sys.executable}')"
    python3 -c "import sys; print(f'Python Version: {sys.version}')"
    python3 -c "import sys; print(f'Platform: {sys.platform}')"
else
    print_warning "Python3 NOT installed"
fi

if command -v pip3 &>/dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1)
    print_success "pip3 installed: $PIP_VERSION"
    print_info "pip3 Path" "$(which pip3)"
else
    print_warning "pip3 NOT installed"
fi

if command -v python3 &>/dev/null; then
    echo ""
    echo "Python User Site Packages:"
    python3 -m site
fi

# ============================================================================
# 5. INSTALLED PYTHON PACKAGES
# ============================================================================

print_section "5. INSTALLED PYTHON PACKAGES"

if command -v pip3 &>/dev/null; then
    echo "Installed Packages (pip list):"
    echo ""
    pip3 list 2>/dev/null || echo "Unable to list packages"

    echo ""
    echo "Checking Critical Packages:"
    for pkg in anthropic requests pyyaml pytest python-dotenv; do
        if pip3 list 2>/dev/null | grep -i "^$pkg " &>/dev/null; then
            VERSION=$(pip3 list 2>/dev/null | grep -i "^$pkg " | awk '{print $2}')
            print_success "$pkg version $VERSION"
        else
            print_warning "$pkg NOT installed"
        fi
    done
else
    print_warning "Cannot check Python packages - pip3 not installed"
fi

# ============================================================================
# 6. CLAUDE CODE INSTALLATION
# ============================================================================

print_section "6. CLAUDE CODE INSTALLATION"

if command -v claude &>/dev/null; then
    print_success "Claude Code installed"
    print_info "Claude Path" "$(which claude)"

    echo ""
    echo "Claude Version:"
    claude --version 2>&1 || true

    echo ""
    echo "Claude Help (first 30 lines):"
    claude --help 2>&1 | head -n 30 || true
else
    print_warning "Claude Code NOT installed"
    echo ""
    echo "To install Claude Code, visit: https://claude.ai/code"
fi

# Check for API key (should NOT be set)
echo ""
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    print_success "ANTHROPIC_API_KEY not set (correct - we use Claude Code, not API)"
else
    print_warning "ANTHROPIC_API_KEY is set (should be removed - we use Claude Code only)"
fi

# ============================================================================
# 7. EXISTING ULTRATHINK INSTALLATIONS
# ============================================================================

print_section "7. EXISTING ULTRATHINK/CLAUDEPROMPT INSTALLATIONS"

# Check common locations
SEARCH_DIRS=(
    "$HOME/claude-test"
    "$HOME/ClaudePrompt"
    "$HOME/TestPrompt"
    "$HOME/ULTRATHINK"
    "/usr/local/claude-test"
    "/opt/claude-test"
)

echo "Searching for existing installations:"
for dir in "${SEARCH_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_warning "Found existing directory: $dir"
        echo "  Contents:"
        ls -la "$dir" 2>/dev/null | head -n 10
    fi
done

# Check for existing CLAUDE.md files
echo ""
echo "Searching for existing CLAUDE.md files:"
find "$HOME" -name "CLAUDE.md" -type f 2>/dev/null | while read -r file; do
    print_warning "Found: $file"
done

# Check for existing ultrathink commands
echo ""
echo "Checking for existing ULTRATHINK commands:"
for cmd in ultrathinkc uc cpp cpps; do
    if command -v $cmd &>/dev/null; then
        print_warning "Command '$cmd' exists at: $(which $cmd)"
    fi
done

# ============================================================================
# 8. SYSTEM RESOURCES
# ============================================================================

print_section "8. SYSTEM RESOURCES"

echo "Memory Information:"
free -h 2>/dev/null || vm_stat 2>/dev/null || echo "Memory info not available"

echo ""
echo "CPU Information:"
if [ -f /proc/cpuinfo ]; then
    CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -n 1 | cut -d: -f2 | xargs)
    CPU_CORES=$(grep -c "processor" /proc/cpuinfo)
    print_info "CPU Model" "$CPU_MODEL"
    print_info "CPU Cores" "$CPU_CORES"
else
    sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "CPU info not available"
fi

echo ""
echo "Disk Space - All Mounted Filesystems:"
df -h

# ============================================================================
# 9. NETWORK CONFIGURATION
# ============================================================================

print_section "9. NETWORK CONFIGURATION"

print_info "Hostname" "$(hostname)"

echo ""
echo "Network Interfaces:"
if command -v ip &>/dev/null; then
    ip addr show 2>/dev/null | grep -E "^[0-9]+:|inet " || true
else
    ifconfig 2>/dev/null | grep -E "^[a-z]+|inet " || true
fi

echo ""
echo "DNS Configuration:"
if [ -f /etc/resolv.conf ]; then
    cat /etc/resolv.conf | grep -v "^#" | grep -v "^$"
fi

echo ""
echo "Internet Connectivity Test:"
if ping -c 1 8.8.8.8 &>/dev/null; then
    print_success "Internet connectivity: OK"
else
    print_warning "Internet connectivity: FAILED"
fi

# ============================================================================
# 10. FILE SYSTEM PERMISSIONS
# ============================================================================

print_section "10. FILE SYSTEM PERMISSIONS"

echo "Checking write permissions for key directories:"
for dir in "$HOME" "$HOME/bin" "/tmp" "/usr/local" "/opt"; do
    if [ -d "$dir" ]; then
        if [ -w "$dir" ]; then
            print_success "Writable: $dir"
        else
            print_warning "Not writable: $dir"
        fi
    else
        echo "  Directory does not exist: $dir"
    fi
done

echo ""
echo "umask setting:"
print_info "Current umask" "$(umask)"

# ============================================================================
# 11. DEVELOPMENT TOOLS
# ============================================================================

print_section "11. DEVELOPMENT TOOLS"

# Check for common development tools
TOOLS=(git curl wget unzip tar gzip make gcc)

for tool in "${TOOLS[@]}"; do
    if command -v $tool &>/dev/null; then
        VERSION=$($tool --version 2>&1 | head -n 1 || echo "version unknown")
        print_success "$tool: $VERSION"
    else
        print_warning "$tool: NOT installed"
    fi
done

# ============================================================================
# 12. PACKAGE MANAGERS
# ============================================================================

print_section "12. PACKAGE MANAGERS"

if command -v apt &>/dev/null; then
    print_success "APT (Debian/Ubuntu) package manager available"
    print_info "APT Version" "$(apt --version 2>&1 | head -n 1)"
fi

if command -v brew &>/dev/null; then
    print_success "Homebrew package manager available"
    print_info "Brew Version" "$(brew --version 2>&1 | head -n 1)"
fi

if command -v yum &>/dev/null; then
    print_success "YUM (RedHat/CentOS) package manager available"
fi

if command -v snap &>/dev/null; then
    print_success "Snap package manager available"
fi

# ============================================================================
# 13. PATH CONFIGURATION
# ============================================================================

print_section "13. PATH CONFIGURATION"

echo "Current PATH:"
echo "$PATH" | tr ':' '\n' | nl

echo ""
echo "Executable Directories in PATH:"
echo "$PATH" | tr ':' '\n' | while read -r dir; do
    if [ -d "$dir" ] && [ -x "$dir" ]; then
        COUNT=$(find "$dir" -maxdepth 1 -type f -executable 2>/dev/null | wc -l)
        echo "  $dir ($COUNT executables)"
    fi
done

# ============================================================================
# 14. SECURITY AND PERMISSIONS SETTINGS
# ============================================================================

print_section "14. SECURITY AND PERMISSIONS SETTINGS"

echo "User Security Context:"
id

echo ""
echo "Sudo Access:"
if sudo -n true 2>/dev/null; then
    print_success "Sudo access available (passwordless)"
elif sudo -v 2>/dev/null; then
    print_success "Sudo access available (requires password)"
else
    print_warning "No sudo access"
fi

echo ""
echo "SELinux Status:"
if command -v getenforce &>/dev/null; then
    SELINUX_STATUS=$(getenforce 2>/dev/null)
    print_info "SELinux" "$SELINUX_STATUS"
else
    echo "  SELinux not installed"
fi

# ============================================================================
# 15. TIMEZONE AND LOCALE
# ============================================================================

print_section "15. TIMEZONE AND LOCALE"

print_info "Timezone" "$(date +%Z)"
print_info "Current Time" "$(date)"

echo ""
echo "Locale Settings:"
locale 2>/dev/null || echo "Locale info not available"

# ============================================================================
# 16. RECOMMENDED DEPLOYMENT PATH
# ============================================================================

print_section "16. RECOMMENDED DEPLOYMENT PATH"

echo "Based on current system configuration:"
echo ""
print_info "Recommended Base Directory" "$HOME/claude-test"
print_info "ClaudePrompt Directory" "$HOME/claude-test/ClaudePrompt"
print_info "TestPrompt Directory" "$HOME/claude-test/TestPrompt"

echo ""
echo "Directory Creation Test:"
TEST_DIR="$HOME/.ultrathink_deployment_test"
if mkdir -p "$TEST_DIR" 2>/dev/null; then
    print_success "Can create directories in $HOME"
    rmdir "$TEST_DIR"
else
    print_warning "Cannot create directories in $HOME"
fi

# ============================================================================
# DISCOVERY COMPLETE
# ============================================================================

print_section "SYSTEM DISCOVERY COMPLETE"

echo ""
echo "Report generated: $(date)"
echo ""
echo "NEXT STEPS:"
echo "1. Save this output to a file: system_config.txt"
echo "2. Send the complete output to Claude Code"
echo "3. Claude will analyze the configuration and create tailored deployment instructions"
echo ""
echo "Command to save output:"
echo "  bash system_discovery.sh > system_config.txt"
echo ""
echo "================================================================================"
echo ""
