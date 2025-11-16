# Quick Reference Card

## 🚀 One-Liners

```bash
# Basic usage
python cli_interface.py "Your prompt here"

# With Claude API
python cli_interface.py --claude "Your prompt"

# Interactive mode
python cli_interface.py --interactive

# Save to file
python cli_interface.py --output results.json "Your prompt"

# Run demo
python demo.py

# Run tests
python test_orchestration.py
```

## 🐍 Python Quick Start

```python
from master_orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator(min_confidence_score=96.0)
result = orchestrator.process("Your prompt")

print(f"Confidence: {result.confidence_score:.2f}%")
print(f"Success: {result.success}")
print(f"Output: {result.output}")
```

## 📊 Confidence Score Guide

| Score | Meaning | Action |
|-------|---------|--------|
| 96-100% | Excellent | Use with confidence |
| 90-95% | Good | Review output |
| <90% | Needs work | Auto-refined |

## 🛡️ 7 Guardrail Layers

1. **Prompt Shields** - Jailbreak prevention
2. **Input Content** - Harmful content detection
3. **PHI Detection** - Privacy protection
4. **Terminology** - Medical accuracy
5. **Output Content** - Safe generation
6. **Groundedness** - Factual accuracy
7. **Compliance** - HIPAA & fact checking

## 🔧 Common Commands

```bash
# Adjust confidence
python cli_interface.py --min-confidence 98.0 "prompt"

# Use specific model
python cli_interface.py --claude --model claude-3-opus-20240229 "prompt"

# Verbose logging
python cli_interface.py -v "prompt"

# Help
python cli_interface.py --help
```

## 📁 File Structure

```
TestPrompt/
├── agent_framework/          # 8 agent components
├── guardrails/               # 5 guardrail files
├── prompt_preprocessor.py    # Intent classification
├── master_orchestrator.py    # Main coordinator
├── claude_integration.py     # Claude SDK
├── cli_interface.py          # CLI tool
├── demo.py                   # Demonstration
├── test_orchestration.py     # Tests
├── config.yaml               # Configuration
├── requirements.txt          # Dependencies
└── *.md                      # Documentation
```

## 🎯 Confidence Scoring Formula

```
Confidence = (
    Prompt Analysis × 15% +
    Agent Execution × 25% +
    Guardrails × 30% +
    Iteration Efficiency × 15% +
    Verification × 15%
)

Target: 96-100%
```

## 💡 Best Practices

1. ✅ Be specific in prompts
2. ✅ Provide context
3. ✅ Trust confidence scores ≥96%
4. ✅ Use appropriate thresholds
5. ✅ Review logs for insights

## 🐛 Quick Troubleshooting

**Problem:** API key error
**Fix:** Export `ANTHROPIC_API_KEY` or use local mode

**Problem:** Low confidence
**Fix:** Be more specific or let system auto-refine

**Problem:** Slow processing
**Fix:** Normal for complex validation (5-10s)

## 📚 Documentation Files

- `README.md` - Complete documentation
- `GETTING_STARTED.md` - Quick start guide
- `IMPLEMENTATION_SUMMARY.md` - What was built
- `QUICK_REFERENCE.md` - This file

## 🔗 Integration Examples

### Basic
```python
from master_orchestrator import MasterOrchestrator
orchestrator = MasterOrchestrator()
result = orchestrator.process("Explain AI")
```

### With Claude
```python
from claude_integration import ClaudeOrchestrator
orchestrator = ClaudeOrchestrator()
response = orchestrator.process("Explain AI")
print(response.response_text)
```

### Advanced
```python
orchestrator = MasterOrchestrator(
    min_confidence_score=98.0,
    max_refinement_iterations=5
)
result = orchestrator.process(
    prompt="Complex task",
    source_documents=["doc1.txt", "doc2.txt"]
)
```

## 📊 Statistics

```python
stats = orchestrator.get_statistics()
print(f"Success Rate: {stats['success_rate']:.2f}%")
print(f"Avg Confidence: {stats['average_confidence']:.2f}%")
```

## 🎮 Interactive Mode Commands

```
🤖 Enter prompt: Your prompt here
🤖 Enter prompt: quit    # Exit
```

## ⚙️ Environment Variables

```bash
ANTHROPIC_API_KEY=your_key
CONTENT_SAFETY_ENDPOINT=endpoint
CONTENT_SAFETY_KEY=key
ENABLE_PROMPT_SHIELDS=true
LOG_LEVEL=INFO
```

## 🧪 Testing

```bash
# Run all tests
python test_orchestration.py

# Run with pytest
pytest test_orchestration.py -v

# With coverage
pytest --cov=. --cov-report=html
```

## 📈 Success Metrics

- **Accuracy Target:** 96-100%
- **Success Rate:** >95%
- **Avg Processing:** 2-5 seconds
- **Guardrail Layers:** 7
- **Agent Components:** 8

## 🎯 What This System Does

```
INPUT: Any text prompt
  ↓
[Preprocessing] → Intent + Complexity
  ↓
[Guardrails 1-3] → Input validation
  ↓
[Agent Execution] → Smart processing
  ↓
[Guardrails 4-7] → Output validation
  ↓
[QA Scoring] → 96-100% confidence
  ↓
[Refinement] → If needed
  ↓
OUTPUT: High-quality result
```

## 💻 System Requirements

- Python 3.8+
- pip packages (see requirements.txt)
- Optional: Anthropic API key
- Optional: Azure Content Safety credentials

## 🎓 Learning Path

1. Run `demo.py`
2. Try `cli_interface.py` examples
3. Read `GETTING_STARTED.md`
4. Explore Python API
5. Customize `config.yaml`
6. Run `test_orchestration.py`

---

**Remember:** The system automatically refines until reaching 96-100% confidence. Trust the process! 🚀
