# Summary

This project shows how to build **durable AI agents** using three production-grade components:

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — agent runtime and coordination
- [Temporal Python SDK](https://github.com/temporalio/sdk-python) — durable workflows, retries, and long-running tasks
- [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/python-sdk) — standard interface for tools and data sources
- **(Optional)** [Pydantic Logfire](https://pydantic.dev/logfire) — unified observability (logs, traces, metrics) with native LLM & agent instrumentation


This example is inspired by [Temporal’s integration with the OpenAI Agents SDK](https://temporal.io/blog/announcing-openai-agents-sdk-integration) and is accompanied by this [Medium article](https://medium.com/p/c49c928bc4ec/edit).

If you’re tired of debugging Celery tasks, running into scalability limits, or wrestling with LangGraph dependency issues, this tutorial is for you.

> **What we mean by “durable agents”**  
> Agents whose steps are persisted and replayable, with built-in retries, timeouts, and idempotency—so they survive crashes, restarts, and long-running work.

# 1. Set up your Python environment
```
uv sync
source .venv/bin/activate
```

# 2. Run the MCP FastAPI Server on a custom port
```
uvicorn mcp.main:app --reload --port 9000
```