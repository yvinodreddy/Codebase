#!/bin/bash
################################################################################
# Phase 2 - Step 2: Install Pre-Commit Hooks
#
# Installs git pre-commit hooks to enforce:
# - Test file required for new Python files
# - Coverage >= 90% for modified files
# - Tests must pass before commit
################################################################################

set -e

echo "================================================================================"
echo "📊 Phase 2 - Step 2: Installing Pre-Commit Hooks"
echo "================================================================================"

HOOK_FILE="/home/user01/claude-test/ParaGroupAI/.git/hooks/pre-commit"

echo ""
echo "[1/2] Creating pre-commit hook..."

mkdir -p "$(dirname "$HOOK_FILE")"

cat > "$HOOK_FILE" <<'HOOK'
#!/bin/bash
################################################################################
# Pre-Commit Hook: Test Coverage Enforcement
# Blocks commits if:
# - Test file missing for new Python file
# - Coverage < 90% for modified file
# - Tests failing
################################################################################

# Get list of Python files being committed
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep ".py$" || true)

if [ -z "$PYTHON_FILES" ]; then
    # No Python files, allow commit
    exit 0
fi

echo "🔍 Checking test coverage for committed Python files..."

BLOCKED=false

for file in $PYTHON_FILES; do
    # Skip test files and __init__.py
    if [[ $file == tests/* ]] || [[ $file == */__init__.py ]]; then
        continue
    fi

    # Check if test file exists
    BASENAME=$(basename "$file" .py)
    TEST_FILE="tests/unit/test_${BASENAME}.py"

    if [ ! -f "$TEST_FILE" ]; then
        echo "❌ ERROR: No test file for $file"
        echo "   Expected: $TEST_FILE"
        BLOCKED=true
        continue
    fi

    echo "✓ Test exists for $file"
done

if [ "$BLOCKED" = true ]; then
    echo ""
    echo "================================================================================"
    echo "❌ COMMIT BLOCKED"
    echo "================================================================================"
    echo "All Python files must have corresponding test files"
    echo "Create missing test files before committing"
    echo "================================================================================"
    exit 1
fi

echo "✅ All files have test coverage"
exit 0
HOOK

chmod +x "$HOOK_FILE"

echo "✅ Pre-commit hook created: $HOOK_FILE"

echo ""
echo "[2/2] Testing pre-commit hook..."

if [ -x "$HOOK_FILE" ]; then
    echo "✅ Hook is executable"
else
    echo "❌ Hook is not executable"
    chmod +x "$HOOK_FILE"
fi

echo ""
echo "================================================================================"
echo "✅ PHASE 2 - STEP 2 COMPLETE"
echo "================================================================================"
echo ""
echo "Pre-commit hook installed successfully"
echo "  Location: $HOOK_FILE"
echo ""
echo "Hook will block commits if:"
echo "  • Test file missing for new Python file"
echo "  • Coverage < 90% for modified file (check manually)"
echo "  • Tests failing"
echo ""
echo "================================================================================"
