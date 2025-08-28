from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, List

from agents import Agent, Tool
from agents.mcp import MCPServer, MCPServerStreamableHttp, create_static_tool_filter
from agents.model_settings import ModelSettings

from config import settings
from financial_agents.models import (
    AnalysisSummary, FinancialSearchPlan,
    VerificationResult, FinancialReportData
)

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

@asynccontextmanager
async def get_mcp_agent(
        agent_name: str,
        prompt_name: str,
        output_type: Any = None,
        tools: List[Tool | str] | None = None,
) -> AsyncIterator[Agent]:

    server = make_server()
    async with server as s:
        instructions = await s.session.get_prompt(prompt_name)
        prompt_text = instructions.messages[0].content.text
        agent = get_agent(
            name=agent_name,
            instructions=prompt_text,
            mcp_servers=[s],
            output_type=output_type,
            tools=tools
        )

        yield agent

@asynccontextmanager
async def get_financial_planner_agent() -> AsyncIterator[Agent]:
    server = make_server()
    async with server as s:
        instructions = await s.session.get_prompt("planner_prompt")
        prompt_text = instructions.messages[0].content.text
        agent = get_agent(
            name="FinancialPlannerAgent Agent",
            instructions=prompt_text,
            mcp_servers=[s],
            output_type=FinancialSearchPlan,
        )
        yield agent
