#!/bin/bash
# phase2_directory_rename.sh
# CHANGE 2.1: Rename main directory

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/rebranding_logs/phase2_directory_${TIMESTAMP}.log"

# Create log directory at parent level (since we're moving the directory)
mkdir -p /home/user01/claude-test/rebranding_logs

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 2.1: Directory Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "From: /home/user01/claude-test/ClaudePrompt/" | tee -a "$LOG_FILE"
echo "To: /home/user01/claude-test/ParaGroupAI/" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd /home/user01/claude-test

# Step 1: Verify source directory exists
if [ ! -d "ClaudePrompt" ]; then
    echo "❌ ERROR: ClaudePrompt directory not found" | tee -a "$LOG_FILE"
    exit 1
fi

# Step 2: Create backup
echo "Step 1: Creating backup..." | tee -a "$LOG_FILE"
tar -czf "ClaudePrompt_backup_${TIMESTAMP}.tar.gz" ClaudePrompt/
echo "✅ Backup created: ClaudePrompt_backup_${TIMESTAMP}.tar.gz" | tee -a "$LOG_FILE"

# Step 3: Move directory
echo "Step 2: Renaming directory..." | tee -a "$LOG_FILE"
mv ClaudePrompt ParaGroupAI
echo "✅ Directory renamed" | tee -a "$LOG_FILE"

# Step 4: Create symlink for backward compatibility
echo "Step 3: Creating backward compatibility symlink..." | tee -a "$LOG_FILE"
ln -s ParaGroupAI ClaudePrompt
echo "✅ Symlink created: ClaudePrompt → ParaGroupAI" | tee -a "$LOG_FILE"

# Step 5: Update bash aliases
echo "Step 4: Updating bash aliases..." | tee -a "$LOG_FILE"
sed -i 's|/home/user01/claude-test/ClaudePrompt/|/home/user01/claude-test/ParaGroupAI/|g' ~/.bashrc
echo "✅ Bash aliases updated" | tee -a "$LOG_FILE"

# Step 6: Update any absolute path references in files
echo "Step 5: Updating absolute path references..." | tee -a "$LOG_FILE"
FILES=$(find /home/user01/claude-test/ParaGroupAI \
    -type f \
    \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*")

for file in $FILES; do
    sed -i 's|/home/user01/claude-test/ClaudePrompt/|/home/user01/claude-test/ParaGroupAI/|g' "$file"
done
echo "✅ Absolute paths updated" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 2.1 COMPLETE" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "✅ Directory renamed: ClaudePrompt → ParaGroupAI" | tee -a "$LOG_FILE"
echo "✅ Backward compatibility maintained (ClaudePrompt → ParaGroupAI symlink)" | tee -a "$LOG_FILE"
echo "✅ All path references updated" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"