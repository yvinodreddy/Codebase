# Getting Started with the Orchestration System

**Target: 96-100% Accuracy for Every Prompt**

This guide will help you quickly get started with the comprehensive orchestration system that routes all prompts through multi-layer guardrails and agent frameworks for maximum accuracy.

## 🎯 What This System Does

When you ask a question, this system:

1. **Analyzes your intent** - Understands what you're trying to accomplish
2. **Validates for safety** - Runs through 7 layers of guardrails
3. **Executes intelligently** - Uses the right components (search, code generation, verification, etc.)
4. **Refines iteratively** - Keeps improving until reaching 96-100% confidence
5. **Verifies quality** - Multiple verification methods ensure accuracy
6. **Logs everything** - Full transparency and monitoring

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd /home/user01/claude-test/TestPrompt
pip install -r requirements.txt
```

### Step 2: Set Up Environment (Optional)

For full functionality with Azure guardrails and Claude API:

```bash
# Create .env file
cat > .env << 'EOF'
# Azure Content Safety (for guardrails)
CONTENT_SAFETY_ENDPOINT=your_endpoint_here
CONTENT_SAFETY_KEY=your_key_here
CONTENT_SAFETY_API_VERSION=2024-09-01

# Claude API (optional, for Claude integration)
ANTHROPIC_API_KEY=your_key_here

# Guardrail Settings
ENABLE_PROMPT_SHIELDS=true
ENABLE_CONTENT_FILTERING=true
ENABLE_PHI_DETECTION=true
EOF
```

**Note:** The system works without API keys too! It will use local orchestration.

### Step 3: Run Your First Prompt

```bash
# Simple example
python cli_interface.py "What is machine learning?"

# Or try the demo
python demo.py
```

## 💻 Usage Examples

### Example 1: Simple Question

```bash
python cli_interface.py "Explain what an API is"
```

**What happens:**
- ✅ Intent classified as "question"
- ✅ Complexity assessed as "simple"
- ✅ Runs through guardrails validation
- ✅ Executes with feedback loop
- ✅ Verifies output quality
- ✅ Returns result with confidence score

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 96.50%
Iterations: 3
Duration: 1.2s
```

### Example 2: Code Generation

```bash
python cli_interface.py "Write a Python function to calculate Fibonacci numbers"
```

**What happens:**
- ✅ Intent classified as "code_generation"
- ✅ Code generator component activated
- ✅ Multi-method verification (syntax, security, style)
- ✅ Iterative refinement until code quality meets threshold
- ✅ Full guardrails validation

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 98.20%
Iterations: 4
Duration: 2.4s

Generated code passes all verification:
  ✓ Syntax check
  ✓ Security check
  ✓ Style check
  ✓ Guardrails validation
```

### Example 3: Complex Multi-Step Task

```bash
python cli_interface.py "Implement a medical diagnosis system with guardrails and compliance"
```

**What happens:**
- ✅ Intent classified as "task"
- ✅ Complexity assessed as "very_complex"
- ✅ Multiple components activated (context manager, subagent orchestrator)
- ✅ All 7 guardrail layers applied
- ✅ HIPAA compliance validation
- ✅ Medical terminology verification
- ✅ Fact checking
- ✅ Iterative refinement to reach 96%+ confidence

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 97.80%
Iterations: 8
Duration: 5.6s

Pipeline Components Used:
  ✓ Context Manager
  ✓ Feedback Loop
  ✓ Subagent Orchestrator
  ✓ Verification System
  ✓ All 7 Guardrail Layers
```

## 🎮 Interactive Mode

For an interactive session where you can ask multiple questions:

```bash
python cli_interface.py --interactive
```

```
INTERACTIVE MODE
================

Using local orchestrator

🤖 Enter prompt: What is Python?

Processing...

Confidence: 96.50%
Output: [Response here]

🤖 Enter prompt: Write a function to reverse a string

Processing...

Confidence: 98.00%
Output: [Response here]

🤖 Enter prompt: quit
```

## 🔧 Configuration

### Adjust Confidence Threshold

```bash
# Require 98% confidence (stricter)
python cli_interface.py --min-confidence 98.0 "Your prompt"

# Allow 90% confidence (more lenient)
python cli_interface.py --min-confidence 90.0 "Your prompt"
```

### Save Results to File

```bash
python cli_interface.py --output results.json "Explain neural networks"
```

The JSON file will contain:
- Full prompt analysis
- Guardrails validation results
- Agent execution details
- Confidence breakdown
- Quality metrics
- Warnings and errors

### Use Claude API

If you have an Anthropic API key:

```bash
python cli_interface.py --claude "Write a comprehensive guide on REST APIs"
```

With specific model:

```bash
python cli_interface.py --claude --model claude-3-opus-20240229 "Complex analysis task"
```

## 📊 Understanding Confidence Scores

The system calculates confidence based on 5 factors:

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Prompt Analysis** | 15% | How well we understood your intent |
| **Agent Execution** | 25% | Success of task execution |
| **Guardrails Validation** | 30% | Safety and compliance (7 layers) |
| **Iteration Efficiency** | 15% | How efficiently we reached the solution |
| **Verification Results** | 15% | Multi-method verification scores |

**Target:** 96-100% = High confidence, production-ready

**Good:** 90-95% = Acceptable, may have minor issues

**Needs Work:** <90% = System will auto-refine or flag

## 🛡️ The 7-Layer Guardrail System

