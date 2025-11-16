# Comprehensive Orchestration System for Claude AI

**Target Accuracy: 96-100%**

A production-ready orchestration system that integrates all agent framework components and multi-layer guardrails to achieve maximum accuracy and reliability for AI-powered applications.

## 🎯 Overview

This system implements a comprehensive pipeline that processes user prompts through:

1. **Prompt Preprocessing & Intent Classification**
2. **Multi-Layer Guardrails Validation (7 Layers)**
3. **Adaptive Agent Execution with Feedback Loops**
4. **Multi-Method Verification**
5. **Quality Assurance & Confidence Scoring (96-100% target)**
6. **Iterative Refinement**
7. **Comprehensive Monitoring & Logging**

## 🏗️ Architecture

```
USER PROMPT
    ↓
[1] PROMPT PREPROCESSOR
    - Intent Classification
    - Complexity Analysis
    - Component Selection
    ↓
[2] GUARDRAILS INPUT VALIDATION (Layers 1-3)
    - Layer 1: Prompt Shields (jailbreak/injection prevention)
    - Layer 2: Input Content Filtering
    - Layer 3: PHI Detection
    ↓
[3] AGENT EXECUTION PIPELINE
    - Context Gathering (with context manager)
    - Action Execution (with subagent orchestration)
    - Verification (multi-method)
    - Feedback Loop (iterative refinement)
    ↓
[4] GUARDRAILS OUTPUT VALIDATION (Layers 4-7)
    - Layer 4: Medical Terminology Validation
    - Layer 5: Output Content Filtering
    - Layer 6: Groundedness Detection
    - Layer 7: HIPAA Compliance & Fact Checking
    ↓
[5] QUALITY ASSURANCE & CONFIDENCE SCORING
    - Calculate confidence score (target: 96-100%)
    - If score < threshold, trigger refinement
    ↓
[6] MONITORING & LOGGING
    - Track metrics, performance, and quality
    ↓
FINAL RESULT TO USER
```

## 📦 Components

### Agent Framework (`agent_framework/`)

- **feedback_loop.py** - Core agent pattern with self-correction
- **feedback_loop_enhanced.py** - Adaptive feedback loop with profiling
- **context_manager.py** - Context management with automatic compaction
- **code_generator.py** - Code generation with verification
- **agentic_search.py** - File system navigation using bash
- **mcp_integration.py** - Model Context Protocol integration
- **subagent_orchestrator.py** - Parallel subagent execution
- **verification_system.py** - Multi-method verification

### Guardrails (`guardrails/`)

- **multi_layer_system.py** - 7-layer guardrail orchestrator
- **azure_content_safety.py** - Azure AI Content Safety integration
- **medical_guardrails.py** - PHI, HIPAA, terminology, fact checking
- **crewai_guardrails.py** - CrewAI-specific guardrail functions
- **monitoring.py** - Monitoring and logging system

### Orchestration

- **prompt_preprocessor.py** - Intent classification and analysis
- **master_orchestrator.py** - Central orchestration coordinator
- **claude_integration.py** - Claude SDK integration layer
- **cli_interface.py** - User-friendly command-line interface

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

```bash
# Claude API (optional, for Claude integration)
ANTHROPIC_API_KEY=your_api_key_here

# Azure Content Safety (for guardrails)
CONTENT_SAFETY_ENDPOINT=your_endpoint
CONTENT_SAFETY_KEY=your_key
CONTENT_SAFETY_API_VERSION=2024-09-01

# Guardrail Settings
GUARDRAIL_CONTENT_THRESHOLD=2
GUARDRAIL_GROUNDEDNESS_THRESHOLD=20
ENABLE_PROMPT_SHIELDS=true
ENABLE_CONTENT_FILTERING=true
ENABLE_PHI_DETECTION=true
MEDICAL_TERMINOLOGY_VALIDATION=true
ENABLE_GROUNDEDNESS_CHECK=true

# Monitoring
ENABLE_METRICS_LOGGING=true
LOG_LEVEL=INFO
```

## 💻 Usage

### Command Line Interface

#### Basic Usage (Local Orchestrator)

