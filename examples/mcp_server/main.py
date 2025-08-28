import contextlib
from fastapi import FastAPI

from examples.mcp_server.financial_research_server import mcp as mcp_server

@contextlib.asynccontextmanager
async def lifespan(app_: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_server.session_manager.run())
        yield
app = FastAPI(lifespan=lifespan)
app.mount("/financials", mcp_server.streamable_http_app())
