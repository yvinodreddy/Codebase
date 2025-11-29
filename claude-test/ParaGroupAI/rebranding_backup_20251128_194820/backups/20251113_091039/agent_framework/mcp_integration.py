"""
Model Context Protocol (MCP) Integration
Standardized integrations to external services

MCP provides pre-built connectors for common services (Slack, GitHub, etc.)
with automatic OAuth handling and standardized APIs.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class MCPConnection:
    """Connection to an MCP server"""
    server_name: str
    endpoint: str
    auth_config: Dict[str, Any]
    available_tools: List[str] = field(default_factory=list)
    status: str = "initialized"
    connected_at: Optional[str] = None

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute tool on MCP server.

        Args:
            tool_name: Name of tool to execute
            params: Parameters for the tool

        Returns:
            Tool execution result
        """
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available on server '{self.server_name}'")

        logger.info(f"Executing {self.server_name}.{tool_name} with params: {list(params.keys())}")

        # In production, this would make actual API call
        # For now, return mock result
        return {
            "server": self.server_name,
            "tool": tool_name,
            "status": "success",
            "result": f"Mock result from {tool_name}",
            "timestamp": datetime.now().isoformat()
        }


class MCPIntegration:
    """
    Model Context Protocol integration manager.

    MCP provides standardized integrations to external services:
    - Slack (messaging, search)
    - GitHub (repos, issues, PRs)
    - Google Drive (files, docs)
    - Asana (tasks, projects)
    - And many more...

    Benefits:
    - No custom integration code needed
    - Automatic OAuth handling
    - Standardized API across services
    - Pre-built, maintained connectors

    Example:
        >>> mcp = MCPIntegration()
        >>> mcp.register_server("slack", {
        ...     "endpoint": "https://mcp.slack.com",
        ...     "auth": {"token": "xoxb-..."}
        ... })
        >>> results = mcp.call_tool("slack", "search_messages", {
        ...     "query": "project X",
        ...     "limit": 10
        ... })
    """

    def __init__(self):
        """Initialize MCP integration"""
        self.servers: Dict[str, Dict[str, Any]] = {}
        self.active_connections: Dict[str, MCPConnection] = {}
        self.execution_log: List[Dict[str, Any]] = []

        # Register default servers (if available)
        self._register_default_servers()

        logger.info("MCPIntegration initialized")

    def _register_default_servers(self):
        """Register commonly used MCP servers"""
        # These would be loaded from config in production

        default_servers = {
            "slack": {
                "endpoint": "https://mcp.slack.com/api",
                "auth_type": "oauth",
                "tools": [
                    "search_messages",
                    "send_message",
                    "list_channels",
                    "get_user_info",
                    "get_channel_history"
                ]
            },
            "github": {
                "endpoint": "https://mcp.github.com/api",
                "auth_type": "oauth",
                "tools": [
                    "search_repos",
                    "list_issues",
                    "create_issue",
                    "get_pull_requests",
                    "search_code"
                ]
            },
            "google_drive": {
                "endpoint": "https://mcp.googleapis.com/drive",
                "auth_type": "oauth",
                "tools": [
                    "search_files",
                    "get_file",
                    "list_folder",
                    "create_doc",
                    "share_file"
                ]
            },
            "asana": {
                "endpoint": "https://mcp.asana.com/api",
                "auth_type": "oauth",
                "tools": [
                    "list_tasks",
                    "create_task",
                    "get_project",
                    "search_tasks",
                    "assign_task"
                ]
            }
        }

        for name, config in default_servers.items():
            self.servers[name] = config

        logger.info(f"Registered {len(default_servers)} default MCP servers")

    def register_server(
        self,
        name: str,
        server_config: Dict[str, Any]
    ):
        """
        Register MCP server.

        Args:
            name: Server identifier (e.g., "slack", "github")
            server_config: Configuration dict with:
                - endpoint: str (API endpoint)
                - auth: dict (authentication config)
                - tools: list (available tools)
        """
        self.servers[name] = server_config
        logger.info(f"Registered MCP server: {name}")

    def connect(self, server_name: str) -> MCPConnection:
        """
        Connect to MCP server.

        Args:
            server_name: Name of registered server

        Returns:
            MCPConnection instance
        """
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not registered")

        if server_name in self.active_connections:
            logger.debug(f"Reusing existing connection to {server_name}")
            return self.active_connections[server_name]

        config = self.servers[server_name]

        # Create connection
        connection = MCPConnection(
            server_name=server_name,
            endpoint=config["endpoint"],
            auth_config=config.get("auth", {}),
            available_tools=config.get("tools", []),
            status="connected",
            connected_at=datetime.now().isoformat()
        )

        self.active_connections[server_name] = connection

        logger.info(
            f"Connected to {server_name} "
            f"({len(connection.available_tools)} tools available)"
        )

        return connection

    def call_tool(
        self,
        server_name: str,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Any:
        """
        Call tool on MCP server.

        Args:
            server_name: Server identifier
            tool_name: Tool to execute
            params: Tool parameters

        Returns:
            Tool execution result

        Example:
            >>> mcp.call_tool("slack", "search_messages", {
            ...     "query": "project X",
            ...     "channel": "general",
            ...     "limit": 50
            ... })
        """
        # Connect if not already connected
        if server_name not in self.active_connections:
            self.connect(server_name)

        connection = self.active_connections[server_name]

        # Execute tool
        logger.info(f"Calling {server_name}.{tool_name}...")

        try:
            result = connection.execute_tool(tool_name, params)

            # Log execution
            self.execution_log.append({
                "server": server_name,
                "tool": tool_name,
                "params": params,
                "success": True,
                "timestamp": datetime.now().isoformat()
            })

            return result

        except Exception as e:
            logger.error(f"Failed to execute {server_name}.{tool_name}: {e}")

            # Log failure
            self.execution_log.append({
                "server": server_name,
                "tool": tool_name,
                "params": params,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

            raise

    def list_available_servers(self) -> List[str]:
        """List all registered servers"""
        return list(self.servers.keys())

    def list_server_tools(self, server_name: str) -> List[str]:
        """List tools available on a server"""
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not registered")

        return self.servers[server_name].get("tools", [])

    def disconnect(self, server_name: str):
        """Disconnect from server"""
        if server_name in self.active_connections:
            del self.active_connections[server_name]
            logger.info(f"Disconnected from {server_name}")

    def disconnect_all(self):
        """Disconnect from all servers"""
        count = len(self.active_connections)
        self.active_connections.clear()
        logger.info(f"Disconnected from {count} servers")

    def get_statistics(self) -> Dict[str, Any]:
        """Get MCP usage statistics"""
        if not self.execution_log:
            return {
                "total_calls": 0,
                "servers_registered": len(self.servers),
                "active_connections": len(self.active_connections)
            }

        return {
            "total_calls": len(self.execution_log),
            "successful_calls": sum(1 for log in self.execution_log if log["success"]),
            "failed_calls": sum(1 for log in self.execution_log if not log["success"]),
            "success_rate": sum(1 for log in self.execution_log if log["success"]) / len(self.execution_log),
            "servers_used": list(set(log["server"] for log in self.execution_log)),
            "most_used_tools": self._get_most_used_tools(),
            "servers_registered": len(self.servers),
            "active_connections": len(self.active_connections)
        }

    def _get_most_used_tools(self) -> List[Dict[str, Any]]:
        """Get most frequently used tools"""
        tool_counts = {}

        for log in self.execution_log:
            key = f"{log['server']}.{log['tool']}"
            tool_counts[key] = tool_counts.get(key, 0) + 1

        # Sort by count
        sorted_tools = sorted(
            tool_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"tool": tool, "count": count}
            for tool, count in sorted_tools[:10]
        ]


# Example MCP Server Implementations

class SlackMCPServer:
    """Example MCP server for Slack integration"""

    def __init__(self, token: str):
        self.token = token

    def get_available_tools(self) -> List[str]:
        """List available tools"""
        return [
            "search_messages",
            "send_message",
            "list_channels",
            "get_user_info"
        ]

    def search_messages(
        self,
        query: str,
        channel: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search Slack messages.

        Args:
            query: Search query
            channel: Optional channel filter
            limit: Max results

        Returns:
            Search results
        """
        # In production, would call Slack API
        return {
            "matches": [],
            "total": 0,
            "query": query
        }

    def send_message(
        self,
        channel: str,
        text: str
    ) -> Dict[str, Any]:
        """Send message to channel"""
        # In production, would call Slack API
        return {
            "success": True,
            "channel": channel,
            "timestamp": datetime.now().isoformat()
        }


class GitHubMCPServer:
    """Example MCP server for GitHub integration"""

    def __init__(self, token: str):
        self.token = token

    def get_available_tools(self) -> List[str]:
        """List available tools"""
        return [
            "search_repos",
            "list_issues",
            "create_issue",
            "get_pull_requests"
        ]

    def search_repos(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search GitHub repositories"""
        # In production, would call GitHub API
        return {
            "repositories": [],
            "total": 0,
            "query": query
        }

    def list_issues(
        self,
        repo: str,
        state: str = "open",
        limit: int = 50
    ) -> Dict[str, Any]:
        """List issues for repository"""
        # In production, would call GitHub API
        return {
            "issues": [],
            "total": 0,
            "repo": repo,
            "state": state
        }


if __name__ == "__main__":
    # Example usage
    mcp = MCPIntegration()

    print("=" * 60)
    print("MCP INTEGRATION EXAMPLE")
    print("=" * 60)

    # List available servers
    print("\nAvailable MCP servers:")
    for server in mcp.list_available_servers():
        tools = mcp.list_server_tools(server)
        print(f"  - {server} ({len(tools)} tools)")

    # Example: Call Slack tool
    print("\n1. Calling Slack search_messages...")
    result = mcp.call_tool("slack", "search_messages", {
        "query": "project X",
        "limit": 10
    })
    print(f"   Result: {result['status']}")

    # Example: Call GitHub tool
    print("\n2. Calling GitHub search_repos...")
    result = mcp.call_tool("github", "search_repos", {
        "query": "swarmcare"
    })
    print(f"   Result: {result['status']}")

    # Example: Call Google Drive tool
    print("\n3. Calling Google Drive search_files...")
    result = mcp.call_tool("google_drive", "search_files", {
        "query": "specifications"
    })
    print(f"   Result: {result['status']}")

    # Show statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    stats = mcp.get_statistics()
    print(json.dumps(stats, indent=2))

    # Disconnect
    mcp.disconnect_all()
    print("\n✅ Example complete")
