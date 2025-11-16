#!/usr/bin/env python3
"""
Real-Time CPP Task Monitoring Dashboard - Production Grade

Key Features:
- Auto-discovers ALL cpp tasks (running or completed)
- Real-time process detection
- Status indicators: COMPLETED, EXECUTING, WAITING, FAILED
- System resources AT THE TOP
- Live progress tracking
- Detects any cpp task running anywhere on the system

Usage:
    python3 dashboard_realtime.py
    Then open http://localhost:8890 in browser
"""

import asyncio
import glob
import json
import os
import psutil
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn


# Configuration
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"
UPDATE_INTERVAL = 0.5  # Update every 500ms for real-time feel
PORT = 8890


class CPPTaskMonitor:
    """Monitor a single cpp task (running or completed)"""

    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.task_name = output_file.stem
        self.last_size = 0
        self.last_modified = None
        self.last_line_count = 0
        self.status = "UNKNOWN"
        self.current_task = "Initializing..."
        self.progress_percentage = 0
        self.associated_pid = None
        self.errors = []
        self.warnings = []
        self.start_time = None

    def is_completed(self, lines: List[str]) -> bool:
        """Check if task is completed (has answer marker)"""
        # Check for completion markers
        for line in reversed(lines[-50:] if len(lines) > 50 else lines):
            if "THE ANSWER ENDS HERE" in line or "ANSWER ENDS HERE" in line:
                return True
            if "COMPLETE" in line.upper() and "TRACK" in line.upper():
                return True
        return False

    def has_errors(self, lines: List[str]) -> bool:
        """Check for error conditions"""
        recent = lines[-100:] if len(lines) > 100 else lines
        error_count = sum(1 for line in recent if "ERROR" in line.upper() or "FAILED" in line.upper())
        return error_count > 5  # More than 5 errors = failed status

    def find_associated_process(self) -> Optional[int]:
        """Find cpp process writing to this file"""
        try:
            # Method 1: Check lsof for processes with this file open
            result = subprocess.run(
                ['lsof', '-t', str(self.output_file)],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0 and result.stdout.strip():
                pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid.isdigit()]
                if pids:
                    return pids[0]
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            pass

        # Method 2: Check for cpp processes with matching output file in command line
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and './cpp' in ' '.join(proc.info['cmdline']):
                        # Check if this process is redirecting to our file
                        cmdline_str = ' '.join(proc.info['cmdline'])
                        if str(self.output_file) in cmdline_str:
                            return proc.info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        return None

    def update(self) -> Dict:
        """Update metrics with real-time process detection"""
        if not self.output_file.exists():
            self.status = "PENDING"
            return self.get_metrics()

        # File stats
        stat = self.output_file.stat()
        current_size = stat.st_size
        current_modified = stat.st_mtime
        size_delta = current_size - self.last_size
        self.last_size = current_size

        # Check if file is being actively written
        file_is_growing = False
        if self.last_modified and current_modified > self.last_modified:
            file_is_growing = True
        self.last_modified = current_modified

        # Find associated process
        self.associated_pid = self.find_associated_process()

        # Read file content
        try:
            with open(self.output_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                self.last_line_count = len(lines)

                # Check completion status
                is_completed = self.is_completed(lines)
                has_errors = self.has_errors(lines)

                # Determine status
                if is_completed:
                    self.status = "COMPLETED"
                    self.progress_percentage = 100.0
                    self.current_task = "✅ Task completed successfully"
                elif has_errors:
                    self.status = "FAILED"
                    self.current_task = "❌ Task failed with errors"
                elif self.associated_pid or file_is_growing:
                    self.status = "EXECUTING"
                    # Estimate progress based on line count (assuming ~5000 lines = 100%)
                    self.progress_percentage = min(95.0, (self.last_line_count / 5000) * 100)
                    self._parse_current_task(lines[-50:])
                else:
                    # File exists, not growing, no process, not completed
                    self.status = "WAITING"
                    self.progress_percentage = min(95.0, (self.last_line_count / 5000) * 100)
                    self.current_task = "⏸️ Waiting for response..."

                # Extract errors/warnings
                self._extract_errors_warnings(lines[-100:])

        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            self.status = "ERROR"

        return self.get_metrics()

    def _parse_current_task(self, lines: List[str]):
        """Extract current task from recent log lines"""
        for line in reversed(lines):
            line_clean = line.strip()

            # Pattern 1: [VERBOSE] → Task
            if "[VERBOSE]" in line and "→" in line:
                task = line.split("→")[-1].strip()
                if task and len(task) < 150:
                    self.current_task = task
                    return

            # Pattern 2: [VERBOSE] ✓ Completed
            elif "[VERBOSE]" in line and "✓" in line:
                task = line.split("✓")[-1].strip()
                if task and len(task) < 150:
                    self.current_task = f"✓ {task}"
                    return

            # Pattern 3: STAGE X:
            elif "STAGE" in line and ":" in line:
                match = re.search(r'STAGE\s*(\d+):\s*(.+)', line)
                if match:
                    self.current_task = f"Stage {match.group(1)}: {match.group(2).strip()}"
                    return

            # Pattern 4: Action keywords
            elif any(kw in line for kw in ["Implementing", "Creating", "Writing", "Analyzing", "Processing"]):
                self.current_task = line_clean[:120]
                return

    def _extract_errors_warnings(self, lines: List[str]):
        """Extract recent errors and warnings"""
        self.errors = []
        self.warnings = []

        for line in lines:
            if "ERROR" in line.upper() or "FAIL" in line.upper():
                self.errors.append(line.strip()[:150])
            elif "WARNING" in line.upper() or "WARN" in line.upper():
                self.warnings.append(line.strip()[:150])

        # Keep only last 5
        self.errors = self.errors[-5:]
        self.warnings = self.warnings[-5:]

    def get_metrics(self) -> Dict:
        """Return metrics as dict"""
        return {
            "task_name": self.task_name,
            "output_file": str(self.output_file),
            "status": self.status,
            "progress": round(self.progress_percentage, 1),
            "current_task": self.current_task,
            "file_size_kb": round(self.last_size / 1024, 1),
            "line_count": self.last_line_count,
            "has_process": self.associated_pid is not None,
            "process_pid": self.associated_pid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class SystemMonitor:
    """Monitor system resources"""

    def __init__(self):
        self.start_time = time.time()

    def get_metrics(self) -> Dict:
        """Get current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(SCRIPT_DIR))

        # Find ALL cpp-related processes
        cpp_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                cmdline = proc.info['cmdline'] or []
                cmdline_str = ' '.join(cmdline)

                # Check for cpp or python processes related to ULTRATHINK
                if './cpp' in cmdline_str or 'cpp' == proc.info['name']:
                    cpp_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline_str[:100],
                        'cpu': round(proc.info['cpu_percent'] or 0, 1),
                        'memory': round(proc.info['memory_percent'] or 0, 1),
                        'uptime': round(time.time() - (proc.info['create_time'] or time.time()), 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                pass

        return {
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory.percent, 1),
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "disk_percent": round(disk.percent, 1),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "cpp_processes": cpp_processes
        }


class DashboardManager:
    """Manage all task monitors"""

    def __init__(self):
        self.task_monitors: Dict[str, CPPTaskMonitor] = {}
        self.system_monitor = SystemMonitor()
        self.last_scan = 0
        self.scan_interval = 2.0  # Scan for new tasks every 2 seconds

    def discover_tasks(self):
        """Auto-discover all cpp task output files"""
        current_time = time.time()
        if current_time - self.last_scan < self.scan_interval:
            return

        self.last_scan = current_time

        # Find all cppultrathink_output*.txt files
        pattern = str(TMP_DIR / "cppultrathink_output*.txt")
        output_files = glob.glob(pattern)

        # Also check /tmp/ for legacy files
        legacy_files = glob.glob("/tmp/cppultrathink_output*.txt")
        output_files.extend(legacy_files)

        # Create monitors for new tasks
        for file_path in output_files:
            path_obj = Path(file_path)
            task_key = path_obj.stem

            if task_key not in self.task_monitors:
                self.task_monitors[task_key] = CPPTaskMonitor(path_obj)

    async def get_all_metrics(self) -> Dict:
        """Get metrics for all tasks and system"""
        self.discover_tasks()

        # Update all task monitors
        tasks = []
        for monitor in self.task_monitors.values():
            metrics = monitor.update()
            tasks.append(metrics)

        # Sort by status priority: EXECUTING > WAITING > COMPLETED > FAILED
        status_priority = {"EXECUTING": 0, "WAITING": 1, "COMPLETED": 2, "FAILED": 3, "UNKNOWN": 4, "PENDING": 5}
        tasks.sort(key=lambda t: (status_priority.get(t['status'], 99), t['task_name']))

        system = self.system_monitor.get_metrics()

        return {
            "timestamp": datetime.now().isoformat(),
            "tasks": tasks,
            "system": system,
            "total_tasks": len(tasks),
            "executing_count": sum(1 for t in tasks if t['status'] == 'EXECUTING'),
            "completed_count": sum(1 for t in tasks if t['status'] == 'COMPLETED'),
            "waiting_count": sum(1 for t in tasks if t['status'] == 'WAITING'),
            "failed_count": sum(1 for t in tasks if t['status'] == 'FAILED'),
        }


# FastAPI application
app = FastAPI()
dashboard = DashboardManager()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time CPP Task Monitor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }

        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        /* SYSTEM RESOURCES AT THE TOP */
        .system-section {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .system-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .metric-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .metric-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
        }

        .process-list {
            margin-top: 15px;
            max-height: 150px;
            overflow-y: auto;
        }

        .process-item {
            background: rgba(0,0,0,0.2);
            padding: 8px;
            margin: 5px 0;
            border-radius: 5px;
            font-size: 0.9em;
        }

        /* STATS BAR */
        .stats-bar {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .stat-badge {
            background: rgba(255,255,255,0.15);
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            border: 1px solid rgba(255,255,255,0.3);
        }

        .stat-number {
            font-size: 1.8em;
            font-weight: bold;
            margin-left: 10px;
        }

        /* TASK CARDS */
        .tasks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
            gap: 20px;
        }

        .task-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 2px solid rgba(255,255,255,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }

        .task-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .task-name {
            font-size: 1.3em;
            font-weight: bold;
        }

        .status-badge {
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }

        .status-EXECUTING {
            background: #10b981;
            animation: pulse 2s infinite;
        }

        .status-COMPLETED {
            background: #3b82f6;
        }

        .status-WAITING {
            background: #f59e0b;
            animation: pulse 2s infinite;
        }

        .status-FAILED {
            background: #ef4444;
        }

        .status-UNKNOWN {
            background: #6b7280;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .progress-bar {
            width: 100%;
            height: 30px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .task-details {
            margin-top: 15px;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .current-task {
            background: rgba(0,0,0,0.2);
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-style: italic;
            min-height: 50px;
        }

        .errors-section {
            margin-top: 15px;
            padding: 12px;
            background: rgba(239, 68, 68, 0.2);
            border-radius: 8px;
            border-left: 4px solid #ef4444;
        }

        .warnings-section {
            margin-top: 15px;
            padding: 12px;
            background: rgba(245, 158, 11, 0.2);
            border-radius: 8px;
            border-left: 4px solid #f59e0b;
        }

        .error-item, .warning-item {
            font-size: 0.85em;
            margin: 5px 0;
            padding: 5px;
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
        }

        .last-update {
            text-align: center;
            margin-top: 20px;
            opacity: 0.7;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 Real-Time CPP Task Monitor</h1>
        <div class="subtitle">Live tracking of ALL cpp tasks with automatic discovery</div>

        <!-- SYSTEM RESOURCES AT THE TOP -->
        <div class="system-section">
            <div class="system-title">
                <span>💻</span>
                <span>System Resources</span>
                <span style="margin-left: auto; font-size: 0.8em;" id="uptime"></span>
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">CPU Usage</div>
                    <div class="metric-value" id="cpu">0%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Memory Usage</div>
                    <div class="metric-value" id="memory">0%</div>
                    <div style="font-size: 0.8em; opacity: 0.8; margin-top: 5px;" id="memory_detail"></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Disk Usage</div>
                    <div class="metric-value" id="disk">0%</div>
                    <div style="font-size: 0.8em; opacity: 0.8; margin-top: 5px;" id="disk_detail"></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Active CPP Processes</div>
                    <div class="metric-value" id="cpp_count">0</div>
                    <div class="process-list" id="cpp_processes"></div>
                </div>
            </div>
        </div>

        <!-- STATS BAR -->
        <div class="stats-bar">
            <div class="stat-badge">
                Total Tasks: <span class="stat-number" id="total_tasks">0</span>
            </div>
            <div class="stat-badge">
                🟢 Executing: <span class="stat-number" id="executing_count">0</span>
            </div>
            <div class="stat-badge">
                ⏸️ Waiting: <span class="stat-number" id="waiting_count">0</span>
            </div>
            <div class="stat-badge">
                ✅ Completed: <span class="stat-number" id="completed_count">0</span>
            </div>
            <div class="stat-badge">
                ❌ Failed: <span class="stat-number" id="failed_count">0</span>
            </div>
        </div>

        <!-- TASK CARDS -->
        <div class="tasks-grid" id="tasks_container"></div>

        <div class="last-update">
            Last update: <span id="last_update">Never</span>
        </div>
    </div>

    <script>
        let ws = null;

        function connect() {
            ws = new WebSocket('ws://localhost:' + window.location.port + '/ws');

            ws.onopen = () => {
                console.log('Connected to dashboard');
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };

            ws.onclose = () => {
                console.log('Disconnected, reconnecting...');
                setTimeout(connect, 1000);
            };
        }

        function updateDashboard(data) {
            // Update timestamp
            document.getElementById('last_update').textContent = new Date(data.timestamp).toLocaleTimeString();

            // Update stats
            document.getElementById('total_tasks').textContent = data.total_tasks;
            document.getElementById('executing_count').textContent = data.executing_count;
            document.getElementById('waiting_count').textContent = data.waiting_count;
            document.getElementById('completed_count').textContent = data.completed_count;
            document.getElementById('failed_count').textContent = data.failed_count;

            // Update system metrics
            const sys = data.system;
            document.getElementById('cpu').textContent = sys.cpu_percent + '%';
            document.getElementById('memory').textContent = sys.memory_percent + '%';
            document.getElementById('memory_detail').textContent = `${sys.memory_used_gb} GB / ${sys.memory_total_gb} GB`;
            document.getElementById('disk').textContent = sys.disk_percent + '%';
            document.getElementById('disk_detail').textContent = `${sys.disk_free_gb} GB free`;
            document.getElementById('uptime').textContent = `Uptime: ${Math.floor(sys.uptime_seconds / 60)}m ${Math.floor(sys.uptime_seconds % 60)}s`;
            document.getElementById('cpp_count').textContent = sys.cpp_processes.length;

            // Update CPP processes list
            const procList = document.getElementById('cpp_processes');
            if (sys.cpp_processes.length > 0) {
                procList.innerHTML = sys.cpp_processes.map(p => `
                    <div class="process-item">
                        PID ${p.pid}: ${p.name} | CPU: ${p.cpu}% | MEM: ${p.memory}%
                    </div>
                `).join('');
            } else {
                procList.innerHTML = '<div style="opacity: 0.6; padding: 10px;">No active cpp processes</div>';
            }

            // Update task cards
            const container = document.getElementById('tasks_container');
            container.innerHTML = data.tasks.map(task => `
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-name">${task.task_name}</div>
                        <div class="status-badge status-${task.status}">${task.status}</div>
                    </div>

                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%">
                            ${task.progress}%
                        </div>
                    </div>

                    <div class="task-details">
                        <div class="detail-row">
                            <span>File Size:</span>
                            <span>${task.file_size_kb} KB</span>
                        </div>
                        <div class="detail-row">
                            <span>Line Count:</span>
                            <span>${task.line_count.toLocaleString()}</span>
                        </div>
                        <div class="detail-row">
                            <span>Process:</span>
                            <span>${task.has_process ? '🟢 PID ' + task.process_pid : '⚪ Not running'}</span>
                        </div>
                    </div>

                    <div class="current-task">
                        ${task.current_task}
                    </div>

                    ${task.errors.length > 0 ? `
                        <div class="errors-section">
                            <div style="font-weight: bold; margin-bottom: 8px;">❌ Errors (${task.errors.length}):</div>
                            ${task.errors.map(e => `<div class="error-item">${e}</div>`).join('')}
                        </div>
                    ` : ''}

                    ${task.warnings.length > 0 ? `
                        <div class="warnings-section">
                            <div style="font-weight: bold; margin-bottom: 8px;">⚠️ Warnings (${task.warnings.length}):</div>
                            ${task.warnings.map(w => `<div class="warning-item">${w}</div>`).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        // Connect on page load
        connect();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard HTML"""
    return HTML_TEMPLATE


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()

    try:
        while True:
            # Get current metrics
            metrics = await dashboard.get_all_metrics()

            # Send to client
            await websocket.send_json(metrics)

            # Wait before next update
            await asyncio.sleep(UPDATE_INTERVAL)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    print(f"""
================================================================================
🔥 Real-Time CPP Task Monitor - Starting
================================================================================

Dashboard URL: http://localhost:{PORT}

Features:
  ✅ Auto-discovers ALL cpp tasks
  ✅ Real-time process detection
  ✅ Status indicators (COMPLETED/EXECUTING/WAITING/FAILED)
  ✅ System resources AT THE TOP
  ✅ Live progress tracking
  ✅ Updates every 500ms

Press Ctrl+C to stop
================================================================================
    """)

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
