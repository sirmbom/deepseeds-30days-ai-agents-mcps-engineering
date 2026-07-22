import os
from typing import List, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# 📐 1. SCHEMA & STATE DEFINITIONS
# ==========================================

class Task(BaseModel):
    """Blueprint for an individual atomic task item."""
    id: int = Field(description="Unique chronological identifier for the step.")
    description: str = Field(description="Clear explanation of the single task action.")
    completed: bool = Field(default=False, description="Track execution completion status.")
    response: Optional[str] = Field(default=None, description="The returned output or error from tool execution.")

class Plan(BaseModel):
    """Blueprint for the macro-level roadmap produced by the Planner."""
    tasks: List[Task] = Field(description="Chronological, sequential list of atomic tasks.")

class AgentState(TypedDict):
    """The shared global memory graph dictionary."""
    user_message: str            # 📥 Entry point request
    plan: List[Task]             # 📋 High-level structured roadmap
    current_step_index: int     # 📍 Pointer to the active target task
    final_response: str         # 📤 Ultimate synthesized response
    loop_count: int             # ⚠️ Safe exit count metric
    error_logs: List[str]       # 🪵 System error collection sink

# ==========================================
# 🧠 2. THE PLANNER NODE (Structured Outputs via Gemini)
# ==========================================

def planner_node(state: AgentState) -> dict:
    # Use gemini-2.5-pro for macro-level tactical planning
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.0)
    
    # Binding our Pydantic Plan class schema directly to Gemini
    structured_llm = llm.with_structured_output(Plan)
    
    system_prompt = (
        "You are a macro-level tactical Planner agent. Your job is to break down a "
        "complex user goal into a strict sequence of atomic, chronological steps. "
        "Each task must perform exactly one function (e.g., search, compute, format)."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["user_message"]}
    ]
    
    generated_plan = structured_llm.invoke(messages)
    
    return {
        "plan": [task.dict() for task in generated_plan.tasks],
        "current_step_index": 0,
        "loop_count": 0,
        "error_logs": []
    }

# ==========================================
# ⚙️ 3. THE EXECUTOR NODE (Using LangGraph Command Pattern)
# ==========================================

def executor_node(state: AgentState) -> Command:
    """Processes active steps and handles implicit routing + error traps."""
    current_idx = state["current_step_index"]
    plan = state["plan"]
    loops = state["loop_count"] + 1
    errors = state["error_logs"].copy()
    
    # ⚠️ Failure Prevention: Max loop gatekeeper guardrail
    if loops > 10:
        errors.append("System force-halted: Max loop safety counter threshold exceeded.")
        return Command(
            update={"loop_count": loops, "error_logs": errors},
            goto="synthesizer"
        )
    
    # Gather target task
    active_task = plan[current_idx]
    
    # --- SIMULATED EXECUTOR TOOL ENGINE EXECUTION LOOP ---
    try:
        # Example Failure Injection Setup for Testing
        if "fail" in active_task["description"].lower():
            raise RuntimeError(f"Simulated Tool Execution Crash at step ID: {active_task['id']}")
            
        # Successful execution generation mock
        execution_result = f"Successfully completed: Executed '{active_task['description']}' seamlessly."
        active_task["response"] = execution_result
        active_task["completed"] = True
        next_idx = current_idx + 1
        
    except Exception as e:
        # 🪵 RESILIENT ERROR TRACKING MECHANISM
        error_msg = f"Task ID {active_task['id']} Failed: {str(e)}"
        errors.append(error_msg)
        
        # Log error trace back directly inside the active task response bucket
        active_task["response"] = f"CRASH: {str(e)}"
        active_task["completed"] = False  # Keep unfulfilled so system can evaluate self-correction
        
        # Route graph directly to the Synthesizer with error logs attached to stop execution safely
        return Command(
            update={"plan": plan, "error_logs": errors, "loop_count": loops},
            goto="synthesizer"
        )
    
    # --- DYNAMIC CONDITIONAL ROUTING DECISION ENGINE ---
    # Check if there are any remaining tasks left unfinished
    all_completed = all(t["completed"] for t in plan)
    
    if all_completed or next_idx >= len(plan):
        return Command(
            update={"plan": plan, "current_step_index": current_idx, "loop_count": loops},
            goto="synthesizer"
        )
    else:
        return Command(
            update={"plan": plan, "current_step_index": next_idx, "loop_count": loops},
            goto="executor"
        )

# ==========================================
# 📤 4. THE SYNTHESIZER NODE
# ==========================================

def synthesizer_node(state: AgentState) -> dict:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # If errors were accumulated along the loop, present a diagnosis report
    if state["error_logs"]:
        formatted_errors = "\n- ".join(state["error_logs"])
        final_summary = (
            f"⚠️ Workflow halted due to execution exceptions:\n\n"
            f"Logged Diagnostics:\n- {formatted_errors}\n\n"
            f"Please verify tool configurations in week2/day11/code/."
        )
        return {"final_response": final_summary}
        
    # Standard successful compilation summary loop
    summary_prompt = (
        f"Review the original goal: '{state['user_message']}'.\n"
        f"Synthesize a clear final summary using the structural data output steps "
        f"provided by our runtime tasks: {state['plan']}"
    )
    
    response = llm.invoke(summary_prompt)
    return {"final_response": response.content}

# ==========================================
# 🧱 5. COMPILING THE STATEGRAPH
# ==========================================

workflow = StateGraph(AgentState)

# Add our custom processing units to our state machine
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("synthesizer", synthesizer_node)

# Set up graph topology configurations
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "executor")
# Note: No explicit conditional edge definitions are needed for "executor" 
# because it uses internal Command routing declarations natively!
workflow.add_edge("synthesizer", END)

app = workflow.compile()

# ==========================================
# 🚀 6. VERIFICATION RUNS
# ==========================================
if __name__ == "__main__":
    print("🤖 Testing Successful Multi-Step Execution Pipeline...")
    success_input = {"user_message": "Fetch data logs, clean missing values, and structure results."}
    for output in app.stream(success_input):
        print(output)
        
    print("\n-------------------------------------\n")
    
    print("🪵 Testing Resilient Error Logging Injection...")
    failure_input = {"user_message": "Fetch data logs, inject a tool failure scenario step here, and structure results."}
    for output in app.stream(failure_input):
        print(output)