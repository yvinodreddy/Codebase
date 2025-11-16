#!/bin/bash
# Test the exact command that web UI runs

cd /home/user01/claude-test/ClaudePrompt

# Create temp prompt file like web UI does
TIMESTAMP=$(date +%s%3N)
TEMP_PROMPT="/home/user01/claude-test/ClaudePrompt/tmp/ultrathink-prompt-${TIMESTAMP}.txt"
echo "what is 2+2" > "$TEMP_PROMPT"

# Get output file path like web UI does
OUTPUT_FILE=$(python3 get_output_path.py)

echo "=========================================="
echo "WEB UI COMMAND SIMULATION"
echo "=========================================="
echo "Temp prompt file: $TEMP_PROMPT"
echo "Output file: $OUTPUT_FILE"
echo "Command: ./cpps --file \"$TEMP_PROMPT\" -v"
echo "=========================================="
echo ""

# Run the exact command with full output capture
./cpps --file "$TEMP_PROMPT" -v 2>&1 | tee /tmp/web_ui_test_output.txt

echo ""
echo "=========================================="
echo "Exit code: $?"
echo "=========================================="
echo "Check /tmp/web_ui_test_output.txt for full output"
echo "Check $OUTPUT_FILE for ULTRATHINK output"
