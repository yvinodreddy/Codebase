================================================================================
CODEBASE ANALYSIS REPORT
================================================================================


================================================================================
SECURITY: 18 issues
================================================================================

CRITICAL (9 issues):
--------------------------------------------------------------------------------

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 430
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 435
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 445
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 456
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 474
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 479
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 489
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_mcp_integration.py
Line: 500
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: tests/unit/test_claude_integration.py
Line: 166
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

HIGH (9 issues):
--------------------------------------------------------------------------------

Type: SQL Injection Risk
File: analyze_codebase.py
Line: 40
Description: SQL query uses string formatting instead of parameterized queries
Code: if 'execute' in line and ('f"' in line or '%" ' in line or '.format(' in line):

Type: Command Injection Risk
File: analyze_codebase.py
Line: 51
Description: Using shell=True or os.system can lead to command injection
Code: if ('os.system(' in line or 'shell=True' in line) and not line.strip().startswith('#'):

Type: Command Injection Risk
File: analyze_codebase.py
Line: 57
Description: Using shell=True or os.system can lead to command injection
Code: "description": "Using shell=True or os.system can lead to command injection",

Type: Command Injection Risk
File: agent_framework/agentic_search.py
Line: 88
Description: Using shell=True or os.system can lead to command injection
Code: shell=True,

Type: Command Injection Risk
File: agent_framework/agentic_search.py
Line: 135
Description: Using shell=True or os.system can lead to command injection
Code: shell=True,

Type: Command Injection Risk
File: agent_framework/agentic_search.py
Line: 263
Description: Using shell=True or os.system can lead to command injection
Code: shell=True,

Type: SQL Injection Risk
File: agent_framework/mcp_integration.py
Line: 255
Description: SQL query uses string formatting instead of parameterized queries
Code: logger.error(f"Failed to execute {server_name}.{tool_name}: {e}")

Type: Command Injection Risk
File: agent_framework/code_generator.py
Line: 358
Description: Using shell=True or os.system can lead to command injection
Code: ("os.system(", "Avoid os.system(), use subprocess")

Type: Command Injection Risk
File: archive/old_python/run_tests.py
Line: 18
Description: Using shell=True or os.system can lead to command injection
Code: result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

================================================================================
PERFORMANCE: 114 issues
================================================================================

MEDIUM (11 issues):
--------------------------------------------------------------------------------

Type: N+1 Query Pattern
File: setup_database.py
Line: 90
Description: Potential N+1 query pattern (query inside loop)
Code: # Create indexes for performance

Type: N+1 Query Pattern
File: setup_database.py
Line: 114
Description: Potential N+1 query pattern (query inside loop)
Code: for track_id, name, description, log_file in tracks:

Type: N+1 Query Pattern
File: analyze_codebase.py
Line: 90
Description: Potential N+1 query pattern (query inside loop)
Code: for i, line in enumerate(lines, 1):

Type: N+1 Query Pattern
File: analyze_codebase.py
Line: 91
Description: Potential N+1 query pattern (query inside loop)
Code: # Check for N+1 query patterns

Type: N+1 Query Pattern
File: analyze_codebase.py
Line: 92
Description: Potential N+1 query pattern (query inside loop)
Code: if 'for ' in line and i < len(lines) - 5:

Type: N+1 Query Pattern
File: realtime-tracking/setup_database.py
Line: 37
Description: Potential N+1 query pattern (query inside loop)
Code: # Enable WAL mode for better concurrency

Type: N+1 Query Pattern
File: realtime-tracking/setup_database.py
Line: 106
Description: Potential N+1 query pattern (query inside loop)
Code: # Create indexes for performance

Type: N+1 Query Pattern
File: realtime-tracking/setup_database.py
Line: 130
Description: Potential N+1 query pattern (query inside loop)
Code: for track_id, name, description, log_file in tracks:

Type: N+1 Query Pattern
File: realtime-tracking/websocket_server.py
Line: 311
Description: Potential N+1 query pattern (query inside loop)
Code: """Get recent log entries for a track"""

Type: N+1 Query Pattern
File: realtime-tracking/websocket_server.py
Line: 465
Description: Potential N+1 query pattern (query inside loop)
Code: """Get ULTRATHINK details for a track (agents, stages, guardrails)"""

... and 1 more

LOW (103 issues):
--------------------------------------------------------------------------------

Type: Resource Leak
File: streaming_output.py
Line: 96
Description: File opened without context manager (may leak file descriptor)
Code: with open(self.output_file, 'w', buffering=1) as outfile:  # Line buffering

Type: Resource Leak
File: streaming_output.py
Line: 156
Description: File opened without context manager (may leak file descriptor)
Code: with open(self.output_file, 'r') as f:

Type: Resource Leak
File: streaming_output.py
Line: 184
Description: File opened without context manager (may leak file descriptor)
Code: with open(self.output_file, 'r') as f:

Type: Resource Leak
File: streaming_output.py
Line: 290
Description: File opened without context manager (may leak file descriptor)
Code: with open(output_path, 'r') as f:

