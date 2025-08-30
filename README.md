# Summary

This project shows how to build **durable AI agents** using four production-grade components:

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — agent runtime and coordination
- [Temporal Python SDK](https://github.com/temporalio/sdk-python) — durable workflows, retries, and long-running tasks
- [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/python-sdk) — standard interface for tools and data sources
- **(Optional)** [Pydantic Logfire](https://pydantic.dev/logfire) — unified observability (logs, traces, metrics) with native LLM & agent instrumentation

If you’re tired of debugging Celery tasks, running into scalability limits, or wrestling with LangGraph dependency issues, this tutorial is for you.

> **What we mean by “durable agents”**  
> Agents whose steps are persisted and replayable, with built-in retries, timeouts, and idempotency—so they survive crashes, restarts, and long-running work.

# 1. Set up your Python environment
```
uv sync
source .venv/bin/activate
```

# 2. Run the MCP FastAPI Server on a custom port
In this example, we package the prompts of [the financial analyst example](https://github.com/openai/openai-agents-python/tree/main/examples/financial_research_agent) in an MCP server.
```
uv run uvicorn examples.mcp_server.main:app --reload --port 9000
```

To inspect and interact with the server, run:
```
mcp dev examples/mcp_server/financial_research_server.py
```
This command shows the available tools, schemas, and prompt interfaces exposed by the MCP server.
# 3. Start a Temporal server
Execute the following commands to start a pre-built image along with all the dependencies.

```bash
brew install temporal
temporal server start-dev
```

# 4. Start a Temporal worker
Execute the following command to start a worker to run the examples. 
Ensure that all your environment variables reside at file .env.

```bash
export PYTHONPATH=.
uv run --env-file .env examples/financial_research_agent/temporal/worker.py
```

# 5. Start the financial analyst agent

```bash
export PYTHONPATH=.
uv run --env-file .env examples/financial_research_agent/main.py
```

# 6. Credit

This example is inspired by these two great examples:
- [Open AI Agents SDK - Financial Research Agent Example](https://github.com/openai/openai-agents-python/tree/main/examples/financial_research_agent)
- [Temporal - Financial Research Example](https://github.com/temporalio/samples-python/tree/main/openai_agents/financial_research_agent)

Readers are invited to visit this [Medium article](https://medium.com/p/c49c928bc4ec) for more details.