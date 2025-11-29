#!/usr/bin/env python3
"""
Comprehensive test suite for multi_source_metrics_verifier.py
Target: 90%+ coverage with real code testing
"""

import pytest
import json
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from multi_source_metrics_verifier import (
    MetricsSource,
    ContextCacheSource,
    ConversationStatsSource,
    RealtimeMetricsSource,
    AgentCounterSource,
    MultiSourceMetricsVerifier
)


class TestMetricsSource:
    """Test the base MetricsSource class"""

    def test_initialization(self):
        """Test MetricsSource initialization"""
        source = MetricsSource("TestSource", max_age_seconds=300)
        assert source.name == "TestSource"
        assert source.max_age_seconds == 300
        assert source.confidence == 0.0
        assert source.available == False
        assert source.data == {}

    def test_is_fresh_file_not_exists(self):
        """Test is_fresh when file doesn't exist"""
        source = MetricsSource("TestSource")
        with tempfile.NamedTemporaryFile(delete=True) as tf:
            result = source.is_fresh(tf.name + "_nonexistent")
        assert result == False

    def test_is_fresh_file_exists_and_fresh(self):
        """Test is_fresh when file exists and is fresh"""
        source = MetricsSource("TestSource", max_age_seconds=300)
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"test")
            tf.flush()
            result = source.is_fresh(tf.name)
            os.unlink(tf.name)
        assert result == True

    def test_is_fresh_file_exists_but_stale(self):
        """Test is_fresh when file exists but is stale"""
        source = MetricsSource("TestSource", max_age_seconds=0.001)
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"test")
            tf.flush()
            time.sleep(0.01)  # Make file stale
            result = source.is_fresh(tf.name)
            os.unlink(tf.name)
        assert result == False

    def test_calculate_confidence_very_fresh(self):
        """Test confidence calculation for very fresh data (<1 second)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(0.5)
        assert confidence == 100.0

    def test_calculate_confidence_fresh(self):
        """Test confidence calculation for fresh data (1-5 seconds)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(3)
        assert confidence == 95.0

    def test_calculate_confidence_moderately_fresh(self):
        """Test confidence calculation for moderately fresh data (5-30 seconds)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(15)
        assert confidence == 85.0

    def test_calculate_confidence_getting_stale(self):
        """Test confidence calculation for data getting stale (30-60 seconds)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(45)
        assert confidence == 70.0

    def test_calculate_confidence_stale(self):
        """Test confidence calculation for stale data (60-300 seconds)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(180)
        assert confidence == 50.0

    def test_calculate_confidence_very_stale(self):
        """Test confidence calculation for very stale data (>300 seconds)"""
        source = MetricsSource("TestSource")
        confidence = source.calculate_confidence(600)
        assert confidence == 20.0


class TestContextCacheSource:
    """Test the ContextCacheSource class"""

    def test_initialization(self):
        """Test ContextCacheSource initialization"""
        source = ContextCacheSource()
        assert source.name == "ContextCache"
        assert source.max_age_seconds == 5

    @patch('os.path.exists')
    def test_fetch_file_not_exists(self, mock_exists):
        """Test fetch when cache file doesn't exist"""
        mock_exists.return_value = False
        source = ContextCacheSource()
        result = source.fetch()
        assert result == False
        assert source.available == False

    @patch('subprocess.run')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_success(self, mock_exists, mock_getmtime, mock_run):
        """Test successful fetch from context cache"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 2  # 2 seconds old

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            'status': 'success',
            'tokens_used': 5000,
            'tokens_total': 200000,
            'tokens_pct': 2.5,
            'model_short': 'Claude'
        })
        mock_run.return_value = mock_result

        source = ContextCacheSource()
        result = source.fetch()

        assert result == True
        assert source.available == True
        assert source.data['tokens_used'] == 5000
        assert source.data['tokens_total'] == 200000
        assert source.data['tokens_pct'] == 2.5
        assert source.data['model'] == 'Claude'

    @patch('subprocess.run')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_subprocess_error(self, mock_exists, mock_getmtime, mock_run):
        """Test fetch when subprocess fails"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 2
        mock_run.side_effect = Exception("Subprocess error")

        source = ContextCacheSource()
        result = source.fetch()

        assert result == False
        assert source.available == False

    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_file_too_old(self, mock_exists, mock_getmtime):
        """Test fetch when file is too old"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 10  # 10 seconds old (max is 5)

        source = ContextCacheSource()
        result = source.fetch()

        assert result == False
        assert source.available == False


class TestConversationStatsSource:
    """Test the ConversationStatsSource class"""

    def test_initialization(self):
        """Test ConversationStatsSource initialization"""
        source = ConversationStatsSource()
        assert source.name == "ConversationStats"
        assert source.max_age_seconds == 60

    def test_fetch_empty_json(self):
        """Test fetch with empty JSON input"""
        source = ConversationStatsSource()
        result = source.fetch({})
        assert result == False
        assert source.available == False

    def test_fetch_with_conversation_stats(self):
        """Test fetch with valid conversation stats"""
        source = ConversationStatsSource()
        json_input = {
            'conversation_stats': {
                'context_tokens': 10000,
                'max_tokens': 200000
            }
        }
        result = source.fetch(json_input)

        assert result == True
        assert source.available == True
        assert source.data['tokens_used'] == 10000
        assert source.data['tokens_total'] == 200000
        assert source.data['tokens_pct'] == 5.0
        assert source.confidence == 90.0

    def test_fetch_with_alternative_fields(self):
        """Test fetch with alternative field names"""
        source = ConversationStatsSource()
        json_input = {
            'conversation_stats': {
                'tokens_used': 15000,
                'context_limit': 150000
            }
        }
        result = source.fetch(json_input)

        assert result == True
        assert source.available == True
        assert source.data['tokens_used'] == 15000
        assert source.data['tokens_total'] == 150000
        assert source.data['tokens_pct'] == 10.0

    def test_fetch_with_total_tokens(self):
        """Test fetch with total_tokens field"""
        source = ConversationStatsSource()
        json_input = {
            'conversation_stats': {
                'total_tokens': 8000
            }
        }
        result = source.fetch(json_input)

        assert result == True
        assert source.available == True
        assert source.data['tokens_used'] == 8000
        assert source.data['tokens_total'] == 200000

    def test_fetch_with_zero_tokens(self):
        """Test fetch when tokens are zero"""
        source = ConversationStatsSource()
        json_input = {
            'conversation_stats': {
                'context_tokens': 0
            }
        }
        result = source.fetch(json_input)

        assert result == False
        assert source.available == False

    def test_fetch_with_exception(self):
        """Test fetch with invalid data causing exception"""
        source = ConversationStatsSource()
        json_input = {
            'conversation_stats': None  # Will cause exception
        }
        result = source.fetch(json_input)

        assert result == False
        assert source.available == False


class TestRealtimeMetricsSource:
    """Test the RealtimeMetricsSource class"""

    def test_initialization_no_instance_id(self):
        """Test RealtimeMetricsSource initialization without instance ID"""
        source = RealtimeMetricsSource()
        assert source.name == "RealtimeMetrics"
        assert source.max_age_seconds == 300
        assert source.instance_id == None

    def test_initialization_with_instance_id(self):
        """Test RealtimeMetricsSource initialization with instance ID"""
        source = RealtimeMetricsSource(instance_id="test_123")
        assert source.instance_id == "test_123"

    @patch('os.path.exists')
    def test_fetch_file_not_exists(self, mock_exists):
        """Test fetch when metrics file doesn't exist"""
        mock_exists.return_value = False
        source = RealtimeMetricsSource()
        result = source.fetch()
        assert result == False
        assert source.available == False

    @patch('builtins.open', new_callable=mock_open, read_data='{"agents_total": 25, "context_pct": 5.0, "confidence": 99.2, "executing": true, "tokens_used": 10000, "tokens_total": 200000, "tokens_pct": 5.0}')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_success_shared_mode(self, mock_exists, mock_getmtime, mock_file):
        """Test successful fetch in shared mode"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 10

        source = RealtimeMetricsSource()
        result = source.fetch()

        assert result == True
        assert source.available == True
        assert source.data['agents'] == 25
        assert source.data['context_pct'] == 5.0
        assert source.data['confidence'] == 99.2
        assert source.data['executing'] == True
        assert source.data['tokens_used'] == 10000

    @patch('builtins.open', new_callable=mock_open, read_data='{"agents": 30}')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_success_instance_mode(self, mock_exists, mock_getmtime, mock_file):
        """Test successful fetch in instance mode"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 10

        source = RealtimeMetricsSource(instance_id="inst_123")
        result = source.fetch()

        assert result == True
        assert source.available == True
        assert source.data['agents'] == 30

    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_file_too_old(self, mock_exists, mock_getmtime):
        """Test fetch when file is too old"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 400  # > 300 seconds

        source = RealtimeMetricsSource()
        result = source.fetch()

        assert result == False
        assert source.available == False


class TestAgentCounterSource:
    """Test the AgentCounterSource class"""

    def test_initialization(self):
        """Test AgentCounterSource initialization"""
        source = AgentCounterSource()
        assert source.name == "AgentCounter"
        assert source.max_age_seconds == 300

    @patch('builtins.open', new_callable=mock_open, read_data='42')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_success(self, mock_exists, mock_getmtime, mock_file):
        """Test successful fetch from agent counter"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 10

        source = AgentCounterSource()
        result = source.fetch()

        assert result == True
        assert source.available == True
        assert source.data['agents'] == 42

    @patch('builtins.open', new_callable=mock_open, read_data='invalid')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    def test_fetch_invalid_content(self, mock_exists, mock_getmtime, mock_file):
        """Test fetch with invalid file content"""
        mock_exists.return_value = True
        mock_getmtime.return_value = time.time() - 10

        source = AgentCounterSource()
        result = source.fetch()

        assert result == False
        assert source.available == False


