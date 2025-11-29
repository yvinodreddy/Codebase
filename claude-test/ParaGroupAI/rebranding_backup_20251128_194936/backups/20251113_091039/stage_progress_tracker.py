#!/usr/bin/env python3
"""
Stage Progress Tracker
Calculates 0-100% progress based on ULTRATHINK stages
"""

from typing import Dict


class StageProgressTracker:
    """Tracks progress through 6 ULTRATHINK stages"""

    STAGES = {
        1: {"name": "Prompt Preprocessing & Analysis", "weight": 16},
        2: {"name": "Guardrails - Input Validation", "weight": 17},
        3: {"name": "Context Management", "weight": 17},
        4: {"name": "Agent Orchestration", "weight": 17},
        5: {"name": "Execution", "weight": 17},
        6: {"name": "Output Validation", "weight": 16}
    }

    def __init__(self):
        self.current_stage = 0
        self.stage_completion = 0.0

    def set_stage(self, stage_number: int, completion: float = 0.0):
        """
        Set current stage and completion percentage

        Args:
            stage_number: Stage number (1-6)
            completion: Completion percentage for this stage (0.0-1.0)
        """
        if stage_number < 1 or stage_number > 6:
            raise ValueError(f"Stage number must be 1-6, got {stage_number}")

        if completion < 0.0 or completion > 1.0:
            raise ValueError(f"Completion must be 0.0-1.0, got {completion}")

        self.current_stage = stage_number
        self.stage_completion = completion

    def calculate_progress(self, stage_number: int = None, stage_completion: float = None) -> int:
        """
        Calculate overall 0-100% progress

        Args:
            stage_number: Optional stage number override
            stage_completion: Optional completion override

        Returns:
            Integer progress percentage (0-100)
        """
        stage = stage_number if stage_number is not None else self.current_stage
        completion = stage_completion if stage_completion is not None else self.stage_completion

        if stage == 0:
            return 0

        if stage > 6:
            return 100

        # Calculate weight of all previous stages
        previous_weight = sum(
            s['weight'] for i, s in self.STAGES.items() if i < stage
        )

        # Calculate current stage contribution
        current_weight = self.STAGES[stage]['weight'] * completion

        # Total progress
        total_progress = previous_weight + current_weight

        return int(total_progress)

    def get_stage_name(self, stage_number: int = None) -> str:
        """Get name of a stage"""
        stage = stage_number if stage_number is not None else self.current_stage
        if stage < 1 or stage > 6:
            return "Unknown"
        return self.STAGES[stage]['name']

    def mark_stage_complete(self, stage_number: int):
        """Mark a stage as complete and advance"""
        self.set_stage(stage_number, 1.0)
        if stage_number < 6:
            self.set_stage(stage_number + 1, 0.0)

    def get_status(self) -> Dict:
        """Get current status"""
        return {
            'current_stage': self.current_stage,
            'stage_name': self.get_stage_name(),
            'stage_completion': self.stage_completion,
            'overall_progress': self.calculate_progress()
        }


# Convenience function
def create_progress_tracker() -> StageProgressTracker:
    """Create and return a progress tracker"""
    return StageProgressTracker()
