================================================================================
CODEBASE ANALYSIS REPORT
================================================================================


================================================================================
SECURITY: 105 issues
================================================================================

CRITICAL (63 issues):
--------------------------------------------------------------------------------

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 430
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 435
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 445
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 456
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 474
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 479
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 489
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_mcp_integration.py
Line: 500
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/perfection_99_20251113_093052/tests/unit/test_claude_integration.py
Line: 166
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

Type: Hardcoded Secret
File: backups/absolute_perfection_20251113_094806/tests/unit/test_mcp_integration.py
Line: 430
Description: Potential hardcoded secret detected
Code: *** REDACTED ***

... and 53 more

HIGH (42 issues):
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

Type: SQL Injection Risk
File: backups/perfection_99_20251113_093052/analyze_codebase.py
Line: 40
Description: SQL query uses string formatting instead of parameterized queries
Code: if 'execute' in line and ('f"' in line or '%" ' in line or '.format(' in line):

... and 32 more

================================================================================
PERFORMANCE: 906 issues
================================================================================

MEDIUM (59 issues):
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

... and 49 more

LOW (847 issues):
--------------------------------------------------------------------------------

Type: Resource Leak
File: update_realtime_metrics.py
Line: 37
Description: File opened without context manager (may leak file descriptor)
Code: with open(METRICS_FILE, 'r') as f:

Type: Resource Leak
File: update_realtime_metrics.py
Line: 78
Description: File opened without context manager (may leak file descriptor)
Code: with open(temp_file, 'w') as f:

Type: Resource Leak
File: update_realtime_metrics.py
Line: 99
Description: File opened without context manager (may leak file descriptor)
Code: with open(METRICS_FILE, 'r') as f:

Type: Resource Leak
File: update_realtime_metrics.py
Line: 122
Description: File opened without context manager (may leak file descriptor)
Code: with open(METRICS_FILE, 'w') as f:

Type: Resource Leak
File: get_live_context_metrics.py
Line: 244
Description: File opened without context manager (may leak file descriptor)
Code: with open(args.input, 'r') as f:

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

... and 837 more

================================================================================
CODE QUALITY: 10713 issues
================================================================================

MEDIUM (627 issues):
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
File: multi_source_metrics_verifier.py
Line: 605
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: multi_source_metrics_verifier.py
Line: 613
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: live_metrics_tracker.py
Line: 136
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: live_metrics_tracker.py
Line: 238
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

Type: Bare Except Clause
File: live_metrics_tracker.py
Line: 295
Description: Bare except clause catches all exceptions (use specific exceptions)
Code: except:

... and 617 more

LOW (10086 issues):
--------------------------------------------------------------------------------

Type: Missing Docstring
File: update_realtime_metrics.py
Line: 127
Description: FunctionDef 'main' missing docstring
Code: def main...

Type: Print Statement
File: update_realtime_metrics.py
Line: 83
Description: Using print() instead of logging
Code: print(f"Error writing metrics: {e}", file=sys.stderr)

Type: Print Statement
File: update_realtime_metrics.py
Line: 143
Description: Using print() instead of logging
Code: print("✓ Metrics reset successfully")

Type: Print Statement
File: update_realtime_metrics.py
Line: 145
Description: Using print() instead of logging
Code: print("✗ Failed to reset metrics", file=sys.stderr)

Type: Print Statement
File: update_realtime_metrics.py
Line: 156
Description: Using print() instead of logging
Code: print("✓ Metrics updated successfully")

Type: Print Statement
File: update_realtime_metrics.py
Line: 158
Description: Using print() instead of logging
Code: print("✗ Failed to update metrics", file=sys.stderr)

Type: Missing Docstring
File: get_live_context_metrics.py
Line: 30
Description: FunctionDef '__init__' missing docstring
Code: def __init__...

Type: Print Statement
File: get_live_context_metrics.py
Line: 248
Description: Using print() instead of logging
Code: print(json.dumps({'status': 'error', 'error': str(e)}))

Type: Print Statement
File: get_live_context_metrics.py
Line: 255
Description: Using print() instead of logging
Code: print(extractor.to_json())

Type: Print Statement
File: get_live_context_metrics.py
Line: 257
Description: Using print() instead of logging
Code: print(extractor.to_text())

... and 10076 more

================================================================================
TEST COVERAGE: 5 issues
================================================================================

MEDIUM (4 issues):
--------------------------------------------------------------------------------

Type: Missing Tests
File: backups/20251113_091039/archive/old_python/portable_orchestrator.py
Description: Critical file missing test coverage

Type: Missing Tests
File: archive/old_python/portable_orchestrator.py
Description: Critical file missing test coverage

Type: Missing Tests
File: backups/perfection_20251113_092213/backups/20251113_091039/archive/old_python/portable_orchestrator.py
Description: Critical file missing test coverage

Type: Missing Tests
File: backups/perfection_20251113_092213/archive/old_python/portable_orchestrator.py
Description: Critical file missing test coverage

INFO (1 issues):
--------------------------------------------------------------------------------

Type: Test Coverage
File: Overall
Description: Test coverage: 92.3% (455/493 files)
Code: 38 files untested

================================================================================
SUMMARY
================================================================================
Total Issues: 11729
  Security: 105
  Performance: 906
  Code Quality: 10713
  Test Coverage: 5