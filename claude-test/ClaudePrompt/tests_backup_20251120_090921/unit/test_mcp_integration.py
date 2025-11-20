#!/usr/bin/env python3
"""
Unit Tests for agent_framework/mcp_integration.py
Tests Model Context Protocol integration.

Test Coverage Target: 80%+
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_framework.mcp_integration import (
    MCPConnection,
    MCPIntegration,
    SlackMCPServer,
    GitHubMCPServer,
)


# ==========================================
# MCP CONNECTION TESTS
# ==========================================

class TestMCPConnection:
    """Test MCPConnection dataclass."""

    def test_connection_creation(self):
        """MCPConnection should be created with all fields."""
        conn = MCPConnection(
            server_name="slack",
            endpoint="https://mcp.slack.com/api",
            auth_config={"token": "xoxb-test"},
            available_tools=["search_messages", "send_message"],
            status="connected"
        )

        assert conn.server_name == "slack"
        assert conn.endpoint == "https://mcp.slack.com/api"
        assert conn.status == "connected"
        assert len(conn.available_tools) == 2

    def test_execute_tool_success(self):
        """execute_tool should execute available tool."""
        conn = MCPConnection(
            server_name="github",
            endpoint="https://api.github.com",
            auth_config={"token": "ghp_test"},
            available_tools=["search_repos", "list_issues"]
        )

        result = conn.execute_tool("search_repos", {"query": "python"})

        assert result["server"] == "github"
        assert result["tool"] == "search_repos"
        assert result["status"] == "success"
        assert "timestamp" in result

    def test_execute_tool_unavailable_fails(self):
        """execute_tool should fail for unavailable tool."""
        conn = MCPConnection(
            server_name="slack",
            endpoint="https://mcp.slack.com/api",
            auth_config={"token": "xoxb-test"},
            available_tools=["search_messages"]
        )

        with pytest.raises(ValueError, match="not available"):
            conn.execute_tool("nonexistent_tool", {})


# ==========================================
# MCP INTEGRATION INITIALIZATION TESTS
# ==========================================

class TestMCPIntegrationInit:
    """Test MCPIntegration initialization."""

    def test_init_creates_instance(self):
        """MCPIntegration should initialize."""
        mcp = MCPIntegration()
        assert mcp is not None

    def test_init_registers_default_servers(self):
        """MCPIntegration should register default servers."""
        mcp = MCPIntegration()

        # Should have default servers
        servers = mcp.list_available_servers()
        assert "slack" in servers
        assert "github" in servers
        assert "google_drive" in servers
        assert "asana" in servers

    def test_init_empty_connections(self):
        """MCPIntegration should start with no active connections."""
        mcp = MCPIntegration()
        assert len(mcp.active_connections) == 0

    def test_init_empty_log(self):
        """MCPIntegration should start with empty execution log."""
        mcp = MCPIntegration()
        assert len(mcp.execution_log) == 0


# ==========================================
# REGISTER SERVER TESTS
# ==========================================

class TestRegisterServer:
    """Test register_server method."""

    def test_register_new_server(self):
        """register_server should register new server."""
        mcp = MCPIntegration()

        mcp.register_server("custom", {
            "endpoint": "https://custom.api.com",
            "auth": {"key": "secret"},
            "tools": ["tool1", "tool2"]
        })

        assert "custom" in mcp.list_available_servers()

    def test_register_overwrites_existing(self):
        """register_server should overwrite existing server."""
        mcp = MCPIntegration()

        original_tools = mcp.list_server_tools("slack")

        mcp.register_server("slack", {
            "endpoint": "https://new.endpoint.com",
            "tools": ["new_tool"]
        })

        new_tools = mcp.list_server_tools("slack")
        assert new_tools != original_tools
        assert "new_tool" in new_tools


# ==========================================
# CONNECT TESTS
# ==========================================

class TestConnect:
    """Test connect method."""

    def test_connect_to_registered_server(self):
        """connect should connect to registered server."""
        mcp = MCPIntegration()

        connection = mcp.connect("slack")

        assert isinstance(connection, MCPConnection)
        assert connection.server_name == "slack"
        assert connection.status == "connected"
        assert connection.connected_at is not None

    def test_connect_creates_active_connection(self):
        """connect should add to active_connections."""
        mcp = MCPIntegration()

        mcp.connect("github")

        assert "github" in mcp.active_connections

    def test_connect_reuses_existing_connection(self):
        """connect should reuse existing connection."""
        mcp = MCPIntegration()

        conn1 = mcp.connect("slack")
        conn2 = mcp.connect("slack")

        # Should be same connection
        assert conn1 is conn2

    def test_connect_unregistered_server_fails(self):
        """connect should fail for unregistered server."""
        mcp = MCPIntegration()

        with pytest.raises(ValueError, match="not registered"):
            mcp.connect("nonexistent_server")

    def test_connect_loads_tools(self):
        """connect should load available tools from server config."""
        mcp = MCPIntegration()

        connection = mcp.connect("slack")

        assert len(connection.available_tools) > 0
        assert "search_messages" in connection.available_tools


# ==========================================
# CALL TOOL TESTS
# ==========================================

class TestCallTool:
    """Test call_tool method."""

    def test_call_tool_on_connected_server(self):
        """call_tool should execute tool on connected server."""
        mcp = MCPIntegration()
        mcp.connect("slack")

        result = mcp.call_tool("slack", "search_messages", {"query": "test"})

        assert result["server"] == "slack"
        assert result["tool"] == "search_messages"
        assert result["status"] == "success"

    def test_call_tool_auto_connects(self):
        """call_tool should auto-connect if not connected."""
        mcp = MCPIntegration()

        # Not connected yet
        assert "github" not in mcp.active_connections

        result = mcp.call_tool("github", "search_repos", {"query": "python"})

        # Should have auto-connected
        assert "github" in mcp.active_connections
        assert result["status"] == "success"

    def test_call_tool_logs_success(self):
        """call_tool should log successful execution."""
        mcp = MCPIntegration()

        mcp.call_tool("slack", "search_messages", {"query": "test"})

        assert len(mcp.execution_log) == 1
        assert mcp.execution_log[0]["success"] is True
        assert mcp.execution_log[0]["server"] == "slack"
        assert mcp.execution_log[0]["tool"] == "search_messages"

    def test_call_tool_unavailable_logs_failure(self):
        """call_tool should log failure for unavailable tool."""
        mcp = MCPIntegration()

        with pytest.raises(ValueError):
            mcp.call_tool("slack", "nonexistent_tool", {})

        # Should have logged the failure
        assert len(mcp.execution_log) == 1
        assert mcp.execution_log[0]["success"] is False
        assert "error" in mcp.execution_log[0]

    def test_call_tool_multiple_calls(self):
        """call_tool should handle multiple calls."""
        mcp = MCPIntegration()

        mcp.call_tool("slack", "search_messages", {"query": "test1"})
        mcp.call_tool("github", "search_repos", {"query": "test2"})
        mcp.call_tool("slack", "send_message", {"channel": "general", "text": "hi"})

        assert len(mcp.execution_log) == 3


# ==========================================
# LIST METHODS TESTS
# ==========================================

class TestListMethods:
    """Test list methods."""

    def test_list_available_servers(self):
        """list_available_servers should return all registered servers."""
        mcp = MCPIntegration()

        servers = mcp.list_available_servers()

        assert isinstance(servers, list)
        assert len(servers) >= 4  # At least the default servers
        assert "slack" in servers
        assert "github" in servers

    def test_list_server_tools_existing_server(self):
        """list_server_tools should return tools for server."""
        mcp = MCPIntegration()

        tools = mcp.list_server_tools("slack")

        assert isinstance(tools, list)
        assert len(tools) > 0
        assert "search_messages" in tools

    def test_list_server_tools_nonexistent_fails(self):
        """list_server_tools should fail for nonexistent server."""
        mcp = MCPIntegration()

        with pytest.raises(ValueError, match="not registered"):
            mcp.list_server_tools("nonexistent_server")


# ==========================================
# DISCONNECT TESTS
# ==========================================

class TestDisconnect:
    """Test disconnect methods."""

    def test_disconnect_removes_connection(self):
        """disconnect should remove active connection."""
        mcp = MCPIntegration()
        mcp.connect("slack")

        assert "slack" in mcp.active_connections

        mcp.disconnect("slack")

        assert "slack" not in mcp.active_connections

    def test_disconnect_nonexistent_no_error(self):
        """disconnect should handle nonexistent connection gracefully."""
        mcp = MCPIntegration()

        # Should not raise error
        mcp.disconnect("nonexistent")

    def test_disconnect_all_clears_connections(self):
        """disconnect_all should clear all connections."""
        mcp = MCPIntegration()

        mcp.connect("slack")
        mcp.connect("github")
        mcp.connect("asana")

        assert len(mcp.active_connections) == 3

        mcp.disconnect_all()

        assert len(mcp.active_connections) == 0


# ==========================================
# STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    def test_get_statistics_empty(self):
        """get_statistics should return stats for no executions."""
        mcp = MCPIntegration()

        stats = mcp.get_statistics()

        assert stats["total_calls"] == 0
        assert stats["servers_registered"] >= 4
        assert stats["active_connections"] == 0

    def test_get_statistics_with_executions(self):
        """get_statistics should return execution stats."""
        mcp = MCPIntegration()

        mcp.call_tool("slack", "search_messages", {"query": "test"})
        mcp.call_tool("github", "search_repos", {"query": "python"})

        stats = mcp.get_statistics()

        assert stats["total_calls"] == 2
        assert stats["successful_calls"] == 2
        assert stats["failed_calls"] == 0
        assert stats["success_rate"] == 1.0

    def test_get_statistics_with_failures(self):
        """get_statistics should track failures."""
        mcp = MCPIntegration()

        mcp.call_tool("slack", "search_messages", {"query": "test"})

        try:
            mcp.call_tool("slack", "nonexistent_tool", {})
        except ValueError:
            pass

        stats = mcp.get_statistics()

        assert stats["total_calls"] == 2
        assert stats["successful_calls"] == 1
        assert stats["failed_calls"] == 1
        assert stats["success_rate"] == 0.5

    def test_get_statistics_servers_used(self):
        """get_statistics should track servers used."""
        mcp = MCPIntegration()

        mcp.call_tool("slack", "search_messages", {"query": "test"})
        mcp.call_tool("github", "search_repos", {"query": "python"})

        stats = mcp.get_statistics()

        assert "slack" in stats["servers_used"]
        assert "github" in stats["servers_used"]

    def test_get_statistics_most_used_tools(self):
        """get_statistics should track most used tools."""
        mcp = MCPIntegration()

        # Call same tool multiple times
        for i in range(5):
            mcp.call_tool("slack", "search_messages", {"query": f"test{i}"})

        for i in range(3):
            mcp.call_tool("github", "search_repos", {"query": f"test{i}"})

        stats = mcp.get_statistics()

        assert "most_used_tools" in stats
        assert len(stats["most_used_tools"]) > 0

        # Most used should be slack.search_messages
        top_tool = stats["most_used_tools"][0]
        assert top_tool["tool"] == "slack.search_messages"
        assert top_tool["count"] == 5


# ==========================================
# SLACK MCP SERVER TESTS
# ==========================================

class TestSlackMCPServer:
    """Test SlackMCPServer example implementation."""

    def test_slack_server_initialization(self):
        """SlackMCPServer should initialize with token."""
        server = SlackMCPServer(token="xoxb-test")
        assert server.token == "xoxb-test"

    def test_slack_get_available_tools(self):
        """get_available_tools should return Slack tools."""
        server = SlackMCPServer(token="xoxb-test")

        tools = server.get_available_tools()

        assert isinstance(tools, list)
        assert "search_messages" in tools
        assert "send_message" in tools

    def test_slack_search_messages(self):
        """search_messages should return search results."""
        server = SlackMCPServer(token="xoxb-test")

        result = server.search_messages(query="test", channel="general", limit=10)

        assert isinstance(result, dict)
        assert "matches" in result
        assert "total" in result
        assert result["query"] == "test"

    def test_slack_send_message(self):
        """send_message should return success."""
        server = SlackMCPServer(token="xoxb-test")

        result = server.send_message(channel="general", text="Hello")

        assert result["success"] is True
        assert result["channel"] == "general"
        assert "timestamp" in result


# ==========================================
# GITHUB MCP SERVER TESTS
# ==========================================

class TestGitHubMCPServer:
    """Test GitHubMCPServer example implementation."""

    def test_github_server_initialization(self):
        """GitHubMCPServer should initialize with token."""
        server = GitHubMCPServer(token="ghp_test")
        assert server.token == "ghp_test"

    def test_github_get_available_tools(self):
        """get_available_tools should return GitHub tools."""
        server = GitHubMCPServer(token="ghp_test")

        tools = server.get_available_tools()

        assert isinstance(tools, list)
        assert "search_repos" in tools
        assert "list_issues" in tools

    def test_github_search_repos(self):
        """search_repos should return search results."""
        server = GitHubMCPServer(token="ghp_test")

        result = server.search_repos(query="python", limit=10)

        assert isinstance(result, dict)
        assert "repositories" in result
        assert "total" in result
        assert result["query"] == "python"

    def test_github_list_issues(self):
        """list_issues should return issues."""
        server = GitHubMCPServer(token="ghp_test")

        result = server.list_issues(repo="owner/repo", state="open", limit=50)

        assert isinstance(result, dict)
        assert "issues" in result
        assert "total" in result
        assert result["repo"] == "owner/repo"
        assert result["state"] == "open"


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestMCPIntegrationWorkflows:
    """Test real-world MCP integration scenarios."""

    def test_complete_slack_workflow(self):
        """Test complete Slack integration workflow."""
        mcp = MCPIntegration()

        # Connect to Slack
        connection = mcp.connect("slack")
        assert connection.server_name == "slack"

        # Search messages
        search_result = mcp.call_tool("slack", "search_messages", {
            "query": "deployment",
            "limit": 50
        })
        assert search_result["status"] == "success"

        # Send message
        send_result = mcp.call_tool("slack", "send_message", {
            "channel": "general",
            "text": "Deployment complete"
        })
        assert send_result["status"] == "success"

        # Check statistics
        stats = mcp.get_statistics()
        assert stats["total_calls"] == 2
        assert stats["successful_calls"] == 2

    def test_multi_server_workflow(self):
        """Test using multiple MCP servers."""
        mcp = MCPIntegration()

        # Use Slack
        mcp.call_tool("slack", "search_messages", {"query": "bug"})

        # Use GitHub
        mcp.call_tool("github", "search_repos", {"query": "ultrathink"})

        # Use Google Drive
        mcp.call_tool("google_drive", "search_files", {"query": "specs"})

        # Check statistics
        stats = mcp.get_statistics()
        assert stats["total_calls"] == 3
        assert len(stats["servers_used"]) == 3

    def test_connection_reuse_workflow(self):
        """Test that connections are reused."""
        mcp = MCPIntegration()

        # First call auto-connects
        mcp.call_tool("github", "search_repos", {"query": "test1"})
        assert len(mcp.active_connections) == 1

        # Second call reuses connection
        mcp.call_tool("github", "list_issues", {"repo": "test/repo"})
        assert len(mcp.active_connections) == 1

        # Different server creates new connection
        mcp.call_tool("slack", "search_messages", {"query": "test"})
        assert len(mcp.active_connections) == 2

    def test_error_handling_workflow(self):
        """Test error handling in workflow."""
        mcp = MCPIntegration()

        # Successful call
        mcp.call_tool("slack", "search_messages", {"query": "test"})

        # Failed call (unavailable tool)
        try:
            mcp.call_tool("slack", "nonexistent_tool", {})
        except ValueError:
            pass

        # Another successful call
        mcp.call_tool("github", "search_repos", {"query": "test"})

        # Check statistics
        stats = mcp.get_statistics()
        assert stats["total_calls"] == 3
        assert stats["successful_calls"] == 2
        assert stats["failed_calls"] == 1


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
