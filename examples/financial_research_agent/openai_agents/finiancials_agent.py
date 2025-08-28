from contextlib import asynccontextmanager
from typing import AsyncIterator

from agents import Agent

from examples.financial_research_agent.models import FinancialSearchPlan
from examples.financial_research_agent.utils import get_agent, make_server

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