```bash
python cli_interface.py "What is machine learning?"
```

#### With Claude API

```bash
python cli_interface.py --claude "Write a Python function to calculate Fibonacci numbers"
```

#### Interactive Mode

```bash
python cli_interface.py --interactive
```

#### Advanced Options

```bash
# Adjust confidence threshold
python cli_interface.py --min-confidence 98.0 "Implement a REST API"

# Save results to file
python cli_interface.py --output results.json "Explain neural networks"

# Use specific Claude model
python cli_interface.py --claude --model claude-3-opus-20240229 "Complex analysis task"

# Verbose logging
python cli_interface.py -v "Debug this prompt"
```

### Python API

#### Using Master Orchestrator

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
print(f"Success: {result.success}")
print(f"Confidence: {result.confidence_score:.2f}%")
print(f"Output: {result.output}")
print(f"Iterations: {result.iterations_performed}")
print(f"Duration: {result.total_duration_seconds:.2f}s")
```

#### Using Claude Integration

```python
from claude_integration import ClaudeOrchestrator

# Create Claude orchestrator
orchestrator = ClaudeOrchestrator(
    model="claude-sonnet-4-5-20250929",
    min_confidence_score=96.0
)

# Process with Claude
response = orchestrator.process(
    prompt="Write a Python function to reverse a string",
    max_tokens=2048,
    temperature=1.0
)

# Access results
print(f"Claude Response: {response.response_text}")
print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
print(f"Tokens: {response.total_tokens}")
print(f"Cost: ${response.cost_estimate:.6f}")
```

## 📊 Confidence Scoring

The system calculates a comprehensive confidence score (0-100%) based on:

| Component | Weight | Description |
|-----------|--------|-------------|
| Prompt Analysis | 15% | Quality of intent classification |
| Agent Execution | 25% | Success of task execution |
| Guardrails Validation | 30% | Safety and compliance checks |
| Iteration Efficiency | 15% | Efficiency vs. expected iterations |
| Verification Results | 15% | Multi-method verification results |

**Target:** 96-100% confidence score

## 🛡️ Guardrails

### 7-Layer Security & Quality System

1. **Layer 1: Prompt Shields** - Jailbreak and injection prevention
2. **Layer 2: Input Content Filtering** - Harmful content detection
3. **Layer 3: PHI Detection** - Patient privacy protection
4. **Layer 4: Medical Terminology** - Clinical accuracy validation
5. **Layer 5: Output Content Filtering** - Safe output generation
6. **Layer 6: Groundedness Detection** - Factual accuracy
7. **Layer 7: HIPAA Compliance & Fact Checking** - Regulatory compliance

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
python test_orchestration.py

# Run with pytest directly
pytest test_orchestration.py -v

# Run with coverage
pytest test_orchestration.py -v --cov=. --cov-report=html
```

### Test Categories

- **Preprocessor Tests** - Intent classification, complexity analysis
- **Orchestrator Tests** - Full pipeline integration
- **Integration Tests** - End-to-end workflows
- **Performance Tests** - Speed and efficiency validation

## 📈 Monitoring & Metrics

### View Statistics

```python
from master_orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator()

# Process some prompts
orchestrator.process("Test 1")
orchestrator.process("Test 2")

# Get statistics
stats = orchestrator.get_statistics()
print(stats)
# Output:
# {
#   "total_requests": 2,
#   "successful_requests": 2,
#   "failed_requests": 0,
#   "average_confidence": 95.5,
#   "average_iterations": 3.5,
#   "average_duration": 2.3,
#   "success_rate": 100.0
# }
```

### Guardrails Monitoring

```python
from guardrails.monitoring import get_monitor

monitor = get_monitor()

# Generate report
report = monitor.generate_report("report.txt")
print(report)
```

## 🎓 Examples

### Example 1: Simple Question

```bash
python cli_interface.py "What is machine learning?"
```

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 96.50%
Iterations: 3
Duration: 1.23s

Prompt Analysis:
   Intent: question
   Complexity: simple
   Required Components: ['feedback_loop']
