from agents import Agent, Runner
from temporalio import workflow

@workflow.defn
class AgentWorkflow:
   @workflow.run
   async def run(self, prompt_name: str) -> str:
       pass