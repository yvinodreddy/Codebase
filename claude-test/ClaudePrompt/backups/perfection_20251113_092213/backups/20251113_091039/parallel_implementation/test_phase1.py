#!/usr/bin/env python3
"""
Test Real-Time Logging System
"""

import time
from realtime_verbose_logger import create_realtime_logger
from stage_progress_tracker import create_progress_tracker
from realtime_db_updates import create_track, update_track_progress, insert_log_entry

def test_realtime_logging():
    """Test the real-time logging system"""

    # Create test output file
    output_file = "parallel_implementation/test_realtime_log.txt"

    # Create logger
    logger = create_realtime_logger(output_file, enabled=True)

    # Create progress tracker
    tracker = create_progress_tracker()

    # Create test track
    track_id = create_track(name="Test Track", status="RUNNING", progress=0)

    if not track_id:
        print("Failed to create track")
        return False

    print(f"Created track ID: {track_id}")

    # Simulate processing through 6 stages
    for stage in range(1, 7):
        logger.stage_header(stage, tracker.get_stage_name(stage))

        # Simulate work in this stage
        for i in range(5):
            completion = (i + 1) / 5
            tracker.set_stage(stage, completion)
            progress = tracker.calculate_progress()

            # Log operation
            operation = f"Processing step {i+1}/5 in {tracker.get_stage_name(stage)}"
            logger.processing_step(operation, "in progress")

            # Update database
            update_track_progress(
                track_id=track_id,
                progress=progress,
                current_task=operation
            )

            # Insert log entry
            insert_log_entry(track_id, "INFO", operation)

            # Small delay to simulate work
            time.sleep(0.5)

        # Mark stage complete
        tracker.mark_stage_complete(stage)
        logger.stage_footer()

        # Update database
        update_track_progress(
            track_id=track_id,
            progress=tracker.calculate_progress(),
            current_task=f"Completed {tracker.get_stage_name(stage)}"
        )

    # Final update
    update_track_progress(
        track_id=track_id,
        status="COMPLETED",
        progress=100,
        current_task="All stages completed"
    )

    logger.success("Test completed successfully!")
    logger.close()

    print(f"\nTest complete! Check {output_file} for real-time logs.")
    print(f"Track ID {track_id} should show 100% progress in database.")

    return True

if __name__ == '__main__':
    success = test_realtime_logging()
    exit(0 if success else 1)
