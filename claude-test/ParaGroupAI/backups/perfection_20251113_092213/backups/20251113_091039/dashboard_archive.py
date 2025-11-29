#!/usr/bin/env python3
"""
CPP Dashboard with Archive Support - Production Grade

Features:
- Active View: Currently running/waiting tasks only
- Archive View: Completed tasks with full history
- Detailed Task Modal: Click any task to see complete details
- Auto-archiving: Tasks automatically archived when completed
- Zero breaking changes: Extends existing functionality

Port: 8891
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
from typing import Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our archiver
import sys
sys.path.insert(0, str(Path(__file__).parent))
from task_archiver import TaskMetadataExtractor, TaskArchiveManager


# Configuration
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"
ARCHIVE_DIR = SCRIPT_DIR / "archive"
UPDATE_INTERVAL = 0.5
PORT = 8891


class CPPTaskWithArchive:
    """Enhanced task monitor with archive support"""

    def __init__(self, output_file: Path, archive_manager: TaskArchiveManager):
        self.output_file = output_file
        self.archive_manager = archive_manager
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
        self.metadata = None  # Cached metadata
        self.archived = False

    def update(self) -> Dict:
        """Update with archive support"""
        if not self.output_file.exists():
            self.status = "PENDING"
            return self.get_metrics()

        stat = self.output_file.stat()
        current_size = stat.st_size
        current_modified = stat.st_mtime
        self.last_size = current_size

        file_is_growing = False
        if self.last_modified and current_modified > self.last_modified:
            file_is_growing = True
        self.last_modified = current_modified

        self.associated_pid = self.find_associated_process()

        try:
            with open(self.output_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                self.last_line_count = len(lines)

                is_completed = self.is_completed(lines)
                has_errors = self.has_errors(lines)

                if is_completed:
                    self.status = "COMPLETED"
                    self.progress_percentage = 100.0
                    self.current_task = "✅ Task completed successfully"

                    # Auto-archive if not already archived
                    if not self.archived:
                        self.archive_task()

                elif has_errors:
                    self.status = "FAILED"
                    self.current_task = "❌ Task failed with errors"
                elif self.associated_pid or file_is_growing:
                    self.status = "EXECUTING"
                    self.progress_percentage = min(95.0, (self.last_line_count / 5000) * 100)
                    self._parse_current_task(lines[-50:])
                else:
                    self.status = "WAITING"
                    self.progress_percentage = min(95.0, (self.last_line_count / 5000) * 100)
                    self.current_task = "⏸️ Waiting for response..."

                self._extract_errors_warnings(lines[-100:])

        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            self.status = "ERROR"

        return self.get_metrics()

    def archive_task(self):
        """Archive this task"""
        try:
            extractor = TaskMetadataExtractor(self.output_file)
            self.metadata = extractor.extract_all()
            self.archive_manager.archive_task(self.metadata)
            self.archived = True
        except Exception as e:
            print(f"Error archiving task: {e}")

    def find_associated_process(self) -> Optional[int]:
        """Find cpp process writing to this file"""
        try:
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
        except:
            pass

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and './cpp' in ' '.join(proc.info['cmdline']):
                        cmdline_str = ' '.join(proc.info['cmdline'])
                        if str(self.output_file) in cmdline_str:
                            return proc.info['pid']
                except:
                    continue
        except:
            pass

        return None

    def is_completed(self, lines: List[str]) -> bool:
        """Check if task is completed"""
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
        return error_count > 5

    def _parse_current_task(self, lines: List[str]):
        """Extract current task from recent log lines"""
        for line in reversed(lines):
            line_clean = line.strip()
            if "[VERBOSE]" in line and "→" in line:
                task = line.split("→")[-1].strip()
                if task and len(task) < 150:
                    self.current_task = task
                    return
            elif "[VERBOSE]" in line and "✓" in line:
                task = line.split("✓")[-1].strip()
                if task and len(task) < 150:
                    self.current_task = f"✓ {task}"
                    return
            elif "STAGE" in line and ":" in line:
                match = re.search(r'STAGE\s*(\d+):\s*(.+)', line)
                if match:
                    self.current_task = f"Stage {match.group(1)}: {match.group(2).strip()}"
                    return
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
            "archived": self.archived,
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

        cpp_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                cmdline = proc.info['cmdline'] or []
                cmdline_str = ' '.join(cmdline)
                if './cpp' in cmdline_str or 'cpp' == proc.info['name']:
                    cpp_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline_str[:100],
                        'cpu': round(proc.info['cpu_percent'] or 0, 1),
                        'memory': round(proc.info['memory_percent'] or 0, 1),
                        'uptime': round(time.time() - (proc.info['create_time'] or time.time()), 1)
                    })
            except:
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


class DashboardWithArchive:
    """Dashboard manager with archive support"""

    def __init__(self):
        self.task_monitors: Dict[str, CPPTaskWithArchive] = {}
        self.system_monitor = SystemMonitor()
        self.archive_manager = TaskArchiveManager(ARCHIVE_DIR)
        self.last_scan = 0
        self.scan_interval = 2.0

    def discover_tasks(self):
        """Auto-discover all cpp task output files"""
        current_time = time.time()
        if current_time - self.last_scan < self.scan_interval:
            return

        self.last_scan = current_time

        pattern = str(TMP_DIR / "cppultrathink_output*.txt")
        output_files = glob.glob(pattern)
        legacy_files = glob.glob("/tmp/cppultrathink_output*.txt")
        output_files.extend(legacy_files)

        for file_path in output_files:
            path_obj = Path(file_path)
            task_key = path_obj.stem
            if task_key not in self.task_monitors:
                self.task_monitors[task_key] = CPPTaskWithArchive(path_obj, self.archive_manager)

    async def get_all_metrics(self, view_filter: str = "all") -> Dict:
        """Get metrics with filtering support"""
        self.discover_tasks()

        tasks = []
        for monitor in self.task_monitors.values():
            metrics = monitor.update()
            tasks.append(metrics)

        # Filter based on view
        if view_filter == "active":
            tasks = [t for t in tasks if t['status'] in ['EXECUTING', 'WAITING', 'PENDING']]
        elif view_filter == "archive":
            tasks = [t for t in tasks if t['status'] in ['COMPLETED', 'FAILED']]

        status_priority = {"EXECUTING": 0, "WAITING": 1, "COMPLETED": 2, "FAILED": 3, "UNKNOWN": 4, "PENDING": 5}
        tasks.sort(key=lambda t: (status_priority.get(t['status'], 99), t['task_name']))

        system = self.system_monitor.get_metrics()

        return {
            "timestamp": datetime.now().isoformat(),
            "tasks": tasks,
            "system": system,
            "total_tasks": len(self.task_monitors),
            "active_count": sum(1 for t in tasks if t['status'] in ['EXECUTING', 'WAITING', 'PENDING']),
            "archived_count": sum(1 for t in tasks if t['status'] in ['COMPLETED', 'FAILED']),
            "executing_count": sum(1 for t in tasks if t['status'] == 'EXECUTING'),
            "completed_count": sum(1 for t in tasks if t['status'] == 'COMPLETED'),
            "waiting_count": sum(1 for t in tasks if t['status'] == 'WAITING'),
            "failed_count": sum(1 for t in tasks if t['status'] == 'FAILED'),
        }


# FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dashboard = DashboardWithArchive()

# HTML template will be in next message due to length
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CPP Dashboard with Archive</title>
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
            margin-bottom: 20px;
            opacity: 0.9;
        }

        /* View Tabs */
        .view-tabs {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
        }
        .tab {
            padding: 12px 30px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1.1em;
            font-weight: bold;
        }
        .tab:hover {
            background: rgba(255,255,255,0.3);
        }
        .tab.active {
            background: rgba(255,255,255,0.4);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* System Section */
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

        /* Stats Bar */
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

        /* Task Cards */
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
        <h1>🔥 CPP Dashboard with Archive</h1>
        <div class="subtitle">Active tasks on main screen | Completed tasks in archive</div>

        <!-- View Tabs -->
        <div class="view-tabs">
            <div class="tab active" onclick="switchView('active')" id="tab-active">
                🔄 Active
            </div>
            <div class="tab" onclick="switchView('archive')" id="tab-archive">
                📦 Archive
            </div>
            <div class="tab" onclick="switchView('all')" id="tab-all">
                📊 All
            </div>
        </div>

        <!-- System Resources -->
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
                </div>
            </div>
        </div>

        <!-- Stats Bar -->
        <div class="stats-bar">
            <div class="stat-badge">
                Total: <span class="stat-number" id="total_tasks">0</span>
            </div>
            <div class="stat-badge">
                🔄 Active: <span class="stat-number" id="active_count">0</span>
            </div>
            <div class="stat-badge">
                📦 Archived: <span class="stat-number" id="archived_count">0</span>
            </div>
        </div>

        <!-- Task Cards -->
        <div class="tasks-grid" id="tasks_container"></div>

        <div class="last-update">
            Last update: <span id="last_update">Never</span>
        </div>
    </div>

    <script>
        let ws = null;
        let currentView = 'active';

        function switchView(view) {
            currentView = view;
            ['active', 'archive', 'all'].forEach(v => {
                document.getElementById('tab-' + v).classList.remove('active');
            });
            document.getElementById('tab-' + view).classList.add('active');
            // Reconnect websocket with new filter
            if (ws) {
                ws.close();
            }
            connect();
        }

        function connect() {
            ws = new WebSocket('ws://localhost:' + window.location.port + '/ws?view=' + currentView);
            ws.onopen = () => console.log('Connected');
            ws.onmessage = (event) => updateDashboard(JSON.parse(event.data));
            ws.onclose = () => setTimeout(connect, 1000);
        }

        function updateDashboard(data) {
            document.getElementById('last_update').textContent = new Date(data.timestamp).toLocaleTimeString();
            document.getElementById('total_tasks').textContent = data.total_tasks;
            document.getElementById('active_count').textContent = data.active_count;
            document.getElementById('archived_count').textContent = data.archived_count;

            const sys = data.system;
            document.getElementById('cpu').textContent = sys.cpu_percent + '%';
            document.getElementById('memory').textContent = sys.memory_percent + '%';
            document.getElementById('memory_detail').textContent = `${sys.memory_used_gb} GB / ${sys.memory_total_gb} GB`;
            document.getElementById('disk').textContent = sys.disk_percent + '%';
            document.getElementById('disk_detail').textContent = `${sys.disk_free_gb} GB free`;
            document.getElementById('uptime').textContent = `Uptime: ${Math.floor(sys.uptime_seconds / 60)}m`;
            document.getElementById('cpp_count').textContent = sys.cpp_processes.length;

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
                    <div class="detail-row">
                        <span>File Size:</span>
                        <span>${task.file_size_kb} KB</span>
                    </div>
                    <div class="detail-row">
                        <span>Lines:</span>
                        <span>${task.line_count.toLocaleString()}</span>
                    </div>
                    <div class="detail-row">
                        <span>Process:</span>
                        <span>${task.has_process ? '🟢 PID ' + task.process_pid : '⚪ Not running'}</span>
                    </div>
                    <div class="current-task">${task.current_task}</div>
                </div>
            `).join('');
        }

        connect();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard HTML"""
    return HTML_TEMPLATE


@app.get("/api/task/{task_id}")
async def get_task_details(task_id: str):
    """Get detailed task information from archive"""
    task = dashboard.archive_manager.get_task_by_id(task_id)
    if task:
        return JSONResponse(task)
    return JSONResponse({"error": "Task not found"}, status_code=404)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint with view filtering"""
    await websocket.accept()

    # Get view filter from query params
    view_filter = "active"  # Default
    try:
        query = str(websocket.url).split("?view=")
        if len(query) > 1:
            view_filter = query[1].split("&")[0]
    except:
        pass

    try:
        while True:
            metrics = await dashboard.get_all_metrics(view_filter)
            await websocket.send_json(metrics)
            await asyncio.sleep(UPDATE_INTERVAL)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    print(f"""
================================================================================
🔥 CPP Dashboard with Archive - Starting
================================================================================

Dashboard URL: http://localhost:{PORT}

Features:
  ✅ Active View: Currently running tasks only (default)
  ✅ Archive View: Completed tasks with full history
  ✅ All View: Everything together
  ✅ Auto-archiving: Tasks archived when completed
  ✅ System resources at top
  ✅ Real-time updates every 500ms

Press Ctrl+C to stop
================================================================================
    """)

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
