from enum import Enum
from pydantic import BaseModel

class AnalysisSummary(BaseModel):
    summary: str
    """Short text summary for this aspect of the analysis."""

class FinancialSearchItem(BaseModel):
    reason: str
    """Your reasoning for why this search is relevant."""

    query: str
    """The search term to feed into a web (or file) search."""

class FinancialSearchPlan(BaseModel):
    searches: list[FinancialSearchItem]
    """A list of searches to perform."""

class VerificationResult(BaseModel):
    verified: bool
    """Whether the report seems coherent and plausible."""

    issues: str
    """If not verified, describe the main issues or concerns."""

class FinancialReportData(BaseModel):
    short_summary: str
    """A short 2‑3 sentence executive summary."""

    markdown_report: str
    """The full markdown report."""

    follow_up_questions: list[str]
    """Suggested follow‑up questions for further research."""

class AgentsChoices(str, Enum):
    FinancialPlannerAgent       = "FinancialPlannerAgent"
    FinancialSearchAgent        = "FinancialSearchAgent"
    FundamentalsAnalystAgent    = "FundamentalsAnalystAgent"
    RiskAnalystAgent            = "RiskAnalystAgent"
    FinancialWriterAgent        = "FinancialWriterAgent"
    VerificationAgent           = "VerificationAgent"

class AgentRunnerParams(BaseModel):
    agent_choice: AgentsChoices
    message: str