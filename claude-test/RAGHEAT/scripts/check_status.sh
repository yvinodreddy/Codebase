#!/bin/bash

# RAGHEAT - Check Project Status
# Quick status overview

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          RAGHEAT - Project Status             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Use Python for reliable JSON parsing
python3 <<'EOF'
import json
from datetime import datetime

with open('PROJECT_STATE.json', 'r') as f:
    state = json.load(f)

# Current Phase
current = state['current_phase']
print(f"\033[1;32mCurrent Phase:\033[0m")
print(f"  Phase {current['phase_number']}: {current['phase_name']}")
print(f"  Status: {current['status'].upper()}")
print(f"  Progress: {current['progress_percentage']}%")
print()

# Overall Progress
total = state['total_tasks']
completed = state['completed_tasks']
percentage = state['overall_progress_percentage']

print(f"\033[1;32mOverall Progress:\033[0m")
print(f"  {completed}/{total} tasks completed ({percentage:.1f}%)")
print()

# Phase Breakdown
print(f"\033[1;32mPhase Breakdown:\033[0m")
for phase_key, phase_data in state['phases'].items():
    phase_num = phase_key.replace('phase_', '')
    name = phase_data['name']
    tasks_done = phase_data['tasks_completed']
    tasks_total = phase_data['tasks_total']
    status = phase_data['status']

    # Status emoji
    emoji = "⏳" if status == "in_progress" else "✅" if status == "completed" else "⏸️"

    print(f"  {emoji} Phase {phase_num}: {name}")
    print(f"     Tasks: {tasks_done}/{tasks_total} ({phase_data.get('duration_days', '?')} days)")

print()

# Next Actions
if state['next_actions']:
    print(f"\033[1;32mNext Actions:\033[0m")
    for i, action in enumerate(state['next_actions'][:5], 1):
        print(f"  {i}. {action}")
    print()

# Blockers
if state['blockers']:
    print(f"\033[1;31m⚠️  Blockers:\033[0m")
    for i, blocker in enumerate(state['blockers'], 1):
        print(f"  {i}. {blocker}")
    print()

# Metrics
metrics = state.get('metrics', {})
if metrics:
    print(f"\033[1;32mMetrics:\033[0m")

    velocity = metrics.get('velocity', {})
    if velocity.get('tasks_per_day', 0) > 0:
        print(f"  Velocity: {velocity['tasks_per_day']} tasks/day")

    quality = metrics.get('quality', {})
    if quality.get('code_coverage_percentage', 0) > 0:
        print(f"  Code Coverage: {quality['code_coverage_percentage']}%")

    performance = metrics.get('performance', {})
    if performance.get('uptime_percentage', 0) > 0:
        print(f"  Uptime: {performance['uptime_percentage']}%")
    print()

# Last Updated
last_updated = state['last_updated']
print(f"\033[1;34mLast Updated:\033[0m {last_updated}")
EOF
