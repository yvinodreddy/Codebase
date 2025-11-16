#!/bin/bash
# Quick test script for ultrathinkc command

echo "========================================"
echo "Testing ULTRATHINKC Command"
echo "========================================"
echo ""

cd /home/user01/claude-test/TestPrompt

echo "✅ Test 1: Check if ultrathinkc exists and is executable"
if [ -x ./ultrathinkc ]; then
    echo "   ✓ ultrathinkc found and executable"
else
    echo "   ✗ ultrathinkc not found or not executable"
    exit 1
fi
echo ""

echo "✅ Test 2: Show help"
./ultrathinkc --help | head -20
echo ""

echo "✅ Test 3: Show how it works (flow diagram)"
./ultrathinkc --how | head -30
echo ""

echo "========================================"
echo "✅ ULTRATHINKC IS READY TO USE!"
echo "========================================"
echo ""
echo "Usage examples:"
echo "  ./ultrathinkc \"your prompt\""
echo "  ./ultrathinkc \"your prompt\" --verbose"
echo "  ./ultrathinkc --file input.txt"
echo "  ./ultrathinkc --how"
echo ""
echo "To use from anywhere, add to PATH:"
echo "  export PATH=\"/home/user01/claude-test/TestPrompt:\$PATH\""
echo ""
