#!/usr/bin/env python3
"""
Real-Time Track Monitoring Dashboard Server

Provides live monitoring of parallel track execution with:
- Real-time progress updates via WebSocket
- Resource usage monitoring (CPU, RAM, disk)
- Task execution tracking
- Live log streaming
- Interactive web UI with graphs

Usage:
    python3 dashboard_server.py
    Then open http://localhost:8888 in browser
"""

import asyncio
import json
import os
import psutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


# Configuration
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"
TRACK_COUNT = 5
UPDATE_INTERVAL = 1.0  # seconds


class TrackMonitor:
    """Monitor individual track execution"""

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

    def update(self) -> Dict:
        """Update track metrics"""
        if not self.output_file.exists():
            return self.get_metrics()

        # File size
        current_size = self.output_file.stat().st_size
        size_delta = current_size - self.last_size
        self.last_size = current_size

        # Line count
        with open(self.output_file, 'r') as f:
            lines = f.readlines()
            current_line_count = len(lines)
            line_delta = current_line_count - self.last_line_count
            self.last_line_count = current_line_count

            # Parse current task from last 50 lines
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            self._parse_current_task(recent_lines)

            # Check for completion
            if any("COMPLETE" in line for line in recent_lines):
                self.status = "completed"
                self.progress_percentage = 100
            elif any("ERROR" in line or "FAIL" in line for line in recent_lines):
                self.status = "error"
                self._extract_errors(recent_lines)
            elif self.status == "pending" and current_line_count > 100:
                self.status = "running"

        # Estimate progress (based on typical output size)
        if self.status == "running":
            # Typical complete output: ~5000 lines
            estimated_progress = min(95, (current_line_count / 5000) * 100)
            self.progress_percentage = estimated_progress

        return self.get_metrics()

    def _parse_current_task(self, lines: List[str]):
        """Extract current task from recent log lines"""
        for line in reversed(lines):
            if "[VERBOSE]" in line and "→" in line:
                # Extract task description
                task = line.split("→")[-1].strip()
                if task and len(task) < 100:
                    self.current_task = task
                    return
            elif "Implementing" in line or "Creating" in line or "Writing" in line:
                self.current_task = line.strip()[:80]
                return

    def _extract_errors(self, lines: List[str]):
        """Extract error messages"""
        for line in lines:
            if "ERROR" in line or "FAIL" in line:
                self.errors.append(line.strip()[:200])
        # Keep only last 5 errors
        self.errors = self.errors[-5:]

    def get_metrics(self) -> Dict:
        """Get current metrics as dict"""
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
            "errors": self.errors
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
            "active_processes": cpp_processes[:10]  # Top 10
        }


class DashboardManager:
    """Manage all monitoring and WebSocket connections"""

    def __init__(self):
        self.track_monitors: Dict[int, TrackMonitor] = {}
        self.system_monitor = SystemMonitor()
        self.active_connections: List[WebSocket] = []
        self.running = False

    def initialize_tracks(self):
        """Discover and initialize track monitors"""
        # Find all track output files
        pattern = "*track*_*.txt"
        track_files = list(TMP_DIR.glob(pattern))

        # Create monitors for discovered tracks
        for track_file in track_files:
            # Extract track number from filename
            filename = track_file.name
            if "track" in filename:
                try:
                    track_num = int(filename.split("track")[1].split("_")[0])
                    if track_num not in self.track_monitors:
                        self.track_monitors[track_num] = TrackMonitor(track_num, track_file)
                        self.track_monitors[track_num].start_time = track_file.stat().st_mtime
                except (ValueError, IndexError):
                    pass

        # Ensure we have monitors for tracks 1-5
        for i in range(1, TRACK_COUNT + 1):
            if i not in self.track_monitors:
                # Find any file matching track
                possible_files = list(TMP_DIR.glob(f"*track{i}*.txt"))
                if possible_files:
                    self.track_monitors[i] = TrackMonitor(i, possible_files[0])

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

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect_websocket(conn)

    async def monitoring_loop(self):
        """Main monitoring loop"""
        self.running = True

        while self.running:
            # Update all tracks
            track_metrics = []
            for track_id in sorted(self.track_monitors.keys()):
                metrics = self.track_monitors[track_id].update()
                track_metrics.append(metrics)

            # Update system metrics
            system_metrics = self.system_monitor.get_metrics()

            # Aggregate stats
            total_progress = sum(m['progress'] for m in track_metrics) / len(track_metrics) if track_metrics else 0
            completed_count = sum(1 for m in track_metrics if m['status'] == 'completed')
            running_count = sum(1 for m in track_metrics if m['status'] == 'running')
            error_count = sum(len(m['errors']) for m in track_metrics)

            # Prepare update payload
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

            # Broadcast to all clients
            await self.broadcast_update(update)

            # Sleep until next update
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
app = FastAPI(title="ULTRATHINK Track Monitor", version="1.0.0")
dashboard = DashboardManager()


