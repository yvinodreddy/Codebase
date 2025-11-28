#!/bin/bash
# phase8_python_package.sh
# CHANGE 8.2: Update Python package configuration

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase8_python_pkg_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 8.2: Python Package Configuration Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Update setup.py if exists
if [ -f "setup.py" ]; then
    cp setup.py setup.py.prebrand.bak

    sed -i 's/name="claudeprompt"/name="para-group-ai-orchestrator"/g' setup.py
    sed -i 's/name="ClaudePrompt"/name="ParaGroupAI"/g' setup.py
    sed -i 's|url=".*claudeprompt.*"|url="https://ai.paragroup.com"|g' setup.py

    echo "✅ Updated setup.py" | tee -a "$LOG_FILE"
fi

# Update pyproject.toml if exists
if [ -f "pyproject.toml" ]; then
    cp pyproject.toml pyproject.toml.prebrand.bak

    sed -i 's/name = "claudeprompt"/name = "para-group-ai-orchestrator"/g' pyproject.toml
    sed -i 's|homepage = ".*claudeprompt.*"|homepage = "https://ai.paragroup.com"|g' pyproject.toml

    echo "✅ Updated pyproject.toml" | tee -a "$LOG_FILE"
fi

echo "✅ PHASE 8.2 COMPLETE" | tee -a "$LOG_FILE"