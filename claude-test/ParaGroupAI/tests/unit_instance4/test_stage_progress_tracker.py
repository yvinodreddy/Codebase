#!/usr/bin/env python3
"""Comprehensive test suite for stage_progress_tracker.py - Target: 90%+ coverage"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from stage_progress_tracker import StageProgressTracker, create_progress_tracker

class TestStageProgressTracker:
    def setup_method(self):
        self.tracker = StageProgressTracker()
    
    def test_initialization(self):
        assert self.tracker.current_stage == 0
        assert self.tracker.stage_completion == 0.0
        assert len(self.tracker.STAGES) == 6
    
    def test_set_stage_valid(self):
        self.tracker.set_stage(3, 0.5)
        assert self.tracker.current_stage == 3
        assert self.tracker.stage_completion == 0.5
    
    def test_set_stage_invalid_number(self):
        with pytest.raises(ValueError):
            self.tracker.set_stage(7)
        with pytest.raises(ValueError):
            self.tracker.set_stage(0)
    
    def test_set_stage_invalid_completion(self):
        with pytest.raises(ValueError):
            self.tracker.set_stage(1, 1.5)
        with pytest.raises(ValueError):
            self.tracker.set_stage(1, -0.1)
    
    def test_calculate_progress_stage_0(self):
        progress = self.tracker.calculate_progress(0, 0)
        assert progress == 0
    
    def test_calculate_progress_stage_1_partial(self):
        progress = self.tracker.calculate_progress(1, 0.5)
        assert progress == 8  # 16 * 0.5
    
    def test_calculate_progress_stage_2_complete(self):
        progress = self.tracker.calculate_progress(2, 1.0)
        assert progress == 33  # 16 + 17
    
    def test_calculate_progress_all_stages(self):
        progress = self.tracker.calculate_progress(6, 1.0)
        assert progress == 100
    
    def test_calculate_progress_beyond_max(self):
        progress = self.tracker.calculate_progress(7, 0)
        assert progress == 100
    
    def test_get_stage_name_valid(self):
        name = self.tracker.get_stage_name(1)
        assert name == "Prompt Preprocessing & Analysis"
    
    def test_get_stage_name_invalid(self):
        name = self.tracker.get_stage_name(0)
        assert name == "Unknown"
        name = self.tracker.get_stage_name(7)
        assert name == "Unknown"
    
    def test_mark_stage_complete(self):
        self.tracker.mark_stage_complete(2)
        assert self.tracker.current_stage == 3
        assert self.tracker.stage_completion == 0.0
        
        status = self.tracker.get_status()
        assert status['current_stage'] == 3
    
    def test_mark_stage_complete_last_stage(self):
        self.tracker.mark_stage_complete(6)
        assert self.tracker.current_stage == 6
        assert self.tracker.stage_completion == 1.0
    
    def test_get_status(self):
        self.tracker.set_stage(3, 0.75)
        status = self.tracker.get_status()
        
        assert status['current_stage'] == 3
        assert status['stage_name'] == "Context Management"
        assert status['stage_completion'] == 0.75
        assert status['overall_progress'] == 50  # Previous stages + 75% of stage 3

def test_create_progress_tracker():
    tracker = create_progress_tracker()
    assert isinstance(tracker, StageProgressTracker)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
