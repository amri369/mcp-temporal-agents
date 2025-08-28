from contextlib import AsyncExitStack, asynccontextmanager
from typing import AsyncIterator

from agents import Agent, RunResult

from examples.financial_research_agent.models import FinancialReportData
from examples.financial_research_agent.utils import get_agent, make_server
from examples.financial_research_agent.openai_agents.risk_agent import get_risk_agent
from examples.financial_research_agent.openai_agents.financials_agent import get_financials_agent

@asynccontextmanager
async def get_writer_agent() -> AsyncIterator[Agent]:
    server = make_server()
    async with server as s:
        instructions = await s.get_prompt("writer_prompt")
        prompt_text = instructions.messages[0].content.text
        agent = get_agent(
            name="FinancialWriterAgent",
            instructions=prompt_text,
            mcp_servers=[s],
            output_type=FinancialReportData,
        )
        yield agent

async def _summary_extractor(run_result: RunResult) -> str:
    """Custom output extractor for sub‑agents that return an AnalysisSummary."""
    # The financial/risk analyst agents emit an AnalysisSummary with a `summary` field.
    # We want the tool call to return just that summary text so the writer can drop it inline.
    return str(run_result.final_output.summary)

@asynccontextmanager
async def get_writer_agent_with_tools() -> AsyncIterator[Agent]:
    """
    Clone the writer agent and attach:
      - fundamentals_analysis (backed by FinancialsAnalystAgent)
      - risk_analysis (backed by RiskAnalystAgent)
    Keeps all three agents alive for the duration of the context.
    """
    async with AsyncExitStack() as stack:
        writer_agent = await stack.enter_async_context(get_writer_agent())
        financials_agent = await stack.enter_async_context(get_financials_agent())
        risk_agent = await stack.enter_async_context(get_risk_agent())

        fundamentals_tool = financials_agent.as_tool(
            tool_name="fundamentals_analysis",
            tool_description="Use to get a short write-up of key financial metrics",
            custom_output_extractor=_summary_extractor,
        )
        risk_tool = risk_agent.as_tool(
            tool_name="risk_analysis",
            tool_description="Use to get a short write-up of potential red flags",
            custom_output_extractor=_summary_extractor,
        )

        writer_with_tools = writer_agent.clone(tools=[fundamentals_tool, risk_tool])
        yield writer_with_tools
