import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from examples.financial_research_agent.models import (
        AgentRunnerParams, AgentsChoices,
        FinancialSearchPlan, FinancialReportData,
        VerificationResult, FinancialReportWorkflowOutput
    )
    from examples.financial_research_agent.temporal.activities import run_agent_activity

RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=5,
)
ACTIVITY_OPTS = dict(
    start_to_close_timeout=timedelta(seconds=60),
    schedule_to_close_timeout=timedelta(seconds=60),
    retry_policy=RETRY_POLICY,
)

@workflow.defn
class FinancialResearchWorkflow:
    @workflow.run
    async def run(self, query: str) -> FinancialReportWorkflowOutput:
        payload = AgentRunnerParams(
            agent_choice=AgentsChoices.FinancialPlannerAgent,
            message=query
        )
        search_plan = await workflow.execute_activity(
            run_agent_activity,
            payload,
            **ACTIVITY_OPTS,
        )

        search_plan = FinancialSearchPlan(**search_plan)

        search_activities = []
        for search_item in search_plan.searches:
            payload = AgentRunnerParams(
                agent_choice=AgentsChoices.FinancialSearchAgent,
                message=search_item.query
            )
            search_activities.append(
                workflow.execute_activity(
                    run_agent_activity,
                    payload,
                    **ACTIVITY_OPTS,
                )
            )

        search_results = await asyncio.gather(*search_activities)

        payload = AgentRunnerParams(
            agent_choice=AgentsChoices.FinancialWriterAgent,
            message=str(search_results)
        )
        report = await workflow.execute_activity(
            run_agent_activity,
            payload,
            **ACTIVITY_OPTS,
        )

        report = FinancialReportData(**report)
        payload = AgentRunnerParams(
            agent_choice=AgentsChoices.VerificationAgent,
            message=str(report)
        )
        verification = await workflow.execute_activity(
            run_agent_activity,
            payload,
            **ACTIVITY_OPTS,
        )

        verification = VerificationResult(**verification)

        print("\n\n=====REPORT=====\n\n")
        print(f"Report:\n{report.markdown_report}")
        print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        print("\n".join(report.follow_up_questions))
        print("\n\n=====VERIFICATION=====\n\n")
        print(verification)

        return FinancialReportWorkflowOutput(
            search_plan=search_plan,
            report=report,
            verification=verification,
        )
