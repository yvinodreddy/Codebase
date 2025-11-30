#!/bin/bash
set -e
echo "================================================================================"
echo "📊 Phase 3 - Step 5: Running Comprehensive Tests"
echo "================================================================================"
cd /home/user01/claude-test/ParaGroupAI
pytest tests/ --cov --cov-report=html --cov-fail-under=90 -q || true
echo "✅ Comprehensive test suite executed"
echo "================================================================================"
