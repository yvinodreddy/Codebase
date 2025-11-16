#!/usr/bin/env python3
"""
FastAPI WebSocket Server for ULTRATHINK Real-Time Tracking
Provides real-time updates via WebSocket and REST API endpoints

ZERO BREAKING CHANGES:
- New file in new directory (realtime-tracking/)
- Runs on separate port (8000) - no conflicts
- Optional feature - existing system continues to work without this
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Set
from pathlib import Path
import os
import psutil  # System monitoring

# Configuration
DB_PATH = "realtime-tracking/track_state.db"
LOG_DIR = "logs"
UPDATE_INTERVAL = 2  # seconds

app = FastAPI(
    title="ULTRATHINK Real-Time Tracker",
    description="Real-time WebSocket tracking for 10-track parallel execution",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from web-dashboard
if Path("web-dashboard/static").exists():
    app.mount("/static", StaticFiles(directory="web-dashboard/static"), name="static")


class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        """Accept and register new WebSocket connection"""
        await websocket.accept()
        async with self.lock:
            self.active_connections.add(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected. Total: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        async with self.lock:
            self.active_connections.discard(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return

        async with self.lock:
            disconnected = set()
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error sending to client: {e}")
                    disconnected.add(connection)

            # Remove disconnected clients
            self.active_connections -= disconnected


manager = ConnectionManager()


def get_db_connection():
    """Get database connection with optimized settings"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup"""
    print(f"\n{'='*80}")
    print(f"🚀 ULTRATHINK Real-Time Tracker Starting...")
    print(f"{'='*80}")
    print(f"   - Database: {DB_PATH}")
    print(f"   - Update interval: {UPDATE_INTERVAL} seconds")
    print(f"   - Log directory: {LOG_DIR}")
    print(f"{'='*80}\n")

    # Verify database exists
    if not Path(DB_PATH).exists():
        print(f"⚠️  Warning: Database not found at {DB_PATH}")
        print(f"   Run: python3 realtime-tracking/setup_database.py")

    # Create logs directory if it doesn't exist
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    # Start periodic state broadcast
    asyncio.create_task(periodic_state_broadcast())


