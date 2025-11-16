# AI Implementation Prompt - Phase 20

## Phase Information
- **Phase ID**: 20
- **Phase Name**: Security Certifications (SOC 2, HITRUST)
- **Story Points**: 42
- **Description**: SOC 2 Type II, HITRUST, penetration testing

## AI Assistant Instructions

You are implementing **Phase 20: Security Certifications (SOC 2, HITRUST)** of the SwarmCare v2.1 Ultimate healthcare AI platform.

### Your Mission
Implement this phase following production-ready standards with 100% quality.

### Key Requirements

1. **Use Guardrails**
   - ALWAYS import and use MultiLayerGuardrailSystem
   - Validate ALL user inputs
   - Sanitize ALL outputs
   - Never bypass security checks

2. **Follow Architecture**
   - Implement in `phases/phase20/code/`
   - Write tests in `phases/phase20/tests/`
   - Document in `phases/phase20/docs/`
   - Track state in `phases/phase20/.state/`

3. **Quality Standards**
   - Write clean, documented code
   - Achieve >80% test coverage
   - Handle all edge cases
   - Follow PEP 8 style guide
   - Add comprehensive error handling

### Phase-Specific Guidance

Security certifications - prepare for SOC 2 Type II and HITRUST compliance

### Code Template

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'guardrails'))

from multi_layer_system import MultiLayerGuardrailSystem

class Phase20Implementation:
    def __init__(self):
        self.guardrails = MultiLayerGuardrailSystem()
    
    def process(self, input_data):
        validated = self.guardrails.validate(input_data)
        result = self._core_logic(validated)
        return self.guardrails.sanitize_output(result)
```

### Resources

- Phase README: `phases/phase20/README.md`
- Implementation Guide: `phases/phase20/docs/IMPLEMENTATION_GUIDE.md`
- Main Documentation: `../../CORRECTED_AND_COMPLETE.md`

---

**Version**: 2.1 Ultimate (Enhanced)
**Last Updated**: 2025-10-27
