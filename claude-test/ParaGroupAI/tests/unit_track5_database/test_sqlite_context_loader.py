"""
Comprehensive tests for database/sqlite_context_loader.py

Target: 90%+ coverage (134/149 statements)
Tests: SQLiteContextLoader class methods

MANDATORY TESTING STANDARD:
- Tests REAL code (imports actual classes/functions)
- Mocks ONLY external dependencies (sqlite3, file I/O)
- Covers success paths, error paths, and edge cases
- ≥ 90% statement coverage required
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from database.sqlite_context_loader import SQLiteContextLoader
import sqlite3
from datetime import datetime
from pathlib import Path


class TestSQLiteContextLoaderInit:
    """Test SQLiteContextLoader initialization"""

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_init_success(self, mock_init_db, mock_path_class):
        """Test successful initialization"""
        mock_path = Mock()
        mock_path.parent.mkdir = Mock()
        mock_path_class.return_value = mock_path

        loader = SQLiteContextLoader(db_path="test.db")

        assert loader.db_path == mock_path
        mock_path.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_init_db.assert_called_once()

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_init_default_path(self, mock_init_db, mock_path_class):
        """Test initialization with default path"""
        loader = SQLiteContextLoader()

        mock_path_class.assert_called_once_with("ultrathink_context.db")


class TestGetConnection:
    """Test _get_connection method"""

    @patch('database.sqlite_context_loader.sqlite3.connect')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_get_connection_new(self, mock_init_db, mock_path_class, mock_connect):
        """Test getting new connection"""
        mock_conn = Mock()
        mock_conn.execute = Mock()
        mock_connect.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        conn = loader._get_connection()

        assert conn == mock_conn
        mock_connect.assert_called_once()
        # Check PRAGMA commands were executed
        assert mock_conn.execute.call_count >= 2

    @patch('database.sqlite_context_loader.sqlite3.connect')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_get_connection_reuse(self, mock_init_db, mock_path_class, mock_connect):
        """Test reusing existing connection"""
        mock_conn = Mock()
        mock_conn.execute = Mock()
        mock_connect.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")

        # First call
        conn1 = loader._get_connection()
        # Second call should reuse
        conn2 = loader._get_connection()

        assert conn1 == conn2
        # connect should only be called once
        mock_connect.assert_called_once()


class TestInitializeDatabase:
    """Test _initialize_database method"""

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_get_connection')
    def test_initialize_schema_missing(self, mock_get_conn, mock_path_class):
        """Test when schema file doesn't exist"""
        mock_path = Mock()
        mock_path.parent.mkdir = Mock()
        mock_path_class.return_value = mock_path

        # Mock schema file not existing
        mock_schema_file = Mock()
        mock_schema_file.exists.return_value = False

        # Mock Path(__file__).parent / "schema_sqlite.sql" to return mock_schema_file
        with patch.object(Path, '__truediv__', return_value=mock_schema_file):
            # Mock database connection and cursor (called before schema check)
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = ("projects",)  # Already initialized
            mock_conn = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            loader = SQLiteContextLoader.__new__(SQLiteContextLoader)
            loader.db_path = mock_path
            loader._local = Mock()

            # This should log warning and return early
            loader._initialize_database()

            # get_connection should be called to check if initialized
            mock_get_conn.assert_called_once()

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('builtins.open', new_callable=mock_open, read_data="CREATE TABLE test (id INTEGER);")
    def test_initialize_schema_new_database(self, mock_file, mock_get_conn, mock_path_class):
        """Test initializing new database"""
        mock_path = Mock()
        mock_path.parent.mkdir = Mock()
        mock_path_class.return_value = mock_path

        # Mock schema file exists
        mock_schema_file = Mock()
        mock_schema_file.exists.return_value = True

        # Mock Path(__file__).parent / "schema_sqlite.sql" to return mock_schema_file
        with patch.object(Path, '__truediv__', return_value=mock_schema_file):
            # Mock database connection and cursor
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = None  # Table doesn't exist yet
            mock_conn = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            loader = SQLiteContextLoader.__new__(SQLiteContextLoader)
            loader.db_path = mock_path
            loader._local = Mock()

            loader._initialize_database()

            # Should read schema and execute it
            mock_file.assert_called()
            mock_cursor.execute.assert_called()
            mock_conn.commit.assert_called()

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_get_connection')
    def test_initialize_schema_already_exists(self, mock_get_conn, mock_path_class):
        """Test when database is already initialized"""
        mock_path = Mock()
        mock_path.parent.mkdir = Mock()
        mock_path_class.return_value = mock_path

        # Mock database connection and cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = ("projects",)  # Table exists
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader.__new__(SQLiteContextLoader)
        loader.db_path = mock_path
        loader._local = Mock()

        loader._initialize_database()

        # Should check and return early
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_not_called()