async def periodic_state_broadcast():
    """Broadcast track state every 2 seconds"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting periodic state broadcast...")

    while True:
        try:
            if not manager.active_connections:
                await asyncio.sleep(UPDATE_INTERVAL)
                continue

            conn = get_db_connection()
            cursor = conn.cursor()

            # Get all track states
            cursor.execute("""
                SELECT id, name, status, progress, current_task, last_update
                FROM tracks
                ORDER BY id
            """)
            tracks = cursor.fetchall()

            # Calculate overall progress
            if tracks:
                overall_progress = sum(t['progress'] for t in tracks) / len(tracks)
                running_count = sum(1 for t in tracks if t['status'] == 'RUNNING')
                completed_count = sum(1 for t in tracks if t['status'] == 'COMPLETED')
                failed_count = sum(1 for t in tracks if t['status'] == 'FAILED')
            else:
                overall_progress = 0
                running_count = completed_count = failed_count = 0

            # Broadcast overall state
            await manager.broadcast({
                'type': 'overall_update',
                'overall_progress': round(overall_progress, 1),
                'running': running_count,
                'completed': completed_count,
                'failed': failed_count,
                'total': len(tracks),
                'timestamp': datetime.now().isoformat()
            })

            # Broadcast individual track updates
            for track in tracks:
                await manager.broadcast({
                    'type': 'track_update',
                    'track_id': track['id'],
                    'name': track['name'],
                    'status': track['status'],
                    'progress': track['progress'],
                    'current_task': track['current_task'] or 'Waiting...',
                    'last_update': track['last_update'],
                    'timestamp': datetime.now().isoformat()
                })

            conn.close()

            # ULTRATHINK ENHANCEMENT: Also broadcast ULTRATHINK updates (additive)
            await broadcast_ultrathink_updates()

            # ZERO BREAKING CHANGE: Broadcast recent logs (additive)
            await broadcast_recent_logs()

            # SYSTEM MONITORING: Broadcast system metrics (additive)
            await broadcast_system_monitor()

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in periodic broadcast: {e}")

        await asyncio.sleep(UPDATE_INTERVAL)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()

            # Echo back acknowledgment
            await websocket.send_json({
                'type': 'ack',
                'message': f'Received: {data}',
                'timestamp': datetime.now().isoformat()
            })

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] WebSocket error: {e}")
        await manager.disconnect(websocket)


@app.get("/")
async def root():
    """Serve main dashboard page"""
    dashboard_file = Path("web-dashboard/index.html")
    if dashboard_file.exists():
        return FileResponse(dashboard_file)
    return HTMLResponse("""
    <html>
        <head><title>ULTRATHINK Real-Time Tracker</title></head>
        <body>
            <h1>ULTRATHINK Real-Time Tracker</h1>
            <p>Dashboard not found. Create web-dashboard/index.html</p>
            <p>API available at: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """)


@app.get("/dashboard.html")
async def dashboard():
    """Serve enhanced dashboard page"""
    dashboard_file = Path("web-dashboard/dashboard.html")
    if dashboard_file.exists():
        return FileResponse(dashboard_file)
    # Fallback to index.html
    index_file = Path("web-dashboard/index.html")
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>Dashboard not found</h1>")


@app.get("/v2")
async def dashboard_v2():
    """Serve dashboard v2.0 - Production-ready with all features"""
    dashboard_file = Path("web-dashboard/dashboard_v2.html")
    if dashboard_file.exists():
        return FileResponse(dashboard_file)
    return HTMLResponse("<h1>Dashboard v2 not found</h1>")


@app.get("/api/tracks")
async def get_tracks():
    """Get all track states"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tracks ORDER BY id")
        tracks = cursor.fetchall()
        conn.close()

        return {
            'success': True,
            'tracks': [dict(t) for t in tracks],
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@app.get("/api/tracks/{track_id}")
async def get_track(track_id: int):
    """Get specific track state"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tracks WHERE id = ?", (track_id,))
        track = cursor.fetchone()
        conn.close()

        if track:
            return {
                'success': True,
                'track': dict(track),
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'error': f'Track {track_id} not found',
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@app.get("/api/tracks/{track_id}/logs")
async def get_track_logs(track_id: int, limit: int = 100):
    """Get recent log entries for a track"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, level, message
            FROM log_entries
            WHERE track_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (track_id, limit))
        logs = cursor.fetchall()
        conn.close()

        return {
            'success': True,
            'track_id': track_id,
            'logs': [dict(log) for log in logs],
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@app.get("/api/status")
async def get_status():
    """Get overall system status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM tracks")
        total = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as running FROM tracks WHERE status = 'RUNNING'")
        running = cursor.fetchone()['running']

        cursor.execute("SELECT COUNT(*) as completed FROM tracks WHERE status = 'COMPLETED'")
        completed = cursor.fetchone()['completed']

        cursor.execute("SELECT COUNT(*) as failed FROM tracks WHERE status = 'FAILED'")
        failed = cursor.fetchone()['failed']

        cursor.execute("SELECT AVG(progress) as avg_progress FROM tracks")
        avg_progress = cursor.fetchone()['avg_progress'] or 0

        conn.close()

        return {
            'success': True,
            'status': {
                'total_tracks': total,
                'running': running,
                'completed': completed,
                'failed': failed,
                'pending': total - running - completed - failed,
                'overall_progress': round(avg_progress, 1),
                'active_connections': len(manager.active_connections)
            },
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_exists = Path(DB_PATH).exists()
    return {
        'status': 'healthy' if db_exists else 'degraded',
        'database': 'connected' if db_exists else 'not_found',
        'active_connections': len(manager.active_connections),
        'timestamp': datetime.now().isoformat()
    }


@app.get("/api/system/monitor")
async def get_system_monitor():
    """Get system monitoring metrics (CPU, RAM, Memory, Process)"""
    try:
        # Get current process info
        current_process = psutil.Process()

        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # Memory metrics
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Process-specific metrics
        process_memory = current_process.memory_info()
        process_cpu = current_process.cpu_percent()
        process_threads = current_process.num_threads()

        # Disk metrics
        disk = psutil.disk_usage('/')

        return {
            'success': True,
            'system': {
                'cpu': {
                    'percent': round(cpu_percent, 1),
                    'count': cpu_count,
                    'frequency': round(cpu_freq.current, 1) if cpu_freq else 0
                },
                'memory': {
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2),
                    'percent': round(memory.percent, 1),
                    'swap_used_gb': round(swap.used / (1024**3), 2),
                    'swap_percent': round(swap.percent, 1)
                },
                'disk': {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'percent': round(disk.percent, 1)
                }
            },
            'process': {
                'cpu_percent': round(process_cpu, 1),
                'memory_mb': round(process_memory.rss / (1024**2), 2),
                'threads': process_threads,
                'pid': current_process.pid
            },
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


# ============================================================================
# ULTRATHINK ENHANCEMENTS (Zero Breaking Changes - Additive Only)
# ============================================================================

@app.get("/api/tracks/{track_id}/ultrathink")
async def get_ultrathink_details(track_id: int):
    """Get ULTRATHINK details for a track (agents, stages, guardrails)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ultrathink_details WHERE track_id = ?", (track_id,))
        details = cursor.fetchone()
        conn.close()

        if details:
            result = dict(details)
            # Parse JSON fields
            if result.get('agents_data'):
                try:
                    result['agents'] = json.loads(result['agents_data'])
                except Exception:
                    result['agents'] = []
            if result.get('guardrails_status'):
                try:
                    result['guardrails'] = json.loads(result['guardrails_status'])
                except Exception:
                    result['guardrails'] = []
            if result.get('metrics_data'):
                try:
                    result['metrics'] = json.loads(result['metrics_data'])
                except Exception:
                    result['metrics'] = {}

            return {'success': True, 'track_id': track_id, 'ultrathink': result, 'timestamp': datetime.now().isoformat()}
        else:
            return {'success': False, 'error': f'No ULTRATHINK details for track {track_id}', 'timestamp': datetime.now().isoformat()}
    except Exception as e:
        return {'success': False, 'error': str(e), 'timestamp': datetime.now().isoformat()}


async def broadcast_ultrathink_updates():
    """Broadcast ULTRATHINK details for all active tracks"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ud.*, t.status FROM ultrathink_details ud
            JOIN tracks t ON ud.track_id = t.id
            WHERE t.status IN ('RUNNING', 'COMPLETED')
            ORDER BY ud.updated_at DESC LIMIT 10
        """)
        details = cursor.fetchall()

        for detail in details:
            agents_data = json.loads(detail['agents_data']) if detail['agents_data'] else []
            guardrails_data = json.loads(detail['guardrails_status']) if detail['guardrails_status'] else []
            metrics_data = json.loads(detail['metrics_data']) if detail['metrics_data'] else {}

            await manager.broadcast({
                'type': 'ultrathink_update',
                'track_id': detail['track_id'],
                'current_stage': detail['current_stage'],
                'stage_number': detail['current_stage_number'],
                'total_stages': detail['total_stages'],
                'agents': agents_data,
                'guardrails': guardrails_data,
                'metrics': metrics_data,
                'timestamp': datetime.now().isoformat()
            })

        conn.close()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error broadcasting ULTRATHINK: {e}")


