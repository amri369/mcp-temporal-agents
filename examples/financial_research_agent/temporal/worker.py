import asyncio

import logfire
from temporalio.client import Client
from temporalio.worker import Worker

from config import settings
from examples.financial_research_agent.temporal.activities import run_agent_activity
from examples.financial_research_agent.temporal.workflows import FinancialResearchWorkflow

if settings.logfire_token:
    logfire.configure(token=settings.logfire_token)
    logfire.instrument_openai_agents()

async def main():
    client = await Client.connect(
        settings.temporal_server_url,
    )

    worker = Worker(
        client,
        task_queue="financial-research-task-queue",
        workflows=[FinancialResearchWorkflow],
        activities=[run_agent_activity],
    )

    print("Starting financial research worker...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())