Every prompt goes through 7 validation layers:

### Input Validation (Layers 1-3)
1. **Prompt Shields** - Blocks jailbreak/injection attempts
2. **Content Filtering** - Detects harmful content
3. **PHI Detection** - Protects patient privacy

### Output Validation (Layers 4-7)
4. **Medical Terminology** - Validates clinical accuracy
5. **Output Content** - Ensures safe generation
6. **Groundedness** - Checks factual accuracy
7. **Compliance** - HIPAA compliance & fact checking

**Result:** Comprehensive safety and quality validation

## 🧪 Testing Your Setup

### Run the Demo

```bash
python demo.py
```

This will demonstrate:
- Prompt preprocessing
- Full orchestration pipeline
- Confidence scoring
- Error handling
- Performance characteristics

### Run the Test Suite

```bash
python test_orchestration.py
```

This will:
- Test all components
- Validate integration
- Check performance
- Generate coverage report

## 📈 Monitoring and Statistics

### View Orchestrator Statistics

```python
from master_orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator()

# Process some prompts
orchestrator.process("Test 1")
orchestrator.process("Test 2")

# Get statistics
stats = orchestrator.get_statistics()
print(f"Success Rate: {stats['success_rate']:.2f}%")
print(f"Average Confidence: {stats['average_confidence']:.2f}%")
```

### View Guardrails Statistics

```python
from guardrails.monitoring import get_monitor

monitor = get_monitor()

# Generate report
report = monitor.generate_report()
print(report)
```

## 🐍 Python API

### Basic Usage

```python
from master_orchestrator import MasterOrchestrator

# Create orchestrator
orchestrator = MasterOrchestrator(
    min_confidence_score=96.0,
    max_refinement_iterations=5
)

# Process prompt
result = orchestrator.process("Explain quantum computing")

# Check results
if result.success:
    print(f"Confidence: {result.confidence_score:.2f}%")
    print(f"Output: {result.output}")
else:
    print(f"Failed: {result.errors}")
```

### With Claude Integration

```python
from claude_integration import ClaudeOrchestrator

# Create Claude orchestrator
orchestrator = ClaudeOrchestrator(
    model="claude-sonnet-4-5-20250929",
    min_confidence_score=96.0
)

# Process with Claude
response = orchestrator.process(
    prompt="Explain machine learning",
    max_tokens=2048
)

# Access results
print(response.response_text)
print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
print(f"Cost: ${response.cost_estimate:.6f}")
```

## 🎯 Best Practices

### 1. Be Specific

**Good:** "Write a Python function to calculate the nth Fibonacci number using recursion"

**Less Good:** "Make a Fibonacci thing"

### 2. Provide Context

**Good:** "Implement a REST API for user authentication that includes JWT tokens and follows security best practices"

**Less Good:** "Make an API"

### 3. Trust the Confidence Score

- **96-100%** - Production ready, use with confidence
- **90-95%** - Review output, likely good but verify
- **<90%** - System will auto-refine or needs clarification

### 4. Use Appropriate Thresholds

- **Critical systems** (medical, financial): Use 98%+ threshold
- **Standard applications**: Use 96% threshold (default)
- **Exploratory tasks**: Use 90% threshold

## 🔍 Troubleshooting

### Problem: "ANTHROPIC_API_KEY must be set"

**Solution:** Either:
1. Set the API key: `export ANTHROPIC_API_KEY=your_key`
2. Don't use `--claude` flag (use local orchestrator)

### Problem: Low confidence scores (<90%)

**Solution:** The system will automatically:
1. Trigger iterative refinement
2. Increase iterations
3. Apply additional verification

You can also:
- Be more specific in your prompt
- Provide more context
- Break complex tasks into smaller parts

### Problem: Slow processing

**Solution:**
- Simple prompts should take 1-3 seconds
- Complex prompts may take 5-10 seconds
- This is normal for comprehensive validation

To speed up:
- Lower `--min-confidence` threshold
- Use simpler prompts
- Disable some guardrails (not recommended)

## 📚 Next Steps

1. **Read the Full README** - `README.md` has comprehensive documentation
2. **Explore Components** - Each file has detailed docstrings
3. **Run Tests** - `test_orchestration.py` shows usage examples
4. **Customize** - Edit `config.yaml` for your needs
5. **Integrate** - Use the Python API in your application

## 🎓 Learning Path

### Beginner
1. Run the demo: `python demo.py`
2. Try CLI examples: `python cli_interface.py "Your prompt"`
3. Read `README.md`

### Intermediate
1. Use Python API in your code
2. Adjust confidence thresholds
3. Customize configuration in `config.yaml`
4. Run test suite

### Advanced
1. Extend with custom components
2. Add custom guardrails
3. Integrate with your LLM application
4. Implement custom verification methods

## 💡 Tips for Maximum Accuracy

1. **Clear Prompts** - The better your prompt, the better the analysis
2. **Use Defaults** - The 96% threshold is optimized for quality
3. **Trust the Process** - The system will refine until it reaches confidence
4. **Review Logs** - Check `orchestrator.log` for detailed insights
5. **Monitor Statistics** - Track success rates and confidence scores

## 🎉 You're Ready!

You now have everything you need to use the comprehensive orchestration system. Start with simple prompts and gradually explore more complex use cases.

**Remember:** The goal is 96-100% accuracy for every prompt. The system is designed to help you achieve this through comprehensive validation and iterative refinement.

Happy orchestrating! 🚀
