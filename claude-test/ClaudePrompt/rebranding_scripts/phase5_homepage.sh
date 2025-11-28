#!/bin/bash
# phase5_homepage.sh
# CHANGE 5.1: Update website homepage

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase5_homepage_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 5.1: Homepage Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Find website files
WEBSITE_FILES=$(find . -type f \
    \( -name "index.html" -o -name "index.htm" -o -name "*.html" \) \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*")

for file in $WEBSITE_FILES; do
    # Backup
    cp "$file" "${file}.prebrand.bak"

    # Update title tags
    sed -i 's/<title>ClaudePrompt/<title>Para Group AI Orchestrator®/g' "$file"

    # Update heading tags
    sed -i 's/<h1>ClaudePrompt/<h1>Para Group AI Orchestrator®/g' "$file"
    sed -i 's/<h2>ClaudePrompt/<h2>Para Group AI Orchestrator®/g' "$file"

    # Update meta tags
    sed -i 's/content="ClaudePrompt/content="Para Group AI Orchestrator®/g' "$file"

    # Add trademark notice
    if ! grep -q "Para Group® is a registered trademark" "$file"; then
        sed -i 's|</body>|<footer><p>Para Group® is a registered trademark of Para Group LLC</p></footer>\n</body>|' "$file"
    fi

    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

echo "✅ PHASE 5.1 COMPLETE" | tee -a "$LOG_FILE"