from typing import Any, List

from agents import Agent, Tool
from agents.mcp import MCPServer, MCPServerStreamableHttp, create_static_tool_filter
from agents.model_settings import ModelSettings

from config import settings

mcp_server_url = f"{settings.mcp_server_url}/financials/mcp"

def make_server(tools: List[str] | None = None) -> MCPServerStreamableHttp:
    if tools:
        return MCPServerStreamableHttp(
            name="Streamable HTTP Securities Server",
            params={"url": mcp_server_url},
            tool_filter=create_static_tool_filter(tools),
        )

    else:
        return MCPServerStreamableHttp(
            name="Streamable HTTP Securities Server",
            params={"url": mcp_server_url},
        )

def get_agent(
        *,
        name: str,
        instructions: str,
        mcp_servers: List[MCPServer] | None = None,
        output_type: Any,
        tools: List[Tool | str] | None = None,
) -> Agent:

    if mcp_servers and tools:
        return Agent(
                name=name,
                instructions=instructions,
                mcp_servers=mcp_servers,
                output_type=output_type,
                tools=tools,
                model_settings=ModelSettings(tool_choice="required")
            )

    if mcp_servers:
        return Agent(
                name=name,
                instructions=instructions,
                mcp_servers=mcp_servers,
                output_type=output_type,
            )

    return Agent(name=name, instructions=instructions)
