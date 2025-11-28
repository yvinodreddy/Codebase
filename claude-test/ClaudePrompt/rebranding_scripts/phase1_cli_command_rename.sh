#!/bin/bash
# phase1_cli_command_rename.sh
# CHANGE 1.2: CLI command rename cpp → prsg

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="rebranding_logs/phase1_cli_rename_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 1.2: CLI Command Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "From: cpp" | tee -a "$LOG_FILE"
echo "To: prsg (Para gRoup aiS orGanizer)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Step 1: Rename main CLI script (create symlink for backward compatibility)
echo "Step 1: Renaming CLI script..." | tee -a "$LOG_FILE"
cd /home/user01/claude-test/ClaudePrompt

if [ -f "cpp" ]; then
    # Create new prsg command
    cp cpp prsg
    echo "✅ Created: prsg" | tee -a "$LOG_FILE"

    # Keep cpp as symlink for backward compatibility (deprecation period)
    mv cpp cpp.original
    ln -s prsg cpp
    echo "✅ Created backward compatibility symlink: cpp → prsg" | tee -a "$LOG_FILE"
else
    echo "❌ ERROR: cpp file not found" | tee -a "$LOG_FILE"
    exit 1
fi

# Step 2: Update bash alias in ~/.bashrc
echo "Step 2: Updating bash alias..." | tee -a "$LOG_FILE"
if grep -q "alias cpp=" ~/.bashrc; then
    # Add new alias
    echo "alias prsg='/home/user01/claude-test/ClaudePrompt/prsg'" >> ~/.bashrc
    echo "✅ Added alias: prsg" | tee -a "$LOG_FILE"

    # Update cpp alias to point to prsg (backward compatibility)
    sed -i "s|alias cpp=.*|alias cpp='/home/user01/claude-test/ClaudePrompt/cpp' # DEPRECATED: Use 'prsg' instead|" ~/.bashrc
    echo "✅ Updated alias: cpp (now deprecated)" | tee -a "$LOG_FILE"
else
    echo "alias prsg='/home/user01/claude-test/ClaudePrompt/prsg'" >> ~/.bashrc
    echo "✅ Added alias: prsg (no previous cpp alias found)" | tee -a "$LOG_FILE"
fi

# Step 3: Update documentation references
echo "Step 3: Updating documentation..." | tee -a "$LOG_FILE"
FILES=$(find /home/user01/claude-test/ClaudePrompt \
    -type f \
    \( -name "*.md" -o -name "README*" \) \
    ! -path "*/.git/*" \
    ! -path "*/rebranding_logs/*")

for file in $FILES; do
    # Replace cpp command references with prsg
    sed -i 's/```bash.*cpp /```bash\nprsg /g' "$file"
    sed -i 's/`cpp /`prsg /g' "$file"
    sed -i 's/The cpp command/The prsg command/g' "$file"
    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

# Step 4: Update Python code references
echo "Step 4: Updating Python code..." | tee -a "$LOG_FILE"
PYTHON_FILES=$(find /home/user01/claude-test/ClaudePrompt \
    -type f -name "*.py" \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/rebranding_logs/*")

for file in $PYTHON_FILES; do
    # Update command references in strings
    sed -i "s/'cpp'/'prsg'/g" "$file"
    sed -i 's/"cpp"/"prsg"/g' "$file"
    echo "✅ Updated: $file" | tee -a "$LOG_FILE"
done

# Step 5: Update get_output_path.py
echo "Step 5: Updating get_output_path.py..." | tee -a "$LOG_FILE"
if [ -f "get_output_path.py" ]; then
    sed -i 's/cppultrathink_output/prsgultrathink_output/g' get_output_path.py
    echo "✅ Updated: get_output_path.py" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 1.2 COMPLETE" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"
echo "✅ CLI command renamed: cpp → prsg" | tee -a "$LOG_FILE"
echo "✅ Backward compatibility maintained (cpp → prsg symlink)" | tee -a "$LOG_FILE"
echo "✅ Documentation updated" | tee -a "$LOG_FILE"
echo "✅ Python code updated" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "NOTE: Run 'source ~/.bashrc' to activate new alias" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"