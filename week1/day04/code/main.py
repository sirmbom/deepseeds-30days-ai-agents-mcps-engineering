from typing import TypedDict, List

class ResearchState(TypedDict):
    query: str
    search_results: List[str]
    summary: str
    fact_check_passed: bool
    final_response: str


def search_node(state: ResearchState):
    print("SEARCHING...")
    user_query = state["query"]

    results = [f"Result 1 for {user_query}", f"Result 2 for {user_query}"]
    return {"search_results": results}

def summarize_node(state: ResearchState):
    print("SUMMARIZING...")
    results = state["search_results"]

    summary="AI summary here"
    return {"summary": summary}

def fact_check_node(state: ResearchState):
    print("FACT-CHECKING...")
    summary = state["summary"]

    passed = True
    return {"fact_check_passed": passed}

def respond_node(state: ResearchState):
    print("GENERATING RESPONSE...")
    return {"final_response": f"Here is the verified result: {state['summary']}"}

def route_after_checking(state: ResearchState) -> str:
    if state["fact_check_passed"]:
        return "response"
    else:
        return "search"


from langgraph.graph import START, END, StateGraph

workflow = StateGraph(ResearchState)

workflow.add_node("search",search_node)
workflow.add_node("summarize",summarize_node)
workflow.add_node("fact_check",fact_check_node)
workflow.add_node("respond",respond_node)

workflow.add_edge(START,"search")
workflow.add_edge("search","summarize")
workflow.add_edge("summarize","fact_check")
workflow.add_conditional_edges(
    "fact_check", route_after_checking,
    {
        "response": "respond",
        "search": "search"
    }
)
workflow.add_edge("respond", END)

app = workflow.compile()