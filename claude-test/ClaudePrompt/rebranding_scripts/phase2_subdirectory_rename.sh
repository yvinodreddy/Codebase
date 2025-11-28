#!/bin/bash
# phase2_subdirectory_rename.sh
# CHANGE 2.2: Rename subdirectories

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase2_subdirs_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 2.2: Subdirectory Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

# Define directory mappings (old_name:new_name)
declare -A DIR_MAP=(
    ["claudeprompt_core"]="paragroup_core"
    ["claudeprompt_utils"]="paragroup_utils"
    ["claudeprompt_web"]="paragroup_web"
)

# Process each directory mapping
for old_dir in "${!DIR_MAP[@]}"; do
    new_dir="${DIR_MAP[$old_dir]}"

    if [ -d "$old_dir" ]; then
        echo "Renaming: $old_dir → $new_dir" | tee -a "$LOG_FILE"
        mv "$old_dir" "$new_dir"

        # Create symlink for backward compatibility
        ln -s "$new_dir" "$old_dir"
        echo "✅ Created symlink: $old_dir → $new_dir" | tee -a "$LOG_FILE"
    else
        echo "⏭️  Skipped: $old_dir (does not exist)" | tee -a "$LOG_FILE"
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "✅ PHASE 2.2 COMPLETE - Subdirectories renamed" | tee -a "$LOG_FILE"