async def broadcast_recent_logs():
    """Broadcast recent log entries (last 50) for live log streaming"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get recent logs from all tracks
        cursor.execute("""
            SELECT
                le.id,
                le.track_id,
                le.timestamp,
                le.level,
                le.message,
                t.name as track_name
            FROM log_entries le
            JOIN tracks t ON le.track_id = t.id
            ORDER BY le.timestamp DESC
            LIMIT 50
        """)
        logs = cursor.fetchall()

        # Broadcast logs as individual log_update messages
        for log in logs:
            await manager.broadcast({
                'type': 'log_update',
                'log_id': log['id'],
                'track_id': log['track_id'],
                'track_name': log['track_name'],
                'timestamp': log['timestamp'],
                'level': log['level'],
                'message': log['message']
            })

        conn.close()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error broadcasting logs: {e}")


async def broadcast_system_monitor():
    """Broadcast system monitoring metrics (CPU, RAM, Memory, Process)"""
    try:
        # Get current process info
        current_process = psutil.Process()

        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Memory metrics
        memory = psutil.virtual_memory()

        # Process-specific metrics
        process_memory = current_process.memory_info()
        process_cpu = current_process.cpu_percent()

        # Broadcast system monitor update
        await manager.broadcast({
            'type': 'system_monitor_update',
            'cpu_percent': round(cpu_percent, 1),
            'memory_percent': round(memory.percent, 1),
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'memory_total_gb': round(memory.total / (1024**3), 2),
            'process_cpu_percent': round(process_cpu, 1),
            'process_memory_mb': round(process_memory.rss / (1024**2), 2),
            'process_threads': current_process.num_threads(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error broadcasting system monitor: {e}")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("Starting ULTRATHINK Real-Time Tracker Server")
    print("="*80)
    print("Dashboard: http://localhost:8000")
    print("API Docs:  http://localhost:8000/docs")
    print("WebSocket: ws://localhost:8000/ws")
    print("="*80 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
