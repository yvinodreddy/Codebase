#!/usr/bin/env python3
"""
Generate tests for all 16 specified modules
"""
import subprocess
import sys
from pathlib import Path

# List of all modules to test
modules = [
    "fix_test_files_complete.py",
    "generate_100_percent_tests.py",
    "generate_effective_tests.py",
    "generate_real_coverage_tests.py",
    "generate_real_test_fixed.py",
    "generate_real_test_implementations.py",
    "generate_real_tests_for_module.py",
    "get_coverage_quickly.py",
    "get_live_context_metrics.py",
    "high_scale_orchestrator.py",
    "instance_id_manager.py",
    "large_scale_error_handler.py",
    "live_metrics_tracker.py",
    "master_orchestrator.py",
    "metrics_aggregator.py",
    "metrics_state_persistence.py"
]

output_dir = Path("tests/unit_instance3")
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🚀 GENERATING TESTS FOR ALL 16 MODULES")
print("=" * 80)

success_count = 0
failure_count = 0

for module in modules:
    module_path = Path(module)
    if not module_path.exists():
        print(f"❌ Module not found: {module}")
        failure_count += 1
        continue

    # Generate test file name
    test_file = output_dir / f"test_{module}"

    print(f"\n📝 Generating test for: {module}")
    print(f"   Output: {test_file}")

    # Run the generator
    try:
        result = subprocess.run(
            [sys.executable, "generate_real_tests_for_module.py", str(module_path), str(test_file)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and test_file.exists():
            print(f"   ✅ Success: Test generated")
            success_count += 1
        else:
            print(f"   ⚠️  Generator returned non-zero: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            failure_count += 1
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout: Generation took too long")
        failure_count += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        failure_count += 1

print("\n" + "=" * 80)
print("📊 GENERATION SUMMARY")
print("=" * 80)
print(f"✅ Successful: {success_count}/{len(modules)}")
print(f"❌ Failed:     {failure_count}/{len(modules)}")
print(f"📁 Output:     {output_dir}")

if success_count == len(modules):
    print("\n🎉 ALL TESTS GENERATED SUCCESSFULLY!")
    sys.exit(0)
else:
    print("\n⚠️  Some tests failed to generate. Check output above.")
    sys.exit(1)