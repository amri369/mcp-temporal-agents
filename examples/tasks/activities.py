from functools import partial
from temporalio import activity
from agents import Runner, WebSearchTool
from financial_agents.helpers import get_mcp_agent, get_financial_planner_agent
from financial_agents.models import (
    AgentRunnerParams, AnalysisSummary, FinancialSearchPlan,
    VerificationResult, FinancialReportData
)

agents_mapper = {
    "FinancialPlannerAgent": get_financial_planner_agent(),
    "FinancialSearchAgent": partial(
        get_mcp_agent,
        agent_name="FinancialSearchAgent",
        prompt_name="search_prompt",
        tools=[WebSearchTool()],
        output_type=AnalysisSummary,
    ),
    "FundamentalsAnalystAgent": partial(
        get_mcp_agent,
        agent_name="FundamentalsAnalystAgent",
        prompt_name="financials_prompt",
        output_type=AnalysisSummary,
    ),
    "RiskAnalystAgent": partial(
        get_mcp_agent,
        agent_name="RiskAnalystAgent",
        prompt_name="risk_prompt",
        output_type=AnalysisSummary,
    ),
    "FinancialWriterAgent": partial(
        get_mcp_agent,
        agent_name="FinancialWriterAgent",
        prompt_name="writer_prompt",
        output_type=FinancialReportData,
    ),
    "VerificationAgent": partial(
        get_mcp_agent,
        agent_name="VerificationAgent",
        prompt_name="verifier_prompt",
        output_type=VerificationResult,
    ),
}

@activity.defn
async def run_agent_activity(params: AgentRunnerParams):
    async with agents_mapper[params.agent_choice] as agent:
        activity.logger.info(
            f"Running agent: {params.agent_choice}"
        )
        result = await Runner.run(starting_agent=agent, input=params.message)
        return result.final_output
