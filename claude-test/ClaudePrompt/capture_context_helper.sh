#!/bin/bash
#
# capture_context_helper.sh - Helper functions for capturing /context output
#
# This script provides shell functions to capture /context command output
# and make it available to the statusline for LIVE metrics display.
#
# INSTALLATION:
# Add to your ~/.bashrc:
#   source /home/user01/claude-test/ClaudePrompt/capture_context_helper.sh
#
# USAGE (inside Claude Code session):
#   1. Run: /context | capture_context
#   2. Statusline will automatically use the live metrics
#
# OR use the auto-capture wrapper (recommended):
#   cpp_live "your prompt" --verbose
#

CONTEXT_CACHE="/tmp/claude_context_cache.txt"

# Function: capture_context
# Captures /context output from stdin and stores it in cache
capture_context() {
    local cache_file="${CONTEXT_CACHE}"

    # Read from stdin and save to cache
    cat > "$cache_file"

    # Verify capture was successful
    if [[ -f "$cache_file" ]] && [[ -s "$cache_file" ]]; then
        echo "✅ Context captured successfully to: $cache_file"
        echo "📊 Statusline will now show LIVE metrics"

        # Parse and display metrics immediately
        python3 /home/user01/claude-test/ClaudePrompt/get_live_context_metrics.py --input "$cache_file" 2>/dev/null
    else
        echo "❌ Failed to capture context"
        return 1
    fi
}

# Function: cpp_live
# Wrapper for cpp command that automatically captures /context before execution
# This provides LIVE metrics in statusline for the entire cpp execution
cpp_live() {
    local prompt="$1"
    shift
    local flags="$@"

    echo "🔄 Capturing live context metrics..."

    # Note: /context command needs to be run manually in Claude Code CLI
    # This function serves as a placeholder/reminder

    echo "📌 To enable LIVE metrics:"
    echo "   1. Run: /context"
    echo "   2. Copy output"
    echo "   3. Pipe to: capture_context"
    echo ""
    echo "Then run your cpp command normally."

    # Run cpp command normally
    /home/user01/claude-test/ClaudePrompt/cpp "$prompt" $flags
}

# Function: show_context_metrics
# Display currently cached context metrics (for debugging)
show_context_metrics() {
    local cache_file="${CONTEXT_CACHE}"

    if [[ ! -f "$cache_file" ]]; then
        echo "❌ No cached context found at: $cache_file"
        echo "Run /context | capture_context first"
        return 1
    fi

    local age=$(($(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0)))

    echo "📊 Cached Context Metrics (age: ${age}s)"
    echo "─────────────────────────────────────────"

    python3 /home/user01/claude-test/ClaudePrompt/get_live_context_metrics.py --input "$cache_file" 2>/dev/null

    if [[ $age -gt 60 ]]; then
        echo ""
        echo "⚠️  Cache is older than 60 seconds - may not reflect current state"
        echo "   Run /context | capture_context to refresh"
    fi
}

# Function: update_statusline_config
# Updates Claude Code settings to use the new live metrics statusline
update_statusline_config() {
    local settings_file="$HOME/.config/claude-code/settings.json"
    local statusline_script="/home/user01/claude-test/ClaudePrompt/statusline_with_live_metrics.sh"

    echo "🔧 Updating Claude Code statusline configuration..."

    # Check if settings file exists
    if [[ ! -f "$settings_file" ]]; then
        echo "❌ Claude Code settings not found: $settings_file"
        echo "   Create it first or run Claude Code to generate default settings"
        return 1
    fi

    # Backup existing settings
    cp "$settings_file" "$settings_file.backup_$(date +%Y%m%d_%H%M%S)"

    # Update statusline setting using Python
    python3 << EOF
import json

settings_file = "$settings_file"
statusline_script = "$statusline_script"

try:
    # Load existing settings
    with open(settings_file, 'r') as f:
        settings = json.load(f)

    # Update statusline
    settings['statusLine'] = statusline_script

    # Save updated settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

    print(f"✅ Statusline updated to: {statusline_script}")
    print("🔄 Restart Claude Code for changes to take effect")
except Exception as e:
    print(f"❌ Error updating settings: {e}")
    exit(1)
EOF
}

# Export functions for use in shell
export -f capture_context
export -f cpp_live
export -f show_context_metrics
export -f update_statusline_config

# Display help message if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    cat << 'EOF'
================================================================================
📊 LIVE METRICS CAPTURE HELPER
================================================================================

This script provides functions to capture /context output for live statusline
metrics display in Claude Code.

INSTALLATION:
  Add to ~/.bashrc:
    source /home/user01/claude-test/ClaudePrompt/capture_context_helper.sh

AVAILABLE FUNCTIONS:

  capture_context
    Captures /context output from stdin
    Usage: /context | capture_context

  show_context_metrics
    Display currently cached context metrics
    Usage: show_context_metrics

  update_statusline_config
    Update Claude Code settings to use live metrics statusline
    Usage: update_statusline_config

  cpp_live
    Wrapper for cpp command with live metrics reminder
    Usage: cpp_live "your prompt" --verbose

RECOMMENDED WORKFLOW:

  1. Install helper functions:
       source /home/user01/claude-test/ClaudePrompt/capture_context_helper.sh

  2. Update statusline (one-time setup):
       update_statusline_config

  3. In Claude Code, capture context:
       (Note: This is a manual process as /context is a CLI command)
       /context
       (Copy the output and run)
       echo "<paste output>" | capture_context

  4. Run your cpp commands normally - statusline will show LIVE metrics!

================================================================================
EOF
fi
