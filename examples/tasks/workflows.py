import asyncio
from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from financial_agents.models import (
        AgentRunnerParams, AgentsChoices, FinancialSearchPlan
    )
    from tasks.activities import run_agent_activity

@workflow.defn
class FinancialResearchWorkflow:
    @workflow.run
    async def run(self, query: str):
        payload = AgentRunnerParams(
            agent_choice=AgentsChoices.FinancialPlannerAgent,
            message=query
        )
        search_plan = await workflow.execute_activity(
            run_agent_activity,
            payload,
            start_to_close_timeout=timedelta(
                seconds=60
            ),
            schedule_to_close_timeout=timedelta(
                seconds=60
            ),
        )

        search_plan = FinancialSearchPlan(**search_plan)

        return search_plan

        # search_activities = []
        # for search_item in search_plan.searches:
        #     payload = AgentRunnerParams(
        #         agent_choice=AgentsChoices.FinancialSearchAgent,
        #         message=search_item.query
        #     )
        #     search_activities.append(
        #         workflow.execute_activity(
        #             run_agent_activity,
        #             payload,
        #             start_to_close_timeout=timedelta(
        #                 seconds=60
        #             ),
        #             schedule_to_close_timeout=timedelta(
        #                 seconds=60
        #             ),
        #         )
        #     )
        #
        # search_results = await asyncio.gather(*search_activities)
        # return search_results
