from temporalio import activity
from agents import Runner
from examples.financial_research_agent.openai_agents.planner_agent import get_planner_agent
from examples.financial_research_agent.openai_agents.search_agent import get_search_agent
from examples.financial_research_agent.openai_agents.writer_agent import get_writer_agent_with_tools
from examples.financial_research_agent.openai_agents.verifier_agent import get_verification_agent
from examples.financial_research_agent.models import AgentRunnerParams

agents_mapper = {
    "FinancialPlannerAgent": get_planner_agent,
    "FinancialSearchAgent": get_search_agent,
    "FinancialWriterAgent": get_writer_agent_with_tools,
    "VerificationAgent": get_verification_agent,
}

@activity.defn
async def run_agent_activity(params: AgentRunnerParams):
    factory = agents_mapper[params.agent_choice]
    async with factory() as agent:
        activity.logger.info(f"Running agent: {params.agent_choice}")
        result = await Runner.run(starting_agent=agent, input=params.message)
        return result.final_output
