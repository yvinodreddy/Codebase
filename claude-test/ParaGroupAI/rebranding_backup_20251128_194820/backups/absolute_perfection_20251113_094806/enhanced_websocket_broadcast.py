#!/usr/bin/env python3
"""
Enhanced WebSocket Broadcasting
Broadcasts updates every 2 seconds with comprehensive data
"""
import asyncio
import time
from typing import Dict, List

async def broadcast_live_updates(manager, get_running_tracks, get_track_data,
                                 get_ultrathink_details, get_latest_logs):
    """
    Broadcast updates every 2 seconds

    Args:
        manager: WebSocket manager
        get_running_tracks: Function to get running tracks
        get_track_data: Function to get track data
        get_ultrathink_details: Function to get ULTRATHINK details
        get_latest_logs: Function to get latest logs
    """
    while True:
        try:
            running_tracks = get_running_tracks()

            for track in running_tracks:
                track_data = get_track_data(track.id)
                ultrathink_data = get_ultrathink_details(track.id)
                latest_logs = get_latest_logs(track.id, limit=10)

                await manager.broadcast_json({
                    'type': 'track_update',
                    'track': track_data,
                    'ultrathink': ultrathink_data,
                    'logs': latest_logs,
                    'timestamp': time.time()
                })

            await asyncio.sleep(2)

        except Exception as e:
            print(f"Broadcast error: {e}")
            await asyncio.sleep(2)