```

### Example 2: Code Generation

```bash
python cli_interface.py "Write a Python function to calculate factorial"
```

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 98.20%
Iterations: 4
Duration: 2.45s

Prompt Analysis:
   Intent: code_generation
   Complexity: moderate
   Required Components: ['code_generator', 'feedback_loop', 'verification_system']
```

### Example 3: Complex Multi-Step Task

```bash
python cli_interface.py "Implement a comprehensive medical diagnosis system with guardrails"
```

**Output:**
```
Status: ✅ SUCCESS
Confidence Score: 97.80%
Iterations: 8
Duration: 5.67s

Prompt Analysis:
   Intent: task
   Complexity: very_complex
   Required Components: ['context_manager', 'feedback_loop', 'subagent_orchestrator', 'verification_system']
```

## 🔧 Configuration

Edit `config.yaml` to customize:

- Confidence thresholds
- Guardrail settings
- Agent framework parameters
- Model selection
- Monitoring options
- Performance tuning

## 📚 Documentation

### Key Concepts

**Feedback Loop:** The core pattern of gather context → take action → verify work → repeat until success.

**Context Compaction:** Automatic compression of conversation history to stay within token limits.

**Multi-Method Verification:** Combining rules-based, code, and LLM verification for robust validation.

**Subagent Orchestration:** Parallel execution of independent tasks for performance.

**Confidence Scoring:** Quantitative quality assessment targeting 96-100% accuracy.

## 🤝 Integration with Claude Code / Web

### Using in Claude Code

1. Copy the entire `TestPrompt` folder to your project
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in `.env`
4. Use the CLI or import in your code:

```python
from master_orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator(min_confidence_score=96.0)
result = orchestrator.process("Your prompt here")
```

### Using in Claude Web

While Claude Web doesn't directly execute Python, you can:

1. **Use the architecture concepts** - Implement similar multi-stage validation in your prompts
2. **Reference the patterns** - Ask Claude to follow the feedback loop pattern
3. **Apply guardrails thinking** - Structure prompts to include validation steps

**Example Prompt for Claude Web:**

```
Please process this request using a comprehensive approach:

1. Analyze my intent and requirements
2. Validate that my request is safe and appropriate
3. Execute the task with iterative refinement
4. Verify the output for quality and accuracy
5. Provide a confidence score (target: 96-100%)

My request: [Your actual prompt here]
```

## 🎯 Achieving 96-100% Accuracy

The system achieves high accuracy through:

1. **Comprehensive Preprocessing** - Understanding intent before execution
2. **Multi-Layer Validation** - 7 layers of guardrails for safety and quality
3. **Adaptive Feedback Loops** - Iterative refinement until quality threshold met
4. **Multi-Method Verification** - Multiple validation approaches
5. **Confidence Scoring** - Quantitative quality measurement
6. **Auto-Refinement** - Automatic re-processing if confidence below threshold
7. **Comprehensive Logging** - Full observability for debugging

## 📝 License

This orchestration system is provided as-is for educational and development purposes.

## 🙏 Acknowledgments

Built using:
- Anthropic's Claude AI and best practices
- Azure AI Content Safety
- Agent design patterns from Anthropic documentation
- Multi-layer guardrail architecture for medical AI applications

## 📞 Support

For questions or issues, please refer to the comprehensive documentation in each component file.

---

**Built with ❤️ for achieving 96-100% AI accuracy**

## 🔒 Security Features

ULTRATHINK includes enterprise-grade security:

- **🔒 Prompt Injection Protection**: 3-tier sanitization system (minimal/balanced/production)
- **🛡️ API Key Masking**: Prevents accidental key exposure in logs
- **⏱️ Rate Limiting**: 500 calls/6min (~83/min) to prevent cost overruns  
- **📝 Security Logging**: Dedicated audit trail (`logs/security_events.log`)
- **🔍 Dependency Scanning**: Automated vulnerability detection (pip-audit/safety)
- **🚫 File Path Validation**: Prevents directory traversal attacks
- **🔐 Error Sanitization**: Production-safe error messages

See [docs/SECURITY.md](docs/SECURITY.md) for full security documentation.

### Security Headers (Web Deployment)
If deploying ULTRATHINK via web interface, ensure these headers:
```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
```
