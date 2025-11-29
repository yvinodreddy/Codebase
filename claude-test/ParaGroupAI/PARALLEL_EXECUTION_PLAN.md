# 🚀 PARALLEL EXECUTION PLAN - Complete in < 2 Hours

**Execute these 3 tracks simultaneously in separate terminal windows**

## ⚡ TRACK 1: Fix Remaining 16 Tests (Window 1) - 20 min

```bash
cd /home/user01/claude-test/ClaudePrompt

# Get list of failing tests
pytest tests/unit_track1_core/*_real.py tests/unit_track3_guardrails/*_real.py tests/unit_track4_security/*_real.py tests/unit_track5_database/*_real.py tests/unit_track7_realtime/*_real.py tests/unit_track9_fixes/*_real.py --lf -v > /tmp/failures.txt 2>&1

# View failures
grep "FAILED\|ERROR" /tmp/failures.txt

# Fix them (I'll create a simple script)
python3 << 'EOF'
import subprocess, re
result = subprocess.run(["pytest", "tests/", "--lf", "-v"], capture_output=True, text=True, cwd="/home/user01/claude-test/ClaudePrompt")
print(result.stdout + result.stderr)
with open("/tmp/test_failures_detailed.txt", "w") as f:
    f.write(result.stdout + result.stderr)
print("\n✅ Saved to /tmp/test_failures_detailed.txt")
EOF
```

## ⚡ TRACK 2: Measure Current Coverage (Window 2) - 5 min

```bash
cd /home/user01/claude-test/ClaudePrompt

# Quick coverage measurement (excludes known problematic files)
pytest tests/unit_track1_core tests/unit_track2_agents tests/unit_track3_guardrails tests/unit_track4_security tests/unit_track5_database tests/unit_track6_infrastructure tests/unit_track7_realtime --cov=. --cov-report=json:coverage_NOW.json --cov-report=term -q 2>&1 | tail -50

# Check coverage
python3 -c "import json; d=json.load(open('coverage_NOW.json')); print(f'Coverage: {d[\"totals\"][\"percent_covered\"]:.2f}%')"
```

## ⚡ TRACK 3: Generate Tests for Low Coverage Files (Window 3) - 60 min

```bash
cd /home/user01/claude-test/ClaudePrompt

# Create quick test generator for ultra think.py (9% coverage → 90%)
cat > quick_generate_ultrathink_tests.py << 'EOF'
#!/usr/bin/env python3
import subprocess
print("Generating tests for ultrathink.py (currently 9%)")
# Use the existing test generator
subprocess.run(["python3", "generate_real_tests.py", "ultrathink.py", "--target-coverage", "90"])
EOF

chmod +x quick_generate_ultrathink_tests.py
python3 quick_generate_ultrathink_tests.py &

# Monitor progress
tail -f /tmp/test_generation.log
```

## 📊 SIMPLE PROGRESS TRACKING

After each track completes, check:

```bash
# Track 1 Status
grep "passed\|failed" /tmp/failures.txt | tail -1

# Track 2 Status
cat coverage_NOW.json | python3 -c "import json, sys; d=json.load(sys.stdin); print(f'{d[\"totals\"][\"percent_covered\"]:.1f}%')"

# Track 3 Status
find tests/ -name "test_ultrathink*.py" -newer /tmp -exec wc -l {} +
```

## ✅ COMPLETION CRITERIA

**Track 1:** 0 failing tests
**Track 2:** Coverage measured accurately
**Track 3:** At least 5 new test files created

## ⏱️ REALISTIC TIMELINE

| Track | Task | Time | Status |
|-------|------|------|--------|
| 1 | Fix 16 tests | 20 min | ⏳ |
| 2 | Measure coverage | 5 min | ⏳ |
| 3 | Generate tests | 60 min | ⏳ |

**TOTAL: ~60 min** (all running in parallel)

## 🎯 AFTER ALL 3 COMPLETE

```bash
# Final coverage check
cd /home/user01/claude-test/ClaudePrompt
pytest tests/ --cov=. --cov-report=json:coverage_FINAL.json --cov-report=html -q

# Git commit
git add .
git commit -m "Complete parallel execution: Fix tests + measure coverage + generate new tests"
git push
```

## 💡 KEY INSIGHT

**Instead of sequential execution taking 2-3 hours, we do it in 60 minutes by running 3 independent tasks simultaneously.**

This is NOT about "opening multiple Claude instances" - it's about running independent bash commands in parallel terminals.
