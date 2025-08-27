from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, List

from agents import Agent
from agents.mcp import MCPServer, MCPServerStreamableHttp, create_static_tool_filter

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
) -> Agent:

    if mcp_servers:
        return Agent(
                name=name,
                instructions=instructions,
                mcp_servers=mcp_servers,
                output_type=output_type,
            )

    return Agent(name=name, instructions=instructions)

@asynccontextmanager
async def get_agent(
        agents_name: str,
        prompt_name: str,
        output_type: Any
) -> AsyncIterator[Agent]:

    server = make_server()
    async with server as s:
        instructions = await s.session.get_prompt(prompt_name)
        prompt_text = instructions.messages[0].content.text
        agent = get_agent(
            name=agents_name,
            instructions=prompt_text,
            mcp_servers=[s],
            output_type=output_type,
        )

        yield agent