Type: Resource Leak
File: streaming_output.py
Line: 299
Description: File opened without context manager (may leak file descriptor)
Code: with open(output_path, 'r') as f:

Type: Resource Leak
File: streaming_output.py
Line: 326
Description: File opened without context manager (may leak file descriptor)
Code: with open(output_path, 'r') as f:

Type: Resource Leak
File: streaming_output.py
Line: 339
Description: File opened without context manager (may leak file descriptor)
Code: with open(output_path, 'r') as f:

Type: Resource Leak
File: ultrathink.py
Line: 1535
Description: File opened without context manager (may leak file descriptor)
Code: with open(file_path, 'r') as f:

Type: Resource Leak
File: realtime_log_monitor.py
Line: 31
Description: File opened without context manager (may leak file descriptor)
Code: with open(self.log_file, 'r') as f:

Type: Resource Leak
File: dashboard_archive.py
Line: 84
Description: File opened without context manager (may leak file descriptor)
Code: with open(self.output_file, 'r', encoding='utf-8', errors='ignore') as f:

... and 93 more

================================================================================
CODE QUALITY: 1874 issues
================================================================================

MEDIUM (15 issues):
--------------------------------------------------------------------------------

Type: Bare Except Clause
File: dashboard_archive.py
Line: 143
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: dashboard_archive.py
Line: 153
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: dashboard_archive.py
Line: 155
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: dashboard_archive.py
Line: 254
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: dashboard_archive.py
Line: 715
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: analyze_codebase.py
Line: 221
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: realtime-tracking/websocket_server.py
Line: 480
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: realtime-tracking/websocket_server.py
Line: 485
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: realtime-tracking/websocket_server.py
Line: 490
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: tests/e2e_framework.py
Line: 207
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

... and 5 more

LOW (1859 issues):
--------------------------------------------------------------------------------

Type: Print Statement
File: streaming_output.py
Line: 119
Description: Using print() instead of logging
Code: print(line, end='', flush=True)

Type: Print Statement
File: streaming_output.py
Line: 124
Description: Using print() instead of logging
Code: print(f"[Progress: {line_num} lines written...]", flush=True)

Type: Print Statement
File: streaming_output.py
Line: 243
Description: Using print() instead of logging
Code: >>> print(f"Generated {stream_out.line_count} lines")

Type: Print Statement
File: streaming_output.py
Line: 286
Description: Using print() instead of logging
Code: print(f"❌ ERROR: Output file not found: {output_file}")

Type: Print Statement
File: streaming_output.py
Line: 295
Description: Using print() instead of logging
Code: print("\n" + "="*80)

Type: Print Statement
File: streaming_output.py
Line: 296
Description: Using print() instead of logging
Code: print(f"📄 FULL OUTPUT ({line_count} lines)")

Type: Print Statement
File: streaming_output.py
Line: 297
Description: Using print() instead of logging
Code: print("="*80 + "\n")

Type: Print Statement
File: streaming_output.py
Line: 300
Description: Using print() instead of logging
Code: print(f.read())

Type: Print Statement
File: streaming_output.py
Line: 304
Description: Using print() instead of logging
Code: print("\n" + "="*80)

Type: Print Statement
File: streaming_output.py
Line: 305
Description: Using print() instead of logging
Code: print(f"📊 LARGE OUTPUT SUMMARY ({line_count:,} lines)")

... and 1849 more

================================================================================
TEST COVERAGE: 13 issues
================================================================================

MEDIUM (12 issues):
--------------------------------------------------------------------------------

Type: Missing Tests
File: guardrails/medical_guardrails.py
Description: Critical file missing test coverage

Type: Missing Tests
File: guardrails/crewai_guardrails.py
Description: Critical file missing test coverage

Type: Missing Tests
File: parallel_implementation/phase3_guardrails_fixes.py
Description: Critical file missing test coverage

Type: Missing Tests
File: security/security_headers.py
Description: Critical file missing test coverage

Type: Missing Tests
File: archive/old_python/portable_orchestrator.py
Description: Critical file missing test coverage

Type: Missing Tests
File: guardrails/hallucination_detector.py
Description: Critical file missing test coverage

Type: Missing Tests
File: agent_framework/subagent_orchestrator.py
Description: Critical file missing test coverage

Type: Missing Tests
File: guardrails/azure_content_safety.py
Description: Critical file missing test coverage

Type: Missing Tests
File: security/dependency_scanner.py
Description: Critical file missing test coverage

Type: Missing Tests
File: guardrails/multi_layer_system.py
Description: Critical file missing test coverage

... and 2 more

INFO (1 issues):
--------------------------------------------------------------------------------

Type: Test Coverage
File: Overall
Description: Test coverage: 38.8% (33/85 files)
Code: 52 files untested

================================================================================
SUMMARY
================================================================================
Total Issues: 2019
  Security: 18
  Performance: 114
  Code Quality: 1874
  Test Coverage: 13