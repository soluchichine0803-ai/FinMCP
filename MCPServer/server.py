from mcp.server import MCPServer

mcp = MCPServer("FastBank")


@mcp.tool()
def ping() -> str:
    """Check whether the FastBank MCP server is running."""
    return "FastBank MCP is online."


if __name__ == "__main__":
    mcp.run(transport="stdio")
