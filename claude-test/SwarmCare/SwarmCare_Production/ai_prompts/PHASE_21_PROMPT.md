# AI Implementation Prompt - Phase 21

## Phase Information
- **Phase ID**: 21
- **Phase Name**: Closed-Loop Clinical Automation
- **Story Points**: 38
- **Description**: Automated ordering, smart alerts, workflow automation

## AI Assistant Instructions

You are implementing **Phase 21: Closed-Loop Clinical Automation** of the SwarmCare v2.1 Ultimate healthcare AI platform.

### Your Mission
Implement this phase following production-ready standards with 100% quality.

### Key Requirements

1. **Use Guardrails**
   - ALWAYS import and use MultiLayerGuardrailSystem
   - Validate ALL user inputs
   - Sanitize ALL outputs
   - Never bypass security checks

2. **Follow Architecture**
   - Implement in `phases/phase21/code/`
   - Write tests in `phases/phase21/tests/`
   - Document in `phases/phase21/docs/`
   - Track state in `phases/phase21/.state/`

3. **Quality Standards**
   - Write clean, documented code
   - Achieve >80% test coverage
   - Handle all edge cases
   - Follow PEP 8 style guide
   - Add comprehensive error handling

### Phase-Specific Guidance

Implement Closed-Loop Clinical Automation following production standards

### Code Template

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'guardrails'))

from multi_layer_system import MultiLayerGuardrailSystem

class Phase21Implementation:
    def __init__(self):
        self.guardrails = MultiLayerGuardrailSystem()
    
    def process(self, input_data):
        validated = self.guardrails.validate(input_data)
        result = self._core_logic(validated)
        return self.guardrails.sanitize_output(result)
```

### Resources

- Phase README: `phases/phase21/README.md`
- Implementation Guide: `phases/phase21/docs/IMPLEMENTATION_GUIDE.md`
- Main Documentation: `../../CORRECTED_AND_COMPLETE.md`

---

**Version**: 2.1 Ultimate (Enhanced)
**Last Updated**: 2025-10-27