class TestLoadContextForInstance:
    """Test load_context_for_instance method"""

    @patch.object(SQLiteContextLoader, '_register_instance')
    @patch.object(SQLiteContextLoader, '_load_priority')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_load_context_success(self, mock_init_db, mock_path, mock_load_priority, mock_register):
        """Test successful context loading"""
        mock_load_priority.return_value = [
            {"snapshot_id": 1, "content": "test1"},
            {"snapshot_id": 2, "content": "test2"}
        ]

        loader = SQLiteContextLoader(db_path="test.db")
        result = loader.load_context_for_instance(
            instance_id="inst_001",
            project_id="proj_001",
            phase_id=1
        )

        assert result["instance_id"] == "inst_001"
        assert result["project_id"] == "proj_001"
        assert result["phase_id"] == 1
        assert len(result["critical_context"]) == 2
        assert result["status"] == "ready"
        assert "load_time_ms" in result

        mock_load_priority.assert_called_once_with("CRITICAL", "proj_001", 1)
        mock_register.assert_called_once_with("inst_001", "proj_001", 1)

    @patch.object(SQLiteContextLoader, '_register_instance')
    @patch.object(SQLiteContextLoader, '_load_priority')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_load_context_no_phase(self, mock_init_db, mock_path, mock_load_priority, mock_register):
        """Test loading context without phase_id"""
        mock_load_priority.return_value = []

        loader = SQLiteContextLoader(db_path="test.db")
        result = loader.load_context_for_instance(
            instance_id="inst_002",
            project_id="proj_002",
            phase_id=None
        )

        assert result["phase_id"] is None
        mock_load_priority.assert_called_once_with("CRITICAL", "proj_002", None)