@app.on_event("startup")
async def startup_event():
    """Initialize dashboard on startup"""
    dashboard.initialize_tracks()
    # Start monitoring loop
    asyncio.create_task(dashboard.monitoring_loop())


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve dashboard HTML"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>ULTRATHINK Track Monitor</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .card-title {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .card-value {
            font-size: 2.5rem;
            font-weight: bold;
        }

        .card-subtitle {
            font-size: 0.9rem;
            opacity: 0.7;
            margin-top: 5px;
        }

        .tracks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .track-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .track-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .track-title {
            font-size: 1.3rem;
            font-weight: bold;
        }

        .status-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-pending { background: #6c757d; }
        .status-running { background: #007bff; }
        .status-completed { background: #28a745; }
        .status-error { background: #dc3545; }

        .progress-bar-container {
            width: 100%;
            height: 30px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 15px;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .track-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }

        .stat {
            font-size: 0.9rem;
        }

        .stat-label {
            opacity: 0.7;
        }

        .stat-value {
            font-weight: bold;
            font-size: 1.1rem;
        }

        .current-task {
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9rem;
            margin-top: 10px;
        }

        .system-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .system-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .metric {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
        }

        .metric-label {
            font-size: 0.9rem;
            opacity: 0.7;
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
        }

        .connection-status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .status-connected { background: #28a745; }
        .status-disconnected { background: #dc3545; animation: none; }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="connection-status">
        <div class="status-indicator status-disconnected" id="status-indicator"></div>
        <span id="connection-text">Connecting...</span>
    </div>

    <div class="container">
        <header>
            <h1>🔥 ULTRATHINK Track Monitor</h1>
            <p class="subtitle">Real-Time Parallel Execution Dashboard</p>
        </header>

        <div class="summary-cards">
            <div class="card">
                <div class="card-title">Overall Progress</div>
                <div class="card-value" id="overall-progress">0%</div>
                <div class="card-subtitle">All tracks combined</div>
            </div>
            <div class="card">
                <div class="card-title">Completed</div>
                <div class="card-value" id="completed-count">0</div>
                <div class="card-subtitle">Tracks finished</div>
            </div>
            <div class="card">
                <div class="card-title">Running</div>
                <div class="card-value" id="running-count">0</div>
                <div class="card-subtitle">Tracks active</div>
            </div>
            <div class="card">
                <div class="card-title">Errors</div>
                <div class="card-value" id="error-count">0</div>
                <div class="card-subtitle">Issues detected</div>
            </div>
        </div>

        <div class="tracks-grid" id="tracks-container">
            <!-- Track cards will be inserted here -->
        </div>

        <div class="system-card">
            <h2 style="margin-bottom: 20px;">📊 System Resources</h2>
            <div class="system-metrics" id="system-metrics">
                <!-- System metrics will be inserted here -->
            </div>
        </div>
    </div>

    <script>
        let ws;
        let reconnectInterval;

        function connect() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);

            ws.onopen = () => {
                console.log('WebSocket connected');
                document.getElementById('status-indicator').className = 'status-indicator status-connected';
                document.getElementById('connection-text').textContent = 'Connected';
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
                document.getElementById('status-indicator').className = 'status-indicator status-disconnected';
                document.getElementById('connection-text').textContent = 'Disconnected';

                // Attempt to reconnect
                if (!reconnectInterval) {
                    reconnectInterval = setInterval(() => {
                        connect();
                    }, 3000);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }

        function updateDashboard(data) {
            // Update summary cards
            document.getElementById('overall-progress').textContent = data.summary.total_progress + '%';
            document.getElementById('completed-count').textContent = data.summary.completed;
            document.getElementById('running-count').textContent = data.summary.running;
            document.getElementById('error-count').textContent = data.summary.errors;

            // Update track cards
            const tracksContainer = document.getElementById('tracks-container');
            tracksContainer.innerHTML = '';

            data.tracks.forEach(track => {
                const card = document.createElement('div');
                card.className = 'track-card';
                card.innerHTML = `
                    <div class="track-header">
                        <div class="track-title">Track ${track.track_id}</div>
                        <div class="status-badge status-${track.status}">${track.status}</div>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${track.progress}%">
                            ${track.progress}%
                        </div>
                    </div>
                    <div class="track-stats">
                        <div class="stat">
                            <div class="stat-label">File Size</div>
                            <div class="stat-value">${track.file_size_kb} KB</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Lines</div>
                            <div class="stat-value">${track.line_count}</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Elapsed</div>
                            <div class="stat-value">${Math.floor(track.elapsed_seconds / 60)}m ${Math.floor(track.elapsed_seconds % 60)}s</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Status</div>
                            <div class="stat-value">${track.status}</div>
                        </div>
                    </div>
                    <div class="current-task">
                        <strong>Current:</strong> ${track.current_task}
                    </div>
                `;
                tracksContainer.appendChild(card);
            });

            // Update system metrics
            const systemContainer = document.getElementById('system-metrics');
            systemContainer.innerHTML = `
                <div class="metric">
                    <div class="metric-label">CPU Usage</div>
                    <div class="metric-value">${data.system.cpu_percent}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Memory Usage</div>
                    <div class="metric-value">${data.system.memory_percent}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Memory Used</div>
                    <div class="metric-value">${data.system.memory_used_gb} GB</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Disk Free</div>
                    <div class="metric-value">${data.system.disk_free_gb} GB</div>
                </div>
            `;
        }

        // Connect on load
        connect();
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await dashboard.connect_websocket(websocket)

    try:
        # Send initial state
        initial_state = dashboard.get_current_state()
        await websocket.send_json(initial_state)

        # Keep connection alive
        while True:
            # Wait for messages (keep-alive)
            await websocket.receive_text()
    except WebSocketDisconnect:
        dashboard.disconnect_websocket(websocket)


@app.get("/api/state")
async def get_state():
    """Get current state as JSON"""
    return dashboard.get_current_state()


@app.get("/api/track/{track_id}")
async def get_track(track_id: int):
    """Get specific track details"""
    if track_id in dashboard.track_monitors:
        return dashboard.track_monitors[track_id].get_metrics()
    return {"error": "Track not found"}


@app.get("/api/logs/{track_id}")
async def get_logs(track_id: int, lines: int = 100):
    """Get recent log lines from track"""
    if track_id in dashboard.track_monitors:
        track = dashboard.track_monitors[track_id]
        if track.output_file.exists():
            with open(track.output_file, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                return {"track_id": track_id, "lines": recent_lines}
    return {"error": "Track not found or no logs available"}


if __name__ == "__main__":
    print("=" * 80)
    print("🔥 ULTRATHINK Real-Time Dashboard Server")
    print("=" * 80)
    print("")
    print("Starting server...")
    print("")
    print("📊 Dashboard URL: http://localhost:8888")
    print("🔌 WebSocket URL: ws://localhost:8888/ws")
    print("📡 API URL: http://localhost:8888/api/state")
    print("")
    print("=" * 80)
    print("")

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
