"""
Comprehensive tests for database/multi_project_manager.py

Target: 90%+ coverage (100/111 statements)
Tests: MultiProjectManager class methods

MANDATORY TESTING STANDARD:
- Tests REAL code (imports actual classes/functions)
- Mocks ONLY external dependencies (SQLiteContextLoader)
- Covers success paths, error paths, and edge cases
- ≥ 90% statement coverage required
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from database.multi_project_manager import MultiProjectManager


class TestMultiProjectManagerInit:
    """Test MultiProjectManager initialization"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_init_success(self, mock_loader_class):
        """Test successful initialization"""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager(db_path="test.db")

        assert manager.db_path == "test.db"
        assert manager.loader == mock_loader
        mock_loader_class.assert_called_once_with("test.db")

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_init_default_db_path(self, mock_loader_class):
        """Test initialization with default db path"""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager()

        assert manager.db_path == "ultrathink_context.db"
        mock_loader_class.assert_called_once_with("ultrathink_context.db")


class TestCreateProject:
    """Test create_project method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_project_with_auto_id(self, mock_loader_class):
        """Test creating project with auto-generated ID"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        project_id = manager.create_project(
            name="Test Project",
            description="Test description",
            total_story_points=1300
        )

        assert project_id.startswith("proj_")
        assert len(project_id) > 10
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_project_with_custom_id(self, mock_loader_class):
        """Test creating project with custom ID"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        project_id = manager.create_project(
            name="Test Project",
            description="Test description",
            total_story_points=1000,
            project_id="custom_project_123"
        )

        assert project_id == "custom_project_123"
        # Verify SQL was called with custom ID
        call_args = mock_cursor.execute.call_args[0]
        assert "custom_project_123" in call_args[1]

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_project_database_error(self, mock_loader_class):
        """Test project creation with database error"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")

        with pytest.raises(Exception, match="Database error"):
            manager.create_project(
                name="Test Project",
                description="Test description"
            )

        mock_conn.rollback.assert_called_once()


class TestLaunchInstance:
    """Test launch_instance method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_launch_instance_success(self, mock_loader_class):
        """Test successful instance launch"""
        mock_loader = Mock()
        mock_loader.load_context_for_instance.return_value = {
            'instance_id': 'inst_123',
            'status': 'ready'
        }
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        instance_id = manager.launch_instance(
            project_id="proj_001",
            phase_id=1
        )

        assert instance_id.startswith("inst_")
        mock_loader.load_context_for_instance.assert_called_once()
        call_kwargs = mock_loader.load_context_for_instance.call_args[1]
        assert call_kwargs['project_id'] == "proj_001"
        assert call_kwargs['phase_id'] == 1

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_launch_instance_without_phase(self, mock_loader_class):
        """Test instance launch without phase_id"""
        mock_loader = Mock()
        mock_loader.load_context_for_instance.return_value = {}
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        instance_id = manager.launch_instance(project_id="proj_001")

        assert instance_id.startswith("inst_")
        call_kwargs = mock_loader.load_context_for_instance.call_args[1]
        assert call_kwargs['phase_id'] is None


class TestGetProjectInstances:
    """Test get_project_instances method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_project_instances_success(self, mock_loader_class):
        """Test getting project instances"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()

        # Mock fetchall to return rows
        mock_cursor.fetchall.return_value = [
            {
                'instance_id': 'inst_001',
                'project_id': 'proj_001',
                'phase_id': 1,
                'hostname': 'localhost',
                'process_id': 12345,
                'started_at': '2025-11-20 10:00:00',
                'last_heartbeat': '2025-11-20 10:05:00',
                'status': 'active',
                'current_token_usage': 5000
            },
            {
                'instance_id': 'inst_002',
                'project_id': 'proj_001',
                'phase_id': 2,
                'hostname': 'localhost',
                'process_id': 12346,
                'started_at': '2025-11-20 10:01:00',
                'last_heartbeat': '2025-11-20 10:06:00',
                'status': 'active',
                'current_token_usage': 3000
            }
        ]

        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        instances = manager.get_project_instances("proj_001")

        assert len(instances) == 2
        assert instances[0]['instance_id'] == 'inst_001'
        assert instances[0]['project_id'] == 'proj_001'
        assert instances[0]['phase_id'] == 1
        assert instances[1]['instance_id'] == 'inst_002'
        mock_cursor.execute.assert_called_once()

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_project_instances_no_results(self, mock_loader_class):
        """Test getting project instances with no results"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        instances = manager.get_project_instances("proj_999")

        assert instances == []