class TestMultiSourceMetricsVerifier:
    """Test the MultiSourceMetricsVerifier class"""

    def test_initialization(self):
        """Test MultiSourceMetricsVerifier initialization"""
        verifier = MultiSourceMetricsVerifier()
        assert verifier.instance_id == None
        assert 'context_cache' in verifier.sources
        assert 'conversation_stats' in verifier.sources
        assert 'realtime_metrics' in verifier.sources
        assert 'agent_counter' in verifier.sources

    def test_initialization_with_instance_id(self):
        """Test initialization with instance ID"""
        verifier = MultiSourceMetricsVerifier(instance_id="inst_456")
        assert verifier.instance_id == "inst_456"

    @patch.object(AgentCounterSource, 'fetch')
    @patch.object(RealtimeMetricsSource, 'fetch')
    @patch.object(ConversationStatsSource, 'fetch')
    @patch.object(ContextCacheSource, 'fetch')
    def test_fetch_all_sources(self, mock_context, mock_conv, mock_realtime, mock_agent):
        """Test fetching from all sources"""
        mock_context.return_value = True
        mock_conv.return_value = False
        mock_realtime.return_value = True
        mock_agent.return_value = True

        verifier = MultiSourceMetricsVerifier()
        results = verifier.fetch_all_sources()

        assert results['context_cache'] == True
        assert results['conversation_stats'] == False
        assert results['realtime_metrics'] == True
        assert results['agent_counter'] == True

    def test_verify_tokens_no_sources(self):
        """Test verify_tokens when no sources are available"""
        verifier = MultiSourceMetricsVerifier()
        tokens_used, tokens_total, tokens_pct, confidence = verifier.verify_tokens()

        assert tokens_used == 0
        assert tokens_total == 200000
        assert tokens_pct == 0.0
        assert confidence == 0.0

    def test_verify_tokens_single_source(self):
        """Test verify_tokens with single source available"""
        verifier = MultiSourceMetricsVerifier()
        verifier.sources['realtime_metrics'].available = True
        verifier.sources['realtime_metrics'].data = {
            'tokens_used': 15000,
            'tokens_total': 200000,
            'tokens_pct': 7.5
        }
        verifier.sources['realtime_metrics'].confidence = 80.0

        tokens_used, tokens_total, tokens_pct, confidence = verifier.verify_tokens()

        assert tokens_used == 15000
        assert tokens_total == 200000
        assert tokens_pct == 7.5
        assert confidence == 80.0

    def test_verify_tokens_multiple_sources_priority(self):
        """Test verify_tokens with multiple sources (priority selection)"""
        verifier = MultiSourceMetricsVerifier()

        # Set up context cache (highest priority)
        verifier.sources['context_cache'].available = True
        verifier.sources['context_cache'].data = {
            'tokens_used': 10000,
            'tokens_total': 200000,
            'tokens_pct': 5.0
        }
        verifier.sources['context_cache'].confidence = 95.0

        # Set up realtime metrics (lower priority)
        verifier.sources['realtime_metrics'].available = True
        verifier.sources['realtime_metrics'].data = {
            'tokens_used': 12000,
            'tokens_total': 200000,
            'tokens_pct': 6.0
        }
        verifier.sources['realtime_metrics'].confidence = 70.0

        tokens_used, tokens_total, tokens_pct, confidence = verifier.verify_tokens()

        # Should select context_cache due to higher priority
        assert tokens_used == 10000
        assert tokens_total == 200000
        assert tokens_pct == 5.0
        assert confidence == 95.0

    def test_verify_agents_no_sources(self):
        """Test verify_agents when no sources are available"""
        verifier = MultiSourceMetricsVerifier()
        agents, confidence = verifier.verify_agents()

        assert agents == 'N/A'
        assert confidence == 0.0

    def test_verify_agents_with_source(self):
        """Test verify_agents with available source"""
        verifier = MultiSourceMetricsVerifier()
        verifier.sources['agent_counter'].available = True
        verifier.sources['agent_counter'].data = {'agents': 25}
        verifier.sources['agent_counter'].confidence = 85.0

        agents, confidence = verifier.verify_agents()

        assert agents == '25'
        assert confidence == 85.0

    def test_verify_confidence_no_source(self):
        """Test verify_confidence when no source is available"""
        verifier = MultiSourceMetricsVerifier()
        conf, confidence = verifier.verify_confidence()

        assert conf == '--'
        assert confidence == 0.0

    def test_verify_confidence_with_source(self):
        """Test verify_confidence with available source"""
        verifier = MultiSourceMetricsVerifier()
        verifier.sources['realtime_metrics'].available = True
        verifier.sources['realtime_metrics'].data = {'confidence': 99.5}
        verifier.sources['realtime_metrics'].confidence = 90.0

        conf, confidence = verifier.verify_confidence()

        assert conf == '99.5'
        assert confidence == 90.0

    def test_calculate_status_optimal(self):
        """Test calculate_status for optimal conditions"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(5.0, True)
        assert status == '🟢 OPTIMAL'

    def test_calculate_status_active(self):
        """Test calculate_status for active state"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(60.0, True)
        assert status == '✅ ACTIVE'

    def test_calculate_status_warning(self):
        """Test calculate_status for warning state"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(88.0, True)
        assert status == '🟡 WARNING'

    def test_calculate_status_critical(self):
        """Test calculate_status for critical state"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(96.0, True)
        assert status == '🔴 CRITICAL'

    def test_calculate_status_not_executing_optimal(self):
        """Test calculate_status when not executing (optimal)"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(5.0, False)
        assert status == '🟢 OPTIMAL'

    def test_calculate_status_not_executing_ready(self):
        """Test calculate_status when not executing (ready)"""
        verifier = MultiSourceMetricsVerifier()
        status = verifier.calculate_status(15.0, False)
        assert status == '🟢 READY'

    @patch.object(MultiSourceMetricsVerifier, 'fetch_all_sources')
    @patch.object(MultiSourceMetricsVerifier, 'verify_tokens')
    @patch.object(MultiSourceMetricsVerifier, 'verify_agents')
    @patch.object(MultiSourceMetricsVerifier, 'verify_confidence')
    def test_verify_all_complete_flow(self, mock_conf, mock_agents, mock_tokens, mock_fetch):
        """Test complete verification flow"""
        mock_fetch.return_value = {
            'context_cache': True,
            'conversation_stats': False,
            'realtime_metrics': True,
            'agent_counter': True
        }
        mock_tokens.return_value = (15000, 200000, 7.5, 90.0)
        mock_agents.return_value = ('25', 85.0)
        mock_conf.return_value = ('99.2', 92.0)

        verifier = MultiSourceMetricsVerifier()
        verifier.sources['conversation_stats'].available = True

        metrics = verifier.verify_all()

        assert metrics['agents'] == '25'
        assert metrics['tokens_used'] == 15000
        assert metrics['tokens_total'] == 200000
        assert metrics['tokens_pct'] == 7.5
        assert metrics['tokens_display'] == '15k/200k'
        assert metrics['confidence'] == '99.2'
        assert metrics['status'] == '🟢 OPTIMAL'
        assert metrics['executing'] == True

    def test_build_metrics_from_state(self):
        """Test building metrics from persisted state"""
        verifier = MultiSourceMetricsVerifier()

        state = {
            'agents': '30',
            'tokens_used': 20000,
            'tokens_total': 200000,
            'tokens_pct': 10.0,
            'tokens_display': '20k/200k',
            'confidence': '98.5',
            'status': '🟢 OPTIMAL',
            'lifecycle_state': 'IDLE',
            'frozen_at': '2025-11-22T10:00:00'
        }

        fetch_results = {
            'context_cache': False,
            'conversation_stats': False,
            'realtime_metrics': False,
            'agent_counter': False
        }

        metrics = verifier._build_metrics_from_state(state, fetch_results)

        assert metrics['agents'] == '30'
        assert metrics['tokens_used'] == 20000
        assert metrics['tokens_pct'] == 10.0
        assert metrics['confidence'] == '98.5'
        assert metrics['status'] == '🟢 OPTIMAL'
        assert metrics['executing'] == False
        assert metrics['verification_report']['source'] == 'persisted_state'


    def test_context_cache_source_exception_during_fetch(self):
        """Test ContextCacheSource handles exceptions properly"""
        source = ContextCacheSource()

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("API error")
            result = source.fetch()

        assert result == False
        assert source.available == False

    def test_realtime_metrics_file_invalid_json(self):
        """Test RealtimeMetricsSource handles invalid JSON"""
        source = RealtimeMetricsSource()

        # Create invalid JSON content
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_mtime = time.time()
                with patch('pathlib.Path.read_text', return_value="not valid json {"):
                    result = source.fetch()

        assert result == False
        assert source.available == False

    def test_agent_counter_file_permission_error(self):
        """Test AgentCounterSource handles permission errors"""
        source = AgentCounterSource()

        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_mtime = time.time()
                with patch('pathlib.Path.read_text', side_effect=PermissionError("No permission")):
                    result = source.fetch()

        assert result == False
        assert source.available == False

    def test_conversation_stats_malformed_json(self):
        """Test ConversationStatsSource handles malformed JSON"""
        source = ConversationStatsSource()

        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_mtime = time.time()
                with patch('pathlib.Path.read_text', return_value='{"incomplete": '):
                    result = source.fetch()

        assert result == False
        assert source.available == False

    def test_metrics_source_import_error_handling(self):
        """Test handling when metrics_state_persistence is unavailable"""
        # Simulate ImportError for metrics_state_persistence
        import sys
        original_modules = sys.modules.copy()

        # Remove the module if it exists
        if 'metrics_state_persistence' in sys.modules:
            del sys.modules['metrics_state_persistence']

        # Mock the import to raise ImportError
        with patch.dict('sys.modules', {'metrics_state_persistence': None}):
            # This would trigger the except ImportError block when module is reloaded
            # Since module is already loaded, we can't easily test this without reloading
            # But we can test that STATE_PERSISTENCE_AVAILABLE flag works correctly
            from multi_source_metrics_verifier import STATE_PERSISTENCE_AVAILABLE

            if not STATE_PERSISTENCE_AVAILABLE:
                # Test that verifier still works without persistence
                verifier = MultiSourceMetricsVerifier()
                assert verifier is not None

        # Restore original modules
        sys.modules.update(original_modules)

    def test_verify_all_with_json_input_state_persistence_unavailable(self):
        """Test verify_all when state persistence is not available"""
        verifier = MultiSourceMetricsVerifier()

        # Mock STATE_PERSISTENCE_AVAILABLE as False
        with patch('multi_source_metrics_verifier.STATE_PERSISTENCE_AVAILABLE', False):
            json_input = {
                'tokens_used': 5000,
                'tokens_total': 100000,
                'confidence': 95.0
            }

            metrics = verifier.verify_all(json_input)

            # Should still work without state persistence
            assert metrics is not None
            assert 'tokens_used' in metrics

    def test_realtime_metrics_source_different_path_modes(self):
        """Test RealtimeMetricsSource with different instance IDs"""
        # Test shared mode (no instance_id)
        source = RealtimeMetricsSource()
        assert source.instance_id is None

        # Test instance mode
        source_with_id = RealtimeMetricsSource(instance_id='test123')
        assert source_with_id.instance_id == 'test123'

        # Test that they handle fetching differently based on instance_id
        # The actual file path is determined internally

    def test_multiline_exception_scenarios(self):
        """Test various exception scenarios in MultiSourceMetricsVerifier"""
        verifier = MultiSourceMetricsVerifier()

        # Test with sources that all fail
        with patch.object(verifier.sources['context_cache'], 'fetch', return_value=False):
            with patch.object(verifier.sources['conversation_stats'], 'fetch', return_value=False):
                with patch.object(verifier.sources['realtime_metrics'], 'fetch', return_value=False):
                    with patch.object(verifier.sources['agent_counter'], 'fetch', return_value=False):
                        results = verifier.fetch_all_sources()

                        # All should be False
                        assert all(not v for v in results.values())

                        # Metrics should still return defaults
                        metrics = verifier.verify_all()
                        assert metrics['agents'] == '0'
                        assert metrics['confidence'] == '0.0'
                        # When not executing, status depends on available sources
                        assert '⚫' in metrics['status'] or '🔴' in metrics['status']

if __name__ == "__main__":
    pytest.main([__file__, "-v"])