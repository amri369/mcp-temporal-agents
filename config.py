from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    logfire_token:          str | None = Field(..., alias="LOGFIRE_TOKEN")
    mcp_server_url:         str | None = Field(..., alias="MCP_SERVER_URL")
    openai_api_key:         str | None = Field(..., alias="OPENAI_API_KEY")
    temporal_server_url:    str | None = Field(..., alias="TEMPORAL_SERVER_URL")

settings = Settings()
