import os
from typing import List, Optional, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

class Task(BaseModel):
    id: int = Field(description="Unique chronological identifier for the task.")
    name: str = Field(description="Clear, descriptive instruction for what action to perform.")
    completed: bool = Field(default=False, description="Tracking flag for execution status.")
    response: str = Field(default="", description="The text result or tool output generated for this task.")

class Plan(BaseModel):
    tasks: List[Task] = Field(description="The chronological checklist of subtasks needed to reach the goal.")

# Graph Global Memory State
class AgentState(TypedDict):
    user_message: str
    plan: List[Task]
    current_step_index: int
    final_response: Optional[str]
    loop_count: int  # Edge-case safety counter

# Defining the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# Passing the Plan and Task structure to the LLM
planner_llm = llm.with_structured_output(Plan)

def planner_node(state: AgentState):
    """The macro-thinker that builds the task checklist."""
    system_prompt = (
        "You are an expert Planner Agent. Your job is to break down a user's complex "
        "request into a highly deterministic, logical sequence of atomic, chronological steps. "
        "Each task must do exactly ONE thing (e.g., search, fetch, compute, or write)."
    )

    structured_plan = planner_llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["user_message"]}
    ])

    return {
        "plan": structured_plan.tasks,
        "current_step_index": 0,
        "loop_count": 0
    }

def executor_node(state: AgentState) -> Command[Literal["executor", "synthesizer"]]:
    """Processes the current task and dynamically handles routing via Command."""
    plan = state["plan"]
    idx = state["current_step_index"]
    loop_count = state["loop_count"] + 1

    if loop_count > 10:
        return Command(
            update={"final_response": "Max runs achieved. Exiting for safety reasons."},
            goto="synthesizer"
        )
    
    current_task = plan[idx]
    print(f"⚙️ Running Task [{current_task.id}]: {current_task.name}")

    # In a real setup, parse current_task.name and execute actual tools here
    simulated_tool_output = f"Successfully processed tool execution for: '{current_task.name}'"

    current_task.completed = True
    current_task.response = simulated_tool_output
    plan[idx] = current_task

    next_idx = idx + 1
    if next_idx < len(plan):
        return Command(
            update={
                "plan": plan,
                "current_step_index": next_idx,
                "loop_count": loop_count
            },
            goto="executor"
        )
    else:
        return Command(
            update={
                "plan": plan,
                "loop_count": loop_count
            },
            goto="synthesizer"
        )

def synthesizer_node(state: AgentState):
    """Gathers all executed responses and formats the final summary delivery."""
    if "Execution halted" in state.get("final_response", ""):
        return {"final_response": state["final_response"]}
        
    print("🧠 Synthesizing final response...")
    history_summary = "\n".join([f"- Task: {t.name}\n Result: {t.response}" for t in state["plan"]])

    prompt = f"The user asked: {state['user_message']}\n\nHere are the results of the actions taken:\n{history_summary}\n\nFormulate a complete, well-structured final answer."
    response = llm.invoke(prompt)

    return {"final_response": response.content}

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("synthesizer", synthesizer_node)

# Set up Core Transitions
builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_edge("synthesizer", END)

# Compile
graph = builder.compile()

# ==========================================
# 5. TEST THE WORKFLOW
# ==========================================
if __name__ == "__main__":
    inputs = {"user_message": "Fetch the 2026 AI industry trend logs, extract the metadata, and write a summary."}
    for event in graph.stream(inputs):
        print(event)