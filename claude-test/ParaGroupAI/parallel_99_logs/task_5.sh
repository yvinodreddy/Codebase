#!/bin/bash
set -euo pipefail

echo "🔹 Task 5 started at $(date)" > "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "   Processing: /home/user01/claude-test/ClaudePrompt/parallel_99_logs/chunk_ae" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"

CREATED=0
FAILED=0
SKIPPED=0

while IFS= read -r SOURCE_FILE; do
    # Skip empty lines
    [[ -z "$SOURCE_FILE" ]] && continue

    # Generate test file name
    TEST_NAME=$(basename "$SOURCE_FILE" .py)
    TEST_FILE="tests/unit_99_coverage/test_${TEST_NAME}_t5.py"

    echo "   Processing: $SOURCE_FILE → $TEST_FILE" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"

    # Generate test using fixed generator
    if python3 generate_real_test_fixed.py "$SOURCE_FILE" "$TEST_FILE" 5 >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log" 2>&1; then
        # Validate syntax
        if python3 -m py_compile "$TEST_FILE" 2>> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"; then
            echo "      ✅ Created and validated" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
            ((CREATED++))
        else
            echo "      ❌ Failed syntax validation" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
            rm -f "$TEST_FILE"
            ((FAILED++))
        fi
    else
        echo "      ⚠️  Skipped (generation failed)" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
        ((SKIPPED++))
    fi
done < "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/chunk_ae"

echo "" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "🔹 Task 5 completed at $(date)" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "   ✅ Created: $CREATED" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "   ❌ Failed: $FAILED" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "   ⚠️  Skipped: $SKIPPED" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
echo "" >> "/home/user01/claude-test/ClaudePrompt/parallel_99_logs/task_5.log"