class TestLoadPriority:
    """Test _load_priority method"""

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_load_priority_with_results(self, mock_init_db, mock_path, mock_get_conn):
        """Test loading priority with results"""
        # Mock cursor with results
        mock_row1 = {
            'snapshot_id': 1,
            'content_type': 'code',
            'priority': 'CRITICAL',
            'token_count': 100,
            'content': '{"test": "data1"}',
            'metadata': '{}',
            'created_at': '2025-01-01 00:00:00'
        }
        mock_row2 = {
            'snapshot_id': 2,
            'content_type': 'config',
            'priority': 'CRITICAL',
            'token_count': 50,
            'content': '{"test": "data2"}',
            'metadata': '{}',
            'created_at': '2025-01-01 00:01:00'
        }

        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [mock_row1, mock_row2]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        results = loader._load_priority("CRITICAL", "proj_001", 1)

        assert len(results) == 2
        assert results[0]["snapshot_id"] == 1
        assert results[1]["snapshot_id"] == 2
        mock_cursor.execute.assert_called_once()

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_load_priority_empty(self, mock_init_db, mock_path, mock_get_conn):
        """Test loading priority with no results"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        results = loader._load_priority("HIGH", "proj_002", None)

        assert results == []


class TestRegisterInstance:
    """Test _register_instance method"""

    @patch('os.getpid')
    @patch('socket.gethostname')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_register_instance_success(self, mock_init_db, mock_path, mock_get_conn, mock_hostname, mock_getpid):
        """Test successful instance registration"""
        mock_hostname.return_value = "test-host"
        mock_getpid.return_value = 12345

        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        loader._register_instance("inst_001", "proj_001", 1)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('os.getpid')
    @patch('socket.gethostname')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_register_instance_error(self, mock_init_db, mock_path, mock_get_conn, mock_hostname, mock_getpid):
        """Test instance registration with database error"""
        mock_hostname.return_value = "test-host"
        mock_getpid.return_value = 12345

        mock_cursor = Mock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")

        # Should not raise, just log error
        loader._register_instance("inst_001", "proj_001", 1)

        mock_conn.rollback.assert_called_once()


class TestGetFullContext:
    """Test get_full_context method"""

    @patch.object(SQLiteContextLoader, '_load_priority')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_get_full_context_all_priorities(self, mock_init_db, mock_path, mock_load_priority):
        """Test getting full context for all priorities"""
        def load_priority_side_effect(priority, project_id, phase_id):
            return [{"priority": priority, "content": f"{priority}_data"}]

        mock_load_priority.side_effect = load_priority_side_effect

        loader = SQLiteContextLoader(db_path="test.db")
        result = loader.get_full_context("proj_001", phase_id=1)

        assert "CRITICAL" in result
        assert "HIGH" in result
        assert "MEDIUM" in result
        assert "LOW" in result
        assert len(result["CRITICAL"]) == 1
        assert mock_load_priority.call_count == 4

    @patch.object(SQLiteContextLoader, '_load_priority')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_get_full_context_empty(self, mock_init_db, mock_path, mock_load_priority):
        """Test getting full context with no data"""
        mock_load_priority.return_value = []

        loader = SQLiteContextLoader(db_path="test.db")
        result = loader.get_full_context("proj_002")

        assert all(len(context) == 0 for context in result.values())


class TestClearInstanceTokens:
    """Test clear_instance_tokens method"""

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_clear_tokens_success(self, mock_init_db, mock_path, mock_get_conn):
        """Test successful token clearing"""
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        loader.clear_instance_tokens("inst_001")

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_clear_tokens_error(self, mock_init_db, mock_path, mock_get_conn):
        """Test token clearing with database error"""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        loader.clear_instance_tokens("inst_001")

        mock_conn.rollback.assert_called_once()


class TestUpdateHeartbeat:
    """Test update_heartbeat method"""

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_update_heartbeat_success(self, mock_init_db, mock_path, mock_get_conn):
        """Test successful heartbeat update"""
        mock_cursor = Mock()
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        loader.update_heartbeat("inst_001")

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_update_heartbeat_error(self, mock_init_db, mock_path, mock_get_conn):
        """Test heartbeat update with database error"""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        loader.update_heartbeat("inst_001")

        mock_conn.rollback.assert_called_once()


class TestStoreContext:
    """Test store_context method"""

    @patch('database.sqlite_context_loader.json.dumps')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_store_context_success(self, mock_init_db, mock_path, mock_get_conn, mock_json_dumps):
        """Test successful context storage"""
        mock_json_dumps.return_value = '{"test": "data"}'

        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [5]  # Next sequence number
        mock_cursor.lastrowid = 123
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        snapshot_id = loader.store_context(
            project_id="proj_001",
            content={"test": "data"},
            priority="HIGH",
            content_type="code",
            phase_id=1
        )

        assert snapshot_id == 123
        assert mock_cursor.execute.call_count == 2  # SELECT + INSERT
        mock_conn.commit.assert_called_once()

    @patch('database.sqlite_context_loader.json.dumps')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_store_context_default_priority(self, mock_init_db, mock_path, mock_get_conn, mock_json_dumps):
        """Test storing context with default priority"""
        mock_json_dumps.return_value = '{}'

        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_cursor.lastrowid = 456
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        snapshot_id = loader.store_context(
            project_id="proj_002",
            content={}
        )

        assert snapshot_id == 456

    @patch('database.sqlite_context_loader.json.dumps')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_store_context_error(self, mock_init_db, mock_path, mock_get_conn, mock_json_dumps):
        """Test context storage with database error"""
        mock_json_dumps.return_value = '{}'

        mock_cursor = Mock()
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")

        with pytest.raises(sqlite3.Error):
            loader.store_context(
                project_id="proj_001",
                content={}
            )

        mock_conn.rollback.assert_called_once()


class TestClose:
    """Test close method"""

    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_close_with_connection(self, mock_init_db, mock_path, mock_get_conn):
        """Test closing active connection"""
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        # Establish connection
        loader._get_connection()
        loader._local.conn = mock_conn

        loader.close()

        mock_conn.close.assert_called_once()
        assert loader._local.conn is None

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_close_no_connection(self, mock_init_db, mock_path):
        """Test closing without active connection"""
        loader = SQLiteContextLoader(db_path="test.db")

        # Should not raise
        loader.close()


class TestContextManager:
    """Test context manager protocol"""

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_context_manager_enter(self, mock_init_db, mock_path):
        """Test __enter__ method"""
        loader = SQLiteContextLoader(db_path="test.db")

        result = loader.__enter__()

        assert result is loader

    @patch.object(SQLiteContextLoader, 'close')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_context_manager_exit(self, mock_init_db, mock_path, mock_close):
        """Test __exit__ method"""
        loader = SQLiteContextLoader(db_path="test.db")

        loader.__exit__(None, None, None)

        mock_close.assert_called_once()

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    @patch.object(SQLiteContextLoader, 'close')
    def test_with_statement(self, mock_close, mock_init_db, mock_path):
        """Test using with statement"""
        with SQLiteContextLoader(db_path="test.db") as loader:
            assert loader is not None

        mock_close.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error scenarios"""

    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_empty_instance_id(self, mock_init_db, mock_path):
        """Test with empty instance ID"""
        loader = SQLiteContextLoader(db_path="test.db")

        with patch.object(loader, '_load_priority', return_value=[]):
            with patch.object(loader, '_register_instance'):
                result = loader.load_context_for_instance("", "proj_001", None)

                assert result["instance_id"] == ""

    @patch.object(SQLiteContextLoader, '_load_priority')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_large_context_data(self, mock_init_db, mock_path, mock_load_priority):
        """Test with large context data"""
        large_context = [{"id": i, "data": "x" * 1000} for i in range(100)]
        mock_load_priority.return_value = large_context

        loader = SQLiteContextLoader(db_path="test.db")

        with patch.object(loader, '_register_instance'):
            result = loader.load_context_for_instance("inst_001", "proj_001", None)

            assert len(result["critical_context"]) == 100

    @patch('database.sqlite_context_loader.json.dumps')
    @patch.object(SQLiteContextLoader, '_get_connection')
    @patch('database.sqlite_context_loader.Path')
    @patch.object(SQLiteContextLoader, '_initialize_database')
    def test_store_context_very_large_content(self, mock_init_db, mock_path, mock_get_conn, mock_json_dumps):
        """Test storing very large content"""
        large_content = {"data": "x" * 10000}
        mock_json_dumps.return_value = "x" * 10000

        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_cursor.lastrowid = 789
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        loader = SQLiteContextLoader(db_path="test.db")
        snapshot_id = loader.store_context("proj_001", large_content)

        assert snapshot_id == 789
