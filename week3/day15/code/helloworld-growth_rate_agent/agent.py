from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import AgentTool, google_search

def calculate_growth_rate(initial_value: float, final_value: float, periods: int) -> float:
    """
    Calculates the Compounded Annual Growth Rate (CAGR) for financial metrics.
    
    Args:
        initial_value: The baseline starting value.
        final_value: The ending value.
        periods: The number of years/periods elapsed.
    """
    if initial_value <= 0 or periods <= 0:
        return 0.0
    return ((final_value / initial_value) ** (1 / periods)) - 1

search_agent = Agent(
    name="search_specialist",
    model=Gemini(model="gemini-2.5-flash", use_interactions_api=True),
    description="Specialist for querying live web data.",
    tools=[google_search]
)

root_agent = Agent(
    name="financial_researcher",
    model=Gemini(model="gemini-2.5-flash", use_interactions_api=True),
    description="Agent for calculating and searching financial trends.",
    instruction="You are a meticulous financial analyst. Always verify metrics and provide calculations alongside web search data.",
    tools=[calculate_growth_rate, AgentTool(agent=search_agent)]
)