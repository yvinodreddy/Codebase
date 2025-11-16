#!/usr/bin/env python3
"""
Enhanced Real-Time Track Monitoring Dashboard with Agent Visibility

Provides world-class visibility with:
- Clickable track cards with drill-down details
- 25-agent allocation and task monitoring
- System prompt visualization
- Real-time error highlighting
- Live log streaming with filtering
- ULTRATHINK stage tracking

Usage:
    python3 dashboard_enhanced.py
    Then open http://localhost:8889 in browser
"""

import asyncio
import json
import os
import psutil
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


# Configuration
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"
TRACK_COUNT = 5
UPDATE_INTERVAL = 1.0  # seconds
PORT = 8889  # Different port to avoid conflict


class AgentInfo:
    """Individual agent information"""

    def __init__(self, agent_id: str, name: str, role: str, priority: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.priority = priority
        self.status = "READY"
        self.current_task = None
        self.progress = 0

    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "priority": self.priority,
            "status": self.status,
            "current_task": self.current_task,
            "progress": self.progress
        }


class EnhancedTrackMonitor:
    """Enhanced monitor with agent tracking and detailed analysis"""

    def __init__(self, track_id: int, output_file: Path):
        self.track_id = track_id
        self.output_file = output_file
        self.start_time = None
        self.last_size = 0
        self.last_line_count = 0
        self.status = "pending"
        self.current_task = "Initializing..."
        self.progress_percentage = 0
        self.errors = []
        self.warnings = []

        # Enhanced tracking
        self.agents: Dict[str, AgentInfo] = {}
        self.agent_count = 0
        self.system_prompt = None
        self.ultrathink_stage = None
        self.guardrail_status = {}
        self.context_usage = {"used": 0, "max": 200000}
        self.iteration_count = 0
        self.quality_score = 0.0

        # Full log cache (last 500 lines)
        self.log_lines = []

    def update(self) -> Dict:
        """Update track metrics with enhanced parsing"""
        if not self.output_file.exists():
            return self.get_metrics()

        # File size
        current_size = self.output_file.stat().st_size
        size_delta = current_size - self.last_size
        self.last_size = current_size

        # Read entire file for comprehensive parsing
        try:
            with open(self.output_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                current_line_count = len(lines)
                line_delta = current_line_count - self.last_line_count
                self.last_line_count = current_line_count

                # Keep last 500 lines for log viewing
                self.log_lines = lines[-500:] if len(lines) > 500 else lines

                # Parse different sections
                self._parse_agents(lines)
                self._parse_ultrathink_stage(lines)
                self._parse_guardrails(lines)
                self._parse_context_usage(lines)
                self._parse_system_prompt(lines)
                self._parse_current_task(lines[-50:])
                self._extract_errors_and_warnings(lines[-100:])

                # Check for completion
                recent = lines[-50:] if len(lines) > 50 else lines
                if any("COMPLETE" in line for line in recent):
                    self.status = "completed"
                    self.progress_percentage = 100
                elif any("ERROR" in line or "FAIL" in line for line in recent):
                    self.status = "error"
                elif self.status == "pending" and current_line_count > 100:
                    self.status = "running"

        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")

        # Estimate progress
        if self.status == "running":
            estimated_progress = min(95, (current_line_count / 5000) * 100)
            self.progress_percentage = estimated_progress

        return self.get_metrics()

    def _parse_agents(self, lines: List[str]):
        """Parse agent allocation from ULTRATHINK output"""
        in_agent_section = False

        for i, line in enumerate(lines):
            # Detect agent section
            if "DETAILED AGENT INFORMATION" in line or "Agent ID:" in line:
                in_agent_section = True

            # Parse agent count
            if "Agents to allocate:" in line or "Total Agents Allocated:" in line:
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    self.agent_count = int(match.group(1))

            # Parse individual agents
            if in_agent_section and "Agent ID:" in line:
                try:
                    # Extract agent ID
                    agent_id_match = re.search(r'Agent ID:\s*(\S+)', line)
                    if agent_id_match:
                        agent_id = agent_id_match.group(1)

                        # Look ahead for name, role, priority
                        name = "Unknown"
                        role = "Unknown"
                        priority = "MEDIUM"

                        # Check next few lines
                        for j in range(i+1, min(i+10, len(lines))):
                            next_line = lines[j]
                            if "Name:" in next_line:
                                name = next_line.split("Name:")[-1].strip()
                            elif "Role:" in next_line:
                                role = next_line.split("Role:")[-1].strip()
                            elif "Priority:" in next_line:
                                priority = next_line.split("Priority:")[-1].strip()

                        # Create or update agent
                        if agent_id not in self.agents:
                            self.agents[agent_id] = AgentInfo(agent_id, name, role, priority)

                except Exception:
                    pass

    def _parse_ultrathink_stage(self, lines: List[str]):
        """Parse current ULTRATHINK processing stage"""
        for line in reversed(lines[-100:]):
            if "[VERBOSE] STAGE" in line:
                match = re.search(r'STAGE\s*(\d+):\s*(.+)', line)
                if match:
                    stage_num = match.group(1)
                    stage_name = match.group(2).strip()
                    self.ultrathink_stage = f"Stage {stage_num}: {stage_name}"
                    break

    def _parse_guardrails(self, lines: List[str]):
        """Parse guardrail layer status"""
        for line in lines:
            if "Layer" in line and ("PASS" in line or "FAIL" in line):
                match = re.search(r'Layer\s*(\d+).*?(PASS|FAIL)', line)
                if match:
                    layer = f"Layer {match.group(1)}"
                    status = match.group(2)
                    self.guardrail_status[layer] = status

    def _parse_context_usage(self, lines: List[str]):
        """Parse context window usage"""
        for line in lines:
            if "Estimated usage" in line or "tokens" in line.lower():
                match = re.search(r'(\d+)[,\s]*tokens', line)
                if match:
                    self.context_usage["used"] = int(match.group(1))
                    break

    def _parse_system_prompt(self, lines: List[str]):
        """Extract the generated system prompt"""
        in_prompt_section = False
        prompt_lines = []

        for line in lines:
            if "ULTRATHINK PROMPT READY" in line or "enhanced with:" in line:
                in_prompt_section = True
            elif in_prompt_section:
                if line.strip().startswith("==="):
                    if prompt_lines:  # End of prompt section
                        break
                elif line.strip():
                    prompt_lines.append(line.strip())

        if prompt_lines:
            self.system_prompt = "\n".join(prompt_lines[:20])  # First 20 lines

    def _parse_current_task(self, lines: List[str]):
        """Extract current task from recent log lines - IMPROVED"""
        # Also update agent tasks while parsing
        for line in reversed(lines):
            line_clean = line.strip()

            # Pattern 1: [VERBOSE]   → Task description
            if "[VERBOSE]" in line and "→" in line:
                task = line.split("→")[-1].strip()
                if task and len(task) < 150 and task != "":
                    self.current_task = task
                    # Try to assign to relevant agent
                    self._update_agent_task_from_line(line, task)
                    if not task.endswith("..."):  # Don't return if it's incomplete
                        return

            # Pattern 2: [VERBOSE]   ✓ Completed task
            elif "[VERBOSE]" in line and "✓" in line:
                task = line.split("✓")[-1].strip()
                if task and len(task) < 150:
                    self.current_task = f"✓ {task}"
                    self._update_agent_task_from_line(line, task)
                    return

            # Pattern 3: STAGE X: Description
            elif "STAGE" in line and ":" in line and "[VERBOSE]" in line:
                match = re.search(r'STAGE\s*(\d+):\s*(.+)', line)
                if match:
                    stage_name = match.group(2).strip()
                    self.current_task = f"Stage {match.group(1)}: {stage_name}"
                    return

            # Pattern 4: Action keywords
            elif any(keyword in line for keyword in ["Implementing", "Creating", "Writing", "Analyzing", "Processing", "Validating", "Executing"]):
                self.current_task = line_clean[:120]
                self._update_agent_task_from_line(line, line_clean[:120])
                return

    def _update_agent_task_from_line(self, line: str, task: str):
        """Update agent tasks based on log line content"""
        # Map task patterns to agent types
        task_lower = task.lower()

        if "analyzing" in task_lower or "analysis" in task_lower:
            self._set_agent_task("A1", task, "EXECUTING")
            self._set_agent_task("A2", task, "EXECUTING")
        elif "guardrail" in task_lower or "layer" in task_lower:
            # Guardrail agents A7-A9, A19-A22
            for agent_id in ["A7", "A8", "A9", "A19", "A20", "A21", "A22"]:
                if agent_id in self.agents:
                    self._set_agent_task(agent_id, task, "EXECUTING")
        elif "context" in task_lower:
            self._set_agent_task("A3", task, "EXECUTING")
            self._set_agent_task("A4", task, "EXECUTING")
        elif "security" in task_lower or "validation" in task_lower:
            self._set_agent_task("A5", task, "EXECUTING")
            self._set_agent_task("A6", task, "EXECUTING")
        elif "executing" in task_lower or "implementing" in task_lower:
            # Task executors A10-A14
            for agent_id in ["A10", "A11", "A12", "A13", "A14"]:
                if agent_id in self.agents:
                    self._set_agent_task(agent_id, task, "EXECUTING")
        elif "verif" in task_lower or "quality" in task_lower:
            # Verifiers A15-A18, QA A23-A24
            for agent_id in ["A15", "A16", "A17", "A18", "A23", "A24"]:
                if agent_id in self.agents:
                    self._set_agent_task(agent_id, task, "EXECUTING")

    def _set_agent_task(self, agent_id: str, task: str, status: str):
        """Set agent's current task and status"""
        if agent_id in self.agents:
            self.agents[agent_id].current_task = task[:80]  # Keep it short
            self.agents[agent_id].status = status
            # Estimate progress based on task completion
            if "✓" in task or "completed" in task.lower():
                self.agents[agent_id].progress = 100
            elif status == "EXECUTING":
                self.agents[agent_id].progress = 50
            else:
                self.agents[agent_id].progress = 0

    def _extract_errors_and_warnings(self, lines: List[str]):
        """Extract errors and warnings"""
        for line in lines:
            if "ERROR" in line.upper() or "FAIL" in line.upper():
                error_text = line.strip()[:200]
                if error_text not in self.errors:
                    self.errors.append(error_text)
            elif "WARNING" in line.upper() or "WARN" in line.upper():
                warning_text = line.strip()[:200]
                if warning_text not in self.warnings:
                    self.warnings.append(warning_text)

        # Keep only last 10 errors/warnings
        self.errors = self.errors[-10:]
        self.warnings = self.warnings[-10:]

    def get_metrics(self) -> Dict:
        """Get comprehensive metrics as dict"""
        elapsed = 0
        if self.start_time:
            elapsed = time.time() - self.start_time

        return {
            "track_id": self.track_id,
            "status": self.status,
            "progress": round(self.progress_percentage, 1),
            "current_task": self.current_task,
            "file_size_kb": round(self.last_size / 1024, 1),
            "line_count": self.last_line_count,
            "elapsed_seconds": round(elapsed, 1),
            "errors": self.errors,
            "warnings": self.warnings,

            # Enhanced data
            "agent_count": len(self.agents),
            "agents": [agent.to_dict() for agent in self.agents.values()],
            "ultrathink_stage": self.ultrathink_stage,
            "guardrail_status": self.guardrail_status,
            "context_usage": self.context_usage,
            "system_prompt": self.system_prompt,
            "log_lines": self.log_lines[-100:]  # Last 100 lines for viewing
        }


class SystemMonitor:
    """Monitor system resource usage"""

    def __init__(self):
        self.process = psutil.Process()
        self.start_time = time.time()

    def get_metrics(self) -> Dict:
        """Get current system metrics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(SCRIPT_DIR))

        # Get cpp process info
        cpp_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if 'python' in proc.info['name'].lower() or 'cpp' in proc.info['name']:
                    cpp_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': round(proc.info['cpu_percent'], 1),
                        'memory': round(proc.info['memory_percent'], 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return {
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory.percent, 1),
            "memory_used_gb": round(memory.used / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "disk_percent": round(disk.percent, 1),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "active_processes": cpp_processes[:10]
        }


class DashboardManager:
    """Manage all monitoring and WebSocket connections"""

    def __init__(self):
        self.track_monitors: Dict[int, EnhancedTrackMonitor] = {}
        self.system_monitor = SystemMonitor()
        self.active_connections: List[WebSocket] = []
        self.running = False

    def initialize_tracks(self):
        """Discover and initialize track monitors"""
        pattern = "*track*_*.txt"
        track_files = list(TMP_DIR.glob(pattern))

        for track_file in track_files:
            filename = track_file.name
            if "track" in filename:
                try:
                    track_num = int(filename.split("track")[1].split("_")[0])
                    if track_num not in self.track_monitors:
                        self.track_monitors[track_num] = EnhancedTrackMonitor(track_num, track_file)
                        self.track_monitors[track_num].start_time = track_file.stat().st_mtime
                except (ValueError, IndexError):
                    pass

        # Ensure we have monitors for tracks 1-5
        for i in range(1, TRACK_COUNT + 1):
            if i not in self.track_monitors:
                possible_files = list(TMP_DIR.glob(f"*track{i}*.txt"))
                if possible_files:
                    self.track_monitors[i] = EnhancedTrackMonitor(i, possible_files[0])

    async def connect_websocket(self, websocket: WebSocket):
        """Add new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect_websocket(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_update(self, data: Dict):
        """Send update to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect_websocket(conn)

    async def monitoring_loop(self):
        """Main monitoring loop"""
        self.running = True

        while self.running:
            track_metrics = []
            for track_id in sorted(self.track_monitors.keys()):
                metrics = self.track_monitors[track_id].update()
                track_metrics.append(metrics)

            system_metrics = self.system_monitor.get_metrics()

            total_progress = sum(m['progress'] for m in track_metrics) / len(track_metrics) if track_metrics else 0
            completed_count = sum(1 for m in track_metrics if m['status'] == 'completed')
            running_count = sum(1 for m in track_metrics if m['status'] == 'running')
            error_count = sum(len(m['errors']) for m in track_metrics)

            update = {
                "timestamp": datetime.now().isoformat(),
                "tracks": track_metrics,
                "system": system_metrics,
                "summary": {
                    "total_progress": round(total_progress, 1),
                    "completed": completed_count,
                    "running": running_count,
                    "errors": error_count,
                    "total_tracks": len(track_metrics)
                }
            }

            await self.broadcast_update(update)
            await asyncio.sleep(UPDATE_INTERVAL)

    def get_current_state(self) -> Dict:
        """Get current state snapshot"""
        track_metrics = []
        for track_id in sorted(self.track_monitors.keys()):
            metrics = self.track_monitors[track_id].get_metrics()
            track_metrics.append(metrics)

        system_metrics = self.system_monitor.get_metrics()

        total_progress = sum(m['progress'] for m in track_metrics) / len(track_metrics) if track_metrics else 0
        completed_count = sum(1 for m in track_metrics if m['status'] == 'completed')
        running_count = sum(1 for m in track_metrics if m['status'] == 'running')
        error_count = sum(len(m['errors']) for m in track_metrics)

        return {
            "timestamp": datetime.now().isoformat(),
            "tracks": track_metrics,
            "system": system_metrics,
            "summary": {
                "total_progress": round(total_progress, 1),
                "completed": completed_count,
                "running": running_count,
                "errors": error_count,
                "total_tracks": len(track_metrics)
            }
        }


# Initialize FastAPI app
app = FastAPI(title="ULTRATHINK Enhanced Track Monitor", version="2.0.0")
dashboard = DashboardManager()


@app.on_event("startup")
async def startup_event():
    """Initialize dashboard on startup"""
    dashboard.initialize_tracks()
    asyncio.create_task(dashboard.monitoring_loop())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await dashboard.connect_websocket(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        dashboard.disconnect_websocket(websocket)


@app.get("/api/state")
async def get_state():
    """Get current state snapshot"""
    return dashboard.get_current_state()


@app.get("/api/track/{track_id}")
async def get_track_details(track_id: int):
    """Get detailed track information"""
    if track_id in dashboard.track_monitors:
        return dashboard.track_monitors[track_id].get_metrics()
    return {"error": "Track not found"}


@app.get("/api/logs/{track_id}")
async def get_track_logs(track_id: int, lines: int = 100):
    """Get recent log lines for a track"""
    if track_id in dashboard.track_monitors:
        monitor = dashboard.track_monitors[track_id]
        return {
            "track_id": track_id,
            "logs": monitor.log_lines[-lines:] if monitor.log_lines else []
        }
    return {"error": "Track not found"}


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve enhanced dashboard HTML"""
    # HTML content will be in the next part
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>ULTRATHINK Enhanced Monitor</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
            background: linear-gradient(90deg, #fff, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .connection-status {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-top: 10px;
        }

        .connected { background: rgba(34, 197, 94, 0.3); border: 2px solid #22c55e; }
        .disconnected { background: rgba(239, 68, 68, 0.3); border: 2px solid #ef4444; }

        /* Summary Cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .summary-card .value {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 10px 0;
        }

        .summary-card .label {
            font-size: 0.9rem;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Track Grid */
        .tracks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .track-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid rgba(255,255,255,0.2);
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        .track-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            border-color: rgba(255,255,255,0.5);
        }

        .track-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        }

        .track-card.completed::before { background: #22c55e; }
        .track-card.running::before { background: #eab308; }
        .track-card.error::before { background: #ef4444; }
        .track-card.pending::before { background: #3b82f6; }

        .track-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .track-title {
            font-size: 1.5rem;
            font-weight: bold;
        }

        .track-status {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-completed { background: rgba(34, 197, 94, 0.3); color: #22c55e; }
        .status-running { background: rgba(234, 179, 8, 0.3); color: #eab308; }
        .status-error { background: rgba(239, 68, 68, 0.3); color: #ef4444; }
        .status-pending { background: rgba(59, 130, 246, 0.3); color: #3b82f6; }

        .progress-container {
            margin: 15px 0;
        }

        .progress-bar {
            width: 100%;
            height: 25px;
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: bold;
        }

        .progress-fill.completed { background: linear-gradient(90deg, #22c55e, #16a34a); }
        .progress-fill.error { background: linear-gradient(90deg, #ef4444, #dc2626); }

        .track-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
            font-size: 0.9rem;
        }

        .stat-item {
            background: rgba(0,0,0,0.2);
            padding: 8px;
            border-radius: 8px;
        }

        .stat-label {
            opacity: 0.7;
            font-size: 0.8rem;
        }

        .stat-value {
            font-weight: bold;
            font-size: 1.1rem;
            margin-top: 3px;
        }

        .current-task {
            background: rgba(0,0,0,0.3);
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.85rem;
            font-style: italic;
            border-left: 3px solid #8b5cf6;
        }

        .click-hint {
            text-align: center;
            opacity: 0.6;
            font-size: 0.8rem;
            margin-top: 10px;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            overflow-y: auto;
        }

        .modal-content {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            margin: 2% auto;
            padding: 30px;
            border-radius: 20px;
            max-width: 1200px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: slideDown 0.3s ease;
        }

        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.2);
        }

        .modal-title {
            font-size: 2rem;
            font-weight: bold;
        }

        .close-btn {
            font-size: 2rem;
            font-weight: bold;
            color: #fff;
            cursor: pointer;
            background: none;
            border: none;
            padding: 0 10px;
            transition: transform 0.2s;
        }

        .close-btn:hover {
            transform: scale(1.2);
            color: #ef4444;
        }

        .modal-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }

        .tab-btn {
            padding: 12px 24px;
            background: transparent;
            border: none;
            color: #fff;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }

        .tab-btn:hover {
            background: rgba(255,255,255,0.1);
        }

        .tab-btn.active {
            border-bottom-color: #8b5cf6;
            background: rgba(139, 92, 246, 0.2);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Agent Grid */
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .agent-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }

        .agent-card:hover {
            background: rgba(255,255,255,0.15);
            transform: scale(1.05);
        }

        .agent-id {
            font-weight: bold;
            font-size: 1.1rem;
            color: #8b5cf6;
            margin-bottom: 8px;
        }

        .agent-name {
            font-size: 0.9rem;
            margin-bottom: 5px;
        }

        .agent-role {
            font-size: 0.8rem;
            opacity: 0.8;
            font-style: italic;
            margin-bottom: 8px;
        }

        .agent-priority {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
        }

        .priority-CRITICAL { background: #ef4444; }
        .priority-HIGH { background: #f59e0b; }
        .priority-MEDIUM { background: #3b82f6; }
        .priority-LOW { background: #6b7280; }

        /* Logs Viewer */
        .logs-container {
            background: #000;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            max-height: 500px;
            overflow-y: auto;
            border: 2px solid rgba(139, 92, 246, 0.5);
        }

        .log-line {
            padding: 3px 0;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .log-line.verbose { color: #a78bfa; }
        .log-line.error { color: #ef4444; font-weight: bold; }
        .log-line.warning { color: #eab308; }
        .log-line.success { color: #22c55e; }

        .system-prompt-box {
            background: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #8b5cf6;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .info-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #8b5cf6;
        }

        .info-label {
            font-size: 0.8rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .info-value {
            font-size: 1.2rem;
            font-weight: bold;
        }

        .error-list {
            background: rgba(239, 68, 68, 0.2);
            border: 2px solid #ef4444;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }

        .error-item {
            padding: 10px;
            margin: 5px 0;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
        }

        .warning-list {
            background: rgba(234, 179, 8, 0.2);
            border: 2px solid #eab308;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }

        .warning-item {
            padding: 10px;
            margin: 5px 0;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
        }

        /* System Resources */
        .resource-bars {
            margin: 20px 0;
        }

        .resource-item {
            margin: 15px 0;
        }

        .resource-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }

        .resource-bar {
            height: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            overflow: hidden;
        }

        .resource-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            transition: width 0.5s ease;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .tracks-grid {
                grid-template-columns: 1fr;
            }

            .agents-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }

            h1 {
                font-size: 2rem;
            }
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.2);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(139, 92, 246, 0.5);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(139, 92, 246, 0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 ULTRATHINK Enhanced Monitor</h1>
            <div class="subtitle">Real-Time Track & Agent Visibility</div>
            <div class="connection-status disconnected" id="connectionStatus">
                ⚠️ Connecting to server...
            </div>
        </header>

        <!-- Summary Section -->
        <div class="summary-grid" id="summaryGrid">
            <!-- Populated by JavaScript -->
        </div>

        <!-- Tracks Grid -->
        <div class="tracks-grid" id="tracksGrid">
            <!-- Populated by JavaScript -->
        </div>

        <!-- System Resources -->
        <div class="resource-bars" id="systemResources">
            <!-- Populated by JavaScript -->
        </div>
    </div>

    <!-- Track Detail Modal -->
    <div id="trackModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">Track Details</div>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>

            <div class="modal-tabs">
                <button class="tab-btn active" onclick="switchTab('overview')">Overview</button>
                <button class="tab-btn" onclick="switchTab('agents')">Agents</button>
                <button class="tab-btn" onclick="switchTab('logs')">Live Logs</button>
                <button class="tab-btn" onclick="switchTab('prompt')">System Prompt</button>
                <button class="tab-btn" onclick="switchTab('errors')">Errors & Warnings</button>
            </div>

            <div id="overview" class="tab-content active">
                <!-- Overview content -->
            </div>

            <div id="agents" class="tab-content">
                <!-- Agents grid -->
            </div>

            <div id="logs" class="tab-content">
                <!-- Logs viewer -->
            </div>

            <div id="prompt" class="tab-content">
                <!-- System prompt -->
            </div>

            <div id="errors" class="tab-content">
                <!-- Errors and warnings -->
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let currentTrackData = {};
        let reconnectInterval = null;

        // WebSocket connection
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.hostname}:8889/ws`;

            ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                console.log('WebSocket connected');
                document.getElementById('connectionStatus').className = 'connection-status connected';
                document.getElementById('connectionStatus').innerHTML = '✅ Connected';
                if (reconnectInterval) {
                    clearInterval(reconnectInterval);
                    reconnectInterval = null;
                }
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                document.getElementById('connectionStatus').className = 'connection-status disconnected';
                document.getElementById('connectionStatus').innerHTML = '⚠️ Reconnecting...';

                if (!reconnectInterval) {
                    reconnectInterval = setInterval(() => {
                        console.log('Attempting to reconnect...');
                        connectWebSocket();
                    }, 3000);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }

        // Update dashboard with new data
        function updateDashboard(data) {
            currentTrackData = data;

            // Update summary cards
            updateSummary(data.summary);

            // Update track cards
            updateTracks(data.tracks);

            // Update system resources
            updateSystemResources(data.system);
        }

        function updateSummary(summary) {
            const summaryHTML = `
                <div class="summary-card">
                    <div class="label">Overall Progress</div>
                    <div class="value">${summary.total_progress}%</div>
                </div>
                <div class="summary-card">
                    <div class="label">Completed</div>
                    <div class="value">${summary.completed} / ${summary.total_tracks}</div>
                </div>
                <div class="summary-card">
                    <div class="label">Running</div>
                    <div class="value" style="color: #eab308;">${summary.running}</div>
                </div>
                <div class="summary-card">
                    <div class="label">Errors</div>
                    <div class="value" style="color: ${summary.errors > 0 ? '#ef4444' : '#22c55e'};">${summary.errors}</div>
                </div>
            `;
            document.getElementById('summaryGrid').innerHTML = summaryHTML;
        }

        function updateTracks(tracks) {
            const tracksHTML = tracks.map(track => `
                <div class="track-card ${track.status}" onclick="openTrackDetails(${track.track_id})">
                    <div class="track-header">
                        <div class="track-title">Track ${track.track_id}</div>
                        <div class="track-status status-${track.status}">${track.status}</div>
                    </div>

                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress-fill ${track.status}" style="width: ${track.progress}%">
                                ${track.progress}%
                            </div>
                        </div>
                    </div>

                    <div class="track-stats">
                        <div class="stat-item">
                            <div class="stat-label">Lines</div>
                            <div class="stat-value">${track.line_count.toLocaleString()}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Size</div>
                            <div class="stat-value">${track.file_size_kb} KB</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Agents</div>
                            <div class="stat-value">${track.agent_count}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Elapsed</div>
                            <div class="stat-value">${formatTime(track.elapsed_seconds)}</div>
                        </div>
                    </div>

                    <div class="current-task">
                        📍 ${track.current_task}
                    </div>

                    <div class="click-hint">
                        👆 Click for detailed view
                    </div>
                </div>
            `).join('');

            document.getElementById('tracksGrid').innerHTML = tracksHTML;
        }

        function updateSystemResources(system) {
            const resourcesHTML = `
                <h3 style="margin-bottom: 15px;">System Resources</h3>
                <div class="resource-item">
                    <div class="resource-label">
                        <span>CPU Usage</span>
                        <span>${system.cpu_percent}%</span>
                    </div>
                    <div class="resource-bar">
                        <div class="resource-fill" style="width: ${system.cpu_percent}%"></div>
                    </div>
                </div>
                <div class="resource-item">
                    <div class="resource-label">
                        <span>Memory Usage</span>
                        <span>${system.memory_used_gb} / ${system.memory_total_gb} GB (${system.memory_percent}%)</span>
                    </div>
                    <div class="resource-bar">
                        <div class="resource-fill" style="width: ${system.memory_percent}%"></div>
                    </div>
                </div>
                <div class="resource-item">
                    <div class="resource-label">
                        <span>Disk Space</span>
                        <span>${system.disk_free_gb} GB free (${100 - system.disk_percent}% available)</span>
                    </div>
                    <div class="resource-bar">
                        <div class="resource-fill" style="width: ${system.disk_percent}%"></div>
                    </div>
                </div>
            `;
            document.getElementById('systemResources').innerHTML = resourcesHTML;
        }

        function openTrackDetails(trackId) {
            const track = currentTrackData.tracks.find(t => t.track_id === trackId);
            if (!track) return;

            document.getElementById('modalTitle').innerHTML = `🔥 Track ${trackId} - Detailed View`;

            // Populate overview tab
            document.getElementById('overview').innerHTML = generateOverviewHTML(track);

            // Populate agents tab
            document.getElementById('agents').innerHTML = generateAgentsHTML(track);

            // Populate logs tab
            document.getElementById('logs').innerHTML = generateLogsHTML(track);

            // Populate prompt tab
            document.getElementById('prompt').innerHTML = generatePromptHTML(track);

            // Populate errors tab
            document.getElementById('errors').innerHTML = generateErrorsHTML(track);

            document.getElementById('trackModal').style.display = 'block';
        }

        function generateOverviewHTML(track) {
            return `
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">Status</div>
                        <div class="info-value" style="color: ${getStatusColor(track.status)}">${track.status.toUpperCase()}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Progress</div>
                        <div class="info-value">${track.progress}%</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Agent Count</div>
                        <div class="info-value">${track.agent_count}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Line Count</div>
                        <div class="info-value">${track.line_count.toLocaleString()}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">File Size</div>
                        <div class="info-value">${track.file_size_kb} KB</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Elapsed Time</div>
                        <div class="info-value">${formatTime(track.elapsed_seconds)}</div>
                    </div>
                </div>

                <h3 style="margin: 20px 0 10px 0;">ULTRATHINK Stage</h3>
                <div class="info-card">
                    <div class="info-value" style="font-size: 1rem;">${track.ultrathink_stage || 'Not available'}</div>
                </div>

                <h3 style="margin: 20px 0 10px 0;">Current Task</h3>
                <div class="system-prompt-box" style="max-height: 100px;">
                    ${track.current_task}
                </div>

                <h3 style="margin: 20px 0 10px 0;">Context Usage</h3>
                <div class="resource-item">
                    <div class="resource-label">
                        <span>Tokens Used</span>
                        <span>${track.context_usage.used.toLocaleString()} / ${track.context_usage.max.toLocaleString()}</span>
                    </div>
                    <div class="resource-bar">
                        <div class="resource-fill" style="width: ${(track.context_usage.used / track.context_usage.max * 100).toFixed(1)}%"></div>
                    </div>
                </div>
            `;
        }

        function generateAgentsHTML(track) {
            if (!track.agents || track.agents.length === 0) {
                return '<p style="text-align: center; padding: 40px;">No agent data available yet. Agents will appear once ULTRATHINK processing begins.</p>';
            }

            const agentsHTML = track.agents.map(agent => `
                <div class="agent-card">
                    <div class="agent-id">${agent.agent_id}</div>
                    <div class="agent-name">${agent.name}</div>
                    <div class="agent-role">${agent.role}</div>
                    <div class="agent-priority priority-${agent.priority}">${agent.priority}</div>
                </div>
            `).join('');

            return `
                <h3 style="margin-bottom: 15px;">${track.agents.length} Agents Allocated</h3>
                <div class="agents-grid">
                    ${agentsHTML}
                </div>
            `;
        }

        function generateLogsHTML(track) {
            if (!track.log_lines || track.log_lines.length === 0) {
                return '<p style="text-align: center; padding: 40px;">No logs available yet.</p>';
            }

            const logsHTML = track.log_lines.map(line => {
                let className = 'log-line';
                if (line.includes('[VERBOSE]')) className += ' verbose';
                if (line.includes('ERROR') || line.includes('FAIL')) className += ' error';
                if (line.includes('WARNING') || line.includes('WARN')) className += ' warning';
                if (line.includes('✓') || line.includes('PASS')) className += ' success';

                return `<div class="${className}">${escapeHtml(line)}</div>`;
            }).join('');

            return `
                <h3 style="margin-bottom: 15px;">Live Log Stream (Last 100 lines)</h3>
                <div class="logs-container">
                    ${logsHTML}
                </div>
            `;
        }

        function generatePromptHTML(track) {
            if (!track.system_prompt) {
                return '<p style="text-align: center; padding: 40px;">System prompt not yet generated.</p>';
            }

            return `
                <h3 style="margin-bottom: 15px;">Generated System Prompt</h3>
                <div class="system-prompt-box">
${escapeHtml(track.system_prompt)}
                </div>
            `;
        }

        function generateErrorsHTML(track) {
            let html = '';

            if (track.errors && track.errors.length > 0) {
                html += '<h3 style="margin-bottom: 15px;">❌ Errors</h3>';
                html += '<div class="error-list">';
                track.errors.forEach(error => {
                    html += `<div class="error-item">${escapeHtml(error)}</div>`;
                });
                html += '</div>';
            } else {
                html += '<p style="color: #22c55e; text-align: center; padding: 20px;">✅ No errors detected!</p>';
            }

            if (track.warnings && track.warnings.length > 0) {
                html += '<h3 style="margin: 20px 0 15px 0;">⚠️ Warnings</h3>';
                html += '<div class="warning-list">';
                track.warnings.forEach(warning => {
                    html += `<div class="warning-item">${escapeHtml(warning)}</div>`;
                });
                html += '</div>';
            }

            return html || '<p style="text-align: center; padding: 40px;">No errors or warnings.</p>';
        }

        function closeModal() {
            document.getElementById('trackModal').style.display = 'none';
        }

        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);

            if (hours > 0) {
                return `${hours}h ${minutes}m`;
            } else if (minutes > 0) {
                return `${minutes}m ${secs}s`;
            } else {
                return `${secs}s`;
            }
        }

        function getStatusColor(status) {
            switch(status) {
                case 'completed': return '#22c55e';
                case 'running': return '#eab308';
                case 'error': return '#ef4444';
                case 'pending': return '#3b82f6';
                default: return '#fff';
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('trackModal');
            if (event.target == modal) {
                closeModal();
            }
        }

        // Initialize
        connectWebSocket();

        // Fetch initial state
        fetch('/api/state')
            .then(response => response.json())
            .then(data => updateDashboard(data))
            .catch(error => console.error('Error fetching initial state:', error));
    </script>
</body>
</html>
"""
    return html_content


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔥 ULTRATHINK ENHANCED DASHBOARD SERVER")
    print("="*80)
    print(f"\nMonitoring tracks from: {TMP_DIR}")
    print(f"Server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop\n")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
