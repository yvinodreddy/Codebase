#!/usr/bin/env python3
"""Quick test to verify enable_dual_retrieval parameter exists"""

import sys
import inspect
from pathlib import Path

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent))

# Force-clear any cached imports
for module in list(sys.modules.keys()):
    if 'context_manager' in module or 'master_orchestrator' in module:
        del sys.modules[module]

# Import fresh
from context_manager_enhanced import ContextManagerEnhanced

# Check the signature
sig = inspect.signature(ContextManagerEnhanced.__init__)
print(f"ContextManagerEnhanced.__init__ parameters:")
for param_name, param in sig.parameters.items():
    if param_name != 'self':
        print(f"  - {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'no type'} = {param.default if param.default != inspect.Parameter.empty else 'required'}")

# Check specifically for enable_dual_retrieval
if 'enable_dual_retrieval' in sig.parameters:
    print("\n✅ enable_dual_retrieval parameter EXISTS")
    print(f"   Default value: {sig.parameters['enable_dual_retrieval'].default}")
else:
    print("\n❌ enable_dual_retrieval parameter MISSING")
    print("\nAvailable parameters:")
    print(list(sig.parameters.keys()))

# Try to create with the parameter
try:
    cm = ContextManagerEnhanced(
        max_tokens=100000,
        project_id="test",
        enable_dual_retrieval=True
    )
    print("\n✅ Successfully created ContextManagerEnhanced with enable_dual_retrieval=True")
except TypeError as e:
    print(f"\n❌ FAILED to create with enable_dual_retrieval: {e}")
