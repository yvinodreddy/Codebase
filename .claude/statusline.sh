#!/bin/bash
# Claude Code Status Line - Based on your bash PS1

# Read JSON input from stdin
input=$(cat)

# Extract current working directory - try multiple methods
cwd=""

# Method 1: Look for workspace.current_dir
if [[ "$input" =~ \"current_dir\":\"([^\"]+)\" ]]; then
  cwd="${BASH_REMATCH[1]}"
fi

# Method 2: Look for cwd field
if [ -z "$cwd" ] && [[ "$input" =~ \"cwd\":\"([^\"]+)\" ]]; then
  cwd="${BASH_REMATCH[1]}"
fi

# Method 3: Fallback to PWD
if [ -z "$cwd" ]; then
  cwd="$PWD"
fi

# Replace home directory with ~
cwd_display="${cwd/#$HOME/~}"

# Get user and hostname
user=$(whoami)
host=$(hostname -s)

# Output with colors (matching your bash PS1)
printf '\033[01;32m%s@%s\033[00m:\033[01;34m%s\033[00m' "$user" "$host" "$cwd_display"
