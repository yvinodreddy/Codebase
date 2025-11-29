# ClaudePrompt/ULTRATHINK Architecture

**Version:** 1.0
**Last Updated:** 2025-11-14
**Status:** Production

## Overview

ClaudePrompt is an orchestration framework that wraps Claude AI with multiple layers of validation, verification, and enhancement to achieve 99-100% accuracy targets.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│                     (cpp "prompt" -v)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   STAGE 1: PREPROCESSING                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Complexity Analysis (SIMPLE/MEDIUM/COMPLEX)        │  │
│  │ • Agent Allocation (5-500 agents)                    │  │
│  │ • Priority Assignment (CRITICAL/HIGH/MEDIUM)         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 2: INPUT GUARDRAILS (3 layers)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Layer 1: Prompt Shields (jailbreak detection)       │  │
│  │ Layer 2: Content Filtering (harmful content)        │  │
│  │ Layer 3: PHI Detection (privacy protection)         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               STAGE 3: CONTEXT MANAGEMENT                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • 200K Token Window Tracking                         │  │
│  │ • Auto-compaction at 85% threshold                   │  │
│  │ • File Access Permissions                            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 4: AGENT ORCHESTRATION                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Parallel Execution (up to 500 agents)              │  │
│  │ • Task Distribution                                  │  │
│  │ • Result Aggregation                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            STAGE 5: OUTPUT GUARDRAILS (5 layers)             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Layer 4: Medical Terminology Check                   │  │
│  │ Layer 5: Output Content Filtering                    │  │
│  │ Layer 6: Groundedness (factual accuracy)             │  │
│  │ Layer 7: Compliance & Fact Checking                  │  │
│  │ Layer 8: Hallucination Detection (8 methods)         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           STAGE 6: ITERATIVE REFINEMENT                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Confidence Scoring                                 │  │
│  │ • If <99%: Refine & Re-execute (max 20 iterations)   │  │
│  │ • Adaptive Feedback Loops                            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATED OUTPUT                          │
│                  (99-100% confidence)                        │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Master Orchestrator (`master_orchestrator.py`)
- Entry point for all processing
- Coordinates 6-stage pipeline
- Manages global state and configuration

### 2. Guardrail System (`guardrails/`)
- 8 comprehensive validation layers
- Input protection (Layers 1-3)
- Output validation (Layers 4-8)
- Multiple detection techniques per layer

### 3. Agent Framework (`agent_framework/`)
- Parallel agent execution
- Task distribution and aggregation
- Priority-based scheduling
- Result verification system

### 4. Context Manager (`context_manager.py`)
- 200K token window tracking
- Automatic compaction
- File access control
- Memory optimization

### 5. Feedback Loop (`feedback_loop.py`)
- Iterative refinement up to 20 iterations
- Confidence scoring
- Gap analysis and refinement
- Convergence tracking

## Design Principles

1. **Defense in Depth:** Multiple validation layers
2. **Fail Safe:** Conservative error handling
3. **Observable:** Comprehensive logging and telemetry
4. **Scalable:** Parallel execution architecture
5. **Production-Ready:** Zero breaking changes guarantee

## Performance Characteristics

- **Latency:** +5-10s per iteration (vs base Claude)
- **Throughput:** Up to 500 parallel agents
- **Accuracy:** Target 99-100% (empirical validation in progress)
- **Memory:** 200K token window (max supported by Claude)

## Security

- Input sanitization through 3 guardrail layers
- Output validation through 5 guardrail layers
- PHI detection and redaction
- Jailbreak attempt prevention
- Content filtering

## Monitoring

- Real-time telemetry (SQLite database)
- Performance metrics tracking
- Confidence score logging
- Guardrail pass/fail rates
- Iteration statistics

---

**This architecture achieves world-class AI orchestration through systematic validation.**