class TestGetAllProjects:
    """Test get_all_projects method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_all_projects_success(self, mock_loader_class):
        """Test getting all projects"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_cursor.fetchall.return_value = [
            {
                'project_id': 'proj_001',
                'name': 'Project 1',
                'description': 'Description 1',
                'total_story_points': 1300,
                'completed_story_points': 500,
                'total_phases': 5,
                'created_at': '2025-11-20 09:00:00',
                'updated_at': '2025-11-20 10:00:00'
            },
            {
                'project_id': 'proj_002',
                'name': 'Project 2',
                'description': 'Description 2',
                'total_story_points': 1000,
                'completed_story_points': 200,
                'total_phases': 3,
                'created_at': '2025-11-20 09:30:00',
                'updated_at': '2025-11-20 10:30:00'
            }
        ]

        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        projects = manager.get_all_projects()

        assert len(projects) == 2
        assert projects[0]['project_id'] == 'proj_001'
        assert projects[0]['name'] == 'Project 1'
        assert projects[0]['total_story_points'] == 1300
        assert projects[1]['project_id'] == 'proj_002'

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_all_projects_empty(self, mock_loader_class):
        """Test getting all projects when none exist"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        projects = manager.get_all_projects()

        assert projects == []


class TestStoreContext:
    """Test store_context method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_store_context_success(self, mock_loader_class):
        """Test storing context"""
        mock_loader = Mock()
        mock_loader.store_context.return_value = 123  # snapshot_id
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        snapshot_id = manager.store_context(
            project_id="proj_001",
            content={"code": "def test(): pass"},
            priority="HIGH",
            content_type="code",
            phase_id=1
        )

        assert snapshot_id == 123
        mock_loader.store_context.assert_called_once_with(
            project_id="proj_001",
            content={"code": "def test(): pass"},
            priority="HIGH",
            content_type="code",
            phase_id=1
        )

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_store_context_default_params(self, mock_loader_class):
        """Test storing context with default parameters"""
        mock_loader = Mock()
        mock_loader.store_context.return_value = 456
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        snapshot_id = manager.store_context(
            project_id="proj_001",
            content={"data": "test"}
        )

        assert snapshot_id == 456
        call_kwargs = mock_loader.store_context.call_args[1]
        assert call_kwargs['priority'] == "HIGH"
        assert call_kwargs['content_type'] == "code"
        assert call_kwargs['phase_id'] is None


class TestCreatePhase:
    """Test create_phase method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_phase_success(self, mock_loader_class):
        """Test creating phase"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.lastrowid = 42
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        phase_id = manager.create_phase(
            project_id="proj_001",
            phase_number=1,
            name="Phase 1",
            story_points=260
        )

        assert phase_id == 42
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "proj_001" in call_args[1]
        assert 1 in call_args[1]
        assert "Phase 1" in call_args[1]
        assert 260 in call_args[1]
        mock_conn.commit.assert_called_once()

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_phase_default_story_points(self, mock_loader_class):
        """Test creating phase with default story points"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.lastrowid = 99
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        phase_id = manager.create_phase(
            project_id="proj_001",
            phase_number=2,
            name="Phase 2"
        )

        assert phase_id == 99
        call_args = mock_cursor.execute.call_args[0]
        assert 0 in call_args[1]  # Default story points

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_phase_database_error(self, mock_loader_class):
        """Test phase creation with database error"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")

        with pytest.raises(Exception, match="Database error"):
            manager.create_phase(
                project_id="proj_001",
                phase_number=1,
                name="Phase 1"
            )

        mock_conn.rollback.assert_called_once()


class TestGetProjectSummary:
    """Test get_project_summary method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_project_summary_success(self, mock_loader_class):
        """Test getting project summary"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_cursor.fetchall.return_value = [
            {
                'project_id': 'proj_001',
                'name': 'Project 1',
                'total_story_points': 1300,
                'completed_story_points': 500,
                'active_instances': 3,
                'total_snapshots': 150,
                'total_tokens': 50000,
                'created_at': '2025-11-20 09:00:00',
                'updated_at': '2025-11-20 10:00:00'
            },
            {
                'project_id': 'proj_002',
                'name': 'Project 2',
                'total_story_points': 1000,
                'completed_story_points': 200,
                'active_instances': 2,
                'total_snapshots': 75,
                'total_tokens': None,  # Test None handling
                'created_at': '2025-11-20 09:30:00',
                'updated_at': '2025-11-20 10:30:00'
            }
        ]

        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        summaries = manager.get_project_summary()

        assert len(summaries) == 2
        assert summaries[0]['project_id'] == 'proj_001'
        assert summaries[0]['active_instances'] == 3
        assert summaries[0]['total_snapshots'] == 150
        assert summaries[0]['total_tokens'] == 50000
        assert summaries[1]['total_tokens'] == 0  # None converted to 0

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_project_summary_empty(self, mock_loader_class):
        """Test getting project summary with no projects"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        summaries = manager.get_project_summary()

        assert summaries == []


class TestClose:
    """Test close method"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_close(self, mock_loader_class):
        """Test closing database connection"""
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        manager.close()

        mock_loader.close.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error handling"""

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_create_project_empty_name(self, mock_loader_class):
        """Test creating project with empty name"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        project_id = manager.create_project(
            name="",
            description="Test"
        )

        # Should still work - database will handle validation
        assert project_id.startswith("proj_")

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_store_context_empty_content(self, mock_loader_class):
        """Test storing context with empty content"""
        mock_loader = Mock()
        mock_loader.store_context.return_value = 777
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        snapshot_id = manager.store_context(
            project_id="proj_001",
            content={}
        )

        assert snapshot_id == 777

    @patch('database.multi_project_manager.SQLiteContextLoader')
    def test_get_project_instances_special_characters(self, mock_loader_class):
        """Test getting instances with special characters in project_id"""
        mock_loader = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_loader._get_connection.return_value = mock_conn
        mock_loader_class.return_value = mock_loader

        manager = MultiProjectManager("test.db")
        instances = manager.get_project_instances("proj_special-chars_123")

        # Should handle special characters gracefully
        assert instances == []
