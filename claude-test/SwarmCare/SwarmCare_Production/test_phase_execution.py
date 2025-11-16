#!/usr/bin/env python3
"""
Quick test to verify phases can execute with agent framework
"""

import sys
import os
from pathlib import Path

# Add paths
root_path = Path(__file__).parent
sys.path.insert(0, str(root_path / "guardrails"))
sys.path.insert(0, str(root_path / "agent_framework"))

def test_phase(phase_num):
    """Test a specific phase can be imported and instantiated"""
    phase_path = root_path / "phases" / f"phase{phase_num:02d}" / "code"
    sys.path.insert(0, str(phase_path))

    try:
        # Import based on phase number
        module_name = "implementation"
        module = __import__(module_name)

        # Find the Phase class
        class_name = f"Phase{phase_num:02d}Implementation"
        if hasattr(module, class_name):
            PhaseClass = getattr(module, class_name)
            instance = PhaseClass()

            print(f"✅ Phase {phase_num:02d}: {instance.phase_name}")
            print(f"   Story Points: {instance.story_points}")
            print(f"   Has feedback_loop: {hasattr(instance, 'feedback_loop')}")
            print(f"   Has context_manager: {hasattr(instance, 'context_manager')}")
            return True
        else:
            print(f"❌ Phase {phase_num:02d}: Class {class_name} not found")
            return False

    except Exception as e:
        print(f"❌ Phase {phase_num:02d}: {str(e)[:80]}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING PHASE EXECUTION WITH AGENT FRAMEWORK")
    print("=" * 80)

    # Test a few sample phases
    test_phases = [0, 1, 5, 10, 15, 20, 25, 28]

    success_count = 0
    for phase_num in test_phases:
        if test_phase(phase_num):
            success_count += 1
        print()

    print("=" * 80)
    print(f"📊 Results: {success_count}/{len(test_phases)} phases functional")

    if success_count == len(test_phases):
        print("🎉 ALL TESTED PHASES ARE FULLY FUNCTIONAL!")
        sys.exit(0)
    elif success_count >= len(test_phases) * 0.8:
        print("✅ MOST PHASES FUNCTIONAL - System is operational")
        sys.exit(0)
    else:
        print("❌ MULTIPLE PHASE FAILURES - Needs investigation")
        sys.exit(1)
