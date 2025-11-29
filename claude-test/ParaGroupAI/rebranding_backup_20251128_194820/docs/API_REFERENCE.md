# ClaudePrompt API Reference

**Version:** 1.0
**Status:** Production

## Core APIs

### Command Line Interface

#### cpp (main command)
```bash
cpp "your prompt here" [options]
```

**Options:**
- `--verbose`, `-v`: Enable verbose output
- `--track N`: Use track number for parallel execution
- `--help`: Show help message

**Returns:** Exit code 0 on success, 1 on failure

### Python APIs

#### Telemetry Database

```python
from monitoring.telemetry import telemetry

# Log an execution
telemetry.log_execution(
    prompt="Test prompt",
    iterations=3,
    final_confidence=99.2,
    success=True
)

# Query low confidence executions
low_conf = telemetry.query_low_confidence(threshold=95.0)

# Get statistics
stats = telemetry.get_statistics()
```

---

**Full API reference:** See individual module documentation
