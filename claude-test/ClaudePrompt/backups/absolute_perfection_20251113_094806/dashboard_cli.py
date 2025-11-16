#!/usr/bin/env python3
"""
CLI Dashboard for Track Monitoring

Real-time terminal dashboard using rich library with:
- Live progress bars
- Resource monitoring
- Task tracking
- Auto-refresh

Usage:
    python3 dashboard_cli.py
"""

import time
from pathlib import Path
from datetime import datetime
import psutil

try:
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    print("Installing required package: rich")
    import subprocess
    subprocess.check_call(["pip3", "install", "-q", "rich"])
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.text import Text


# Configuration
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"
REFRESH_RATE = 1.0  # seconds


class TrackInfo:
    """Track information"""
    def __init__(self, track_id: int, output_file: Path):
        self.track_id = track_id
        self.output_file = output_file
        self.line_count = 0
        self.file_size = 0
        self.status = "pending"
        self.progress = 0
        self.current_task = "Waiting..."
        self.start_time = output_file.stat().st_mtime if output_file.exists() else time.time()

    def update(self):
        """Update track metrics"""
        if not self.output_file.exists():
            return

        # File stats
        self.file_size = self.output_file.stat().st_size

        # Read file
        with open(self.output_file, 'r') as f:
            lines = f.readlines()
            self.line_count = len(lines)

            # Check status
            recent = lines[-50:] if len(lines) > 50 else lines
            if any("COMPLETE" in line for line in recent):
                self.status = "completed"
                self.progress = 100
            elif any("ERROR" in line for line in recent):
                self.status = "error"
            elif self.line_count > 100:
                self.status = "running"

                # Estimate progress (typical: 5000 lines)
                self.progress = min(95, (self.line_count / 5000) * 100)

            # Extract current task
            for line in reversed(recent):
                if "[VERBOSE]" in line and "→" in line:
                    task = line.split("→")[-1].strip()
                    if task and len(task) < 80:
                        self.current_task = task
                        break


def find_tracks():
    """Find all track output files"""
    tracks = {}
    for i in range(1, 6):
        pattern = f"*track{i}*.txt"
        files = list(TMP_DIR.glob(pattern))
        if files:
            # Use most recent file
            latest = max(files, key=lambda f: f.stat().st_mtime)
            tracks[i] = TrackInfo(i, latest)
    return tracks


def get_system_metrics():
    """Get system resource usage"""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(str(SCRIPT_DIR))

    return {
        "cpu": cpu,
        "memory_percent": mem.percent,
        "memory_used_gb": mem.used / (1024**3),
        "memory_total_gb": mem.total / (1024**3),
        "disk_percent": disk.percent,
        "disk_free_gb": disk.free / (1024**3)
    }


def create_dashboard_layout(tracks, system_metrics):
    """Create rich dashboard layout"""
    console = Console()

    # Header
    header = Panel(
        Text("🔥 ULTRATHINK Track Monitor", justify="center", style="bold cyan"),
        subtitle=f"Updated: {datetime.now().strftime('%H:%M:%S')}",
        style="bold white on blue"
    )

    # Summary stats
    completed = sum(1 for t in tracks.values() if t.status == "completed")
    running = sum(1 for t in tracks.values() if t.status == "running")
    total_progress = sum(t.progress for t in tracks.values()) / len(tracks) if tracks else 0

    summary_table = Table(show_header=False, box=None, expand=True)
    summary_table.add_column(justify="center", style="cyan")
    summary_table.add_column(justify="center", style="cyan")
    summary_table.add_column(justify="center", style="cyan")
    summary_table.add_column(justify="center", style="cyan")

    summary_table.add_row(
        f"[bold]Overall Progress[/bold]\n[green]{total_progress:.1f}%[/green]",
        f"[bold]Completed[/bold]\n[green]{completed}[/green] / {len(tracks)}",
        f"[bold]Running[/bold]\n[yellow]{running}[/yellow]",
        f"[bold]Pending[/bold]\n[blue]{len(tracks) - completed - running}[/blue]"
    )

    summary = Panel(summary_table, title="Summary", style="bold white")

    # Track details
    tracks_table = Table(title="Track Details", expand=True)
    tracks_table.add_column("Track", justify="center", style="cyan", width=8)
    tracks_table.add_column("Status", justify="center", width=12)
    tracks_table.add_column("Progress", justify="left", width=25)
    tracks_table.add_column("Lines", justify="right", width=10)
    tracks_table.add_column("Size", justify="right", width=10)
    tracks_table.add_column("Current Task", justify="left")

    for track_id in sorted(tracks.keys()):
        track = tracks[track_id]

        # Status color
        status_colors = {
            "completed": "green",
            "running": "yellow",
            "error": "red",
            "pending": "blue"
        }
        color = status_colors.get(track.status, "white")

        # Progress bar
        progress_bar = "█" * int(track.progress / 5) + "░" * (20 - int(track.progress / 5))
        progress_text = f"[{color}]{progress_bar}[/{color}] {track.progress:.1f}%"

        # Elapsed time
        elapsed = time.time() - track.start_time
        elapsed_str = f"{int(elapsed//60)}m {int(elapsed%60)}s"

        tracks_table.add_row(
            f"[bold]Track {track_id}[/bold]",
            f"[{color}]{track.status.upper()}[/{color}]",
            progress_text,
            f"{track.line_count:,}",
            f"{track.file_size/1024:.1f}KB",
            track.current_task[:50]
        )

    # System resources
    sys_table = Table(title="System Resources", expand=True, show_header=False)
    sys_table.add_column(justify="left", style="cyan", width=15)
    sys_table.add_column(justify="right")
    sys_table.add_column(justify="left", width=20)

    cpu_bar = "█" * int(system_metrics["cpu"] / 5) + "░" * (20 - int(system_metrics["cpu"] / 5))
    mem_bar = "█" * int(system_metrics["memory_percent"] / 5) + "░" * (20 - int(system_metrics["memory_percent"] / 5))
    disk_bar = "█" * int(system_metrics["disk_percent"] / 5) + "░" * (20 - int(system_metrics["disk_percent"] / 5))

    sys_table.add_row(
        "CPU Usage",
        f"{system_metrics['cpu']:.1f}%",
        f"[yellow]{cpu_bar}[/yellow]"
    )
    sys_table.add_row(
        "Memory Usage",
        f"{system_metrics['memory_used_gb']:.2f} / {system_metrics['memory_total_gb']:.2f} GB",
        f"[cyan]{mem_bar}[/cyan]"
    )
    sys_table.add_row(
        "Disk Free",
        f"{system_metrics['disk_free_gb']:.1f} GB",
        f"[green]{disk_bar}[/green]"
    )

    system_panel = Panel(sys_table, style="bold white")

    # Build layout
    layout = Layout()
    layout.split_column(
        Layout(header, size=3),
        Layout(summary, size=5),
        Layout(tracks_table, size=None),
        Layout(system_panel, size=7)
    )

    return layout


def main():
    """Main dashboard loop"""
    console = Console()

    try:
        with Live(console=console, refresh_per_second=1, screen=True) as live:
            while True:
                # Update data
                tracks = find_tracks()
                for track in tracks.values():
                    track.update()

                system_metrics = get_system_metrics()

                # Create layout
                layout = create_dashboard_layout(tracks, system_metrics)

                # Update display
                live.update(layout)

                # Sleep
                time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped by user[/yellow]")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔥 ULTRATHINK CLI Dashboard")
    print("="*80)
    print("\nInitializing dashboard...")
    print("Press Ctrl+C to exit\n")
    time.sleep(2)

    main()
