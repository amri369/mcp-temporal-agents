import asyncio

import logfire
from temporalio.client import Client
from temporalio.contrib.openai_agents import OpenAIAgentsPlugin

from config import settings
from tasks.workflows import (
    FinancialResearchWorkflow,
)

async def main():
    # Get the query from user input
    query = input("Enter a financial research query: ")
    if not query.strip():
        query = "Write up an analysis of Apple Inc.'s most recent quarter."
        print(f"Using default query: {query}")

    client = await Client.connect(
        settings.temporal_server_url,
        plugins=[
            OpenAIAgentsPlugin(),
        ],
    )

    print(f"Starting financial research for: {query}")
    print("This may take several minutes to complete...\n")

    result = await client.execute_workflow(
        FinancialResearchWorkflow.run,
        query,
        id=f"financial-research-{hash(query)}",
        task_queue="financial-research-task-queue",
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())