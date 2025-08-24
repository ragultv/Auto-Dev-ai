from typing import TypedDict, Optional, Dict, Any

class WorkflowState(TypedDict, total=False):
    user_prompt: str
    plan: str
    dataset: Dict[str, Any]
    code: str
    results: Dict[str, Any]
    error: Optional[str]
    summary: Dict[str, Any]
    project_dir: str


from agents.master_agent import master_plan
from agents.research_agent import research_dataset
from agents.coder_agent import generate_training_code
from agents.executor_agent import execute_generated_code
from agents.debug_agent import rewrite_on_error
from agents.evaluator_agent import summarize_and_prepare_ui

import os, datetime

def create_project_structure_node(state: WorkflowState) -> WorkflowState:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"project_{timestamp}"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_dir = os.path.join(base_dir, "projects", project_name)
    os.makedirs(os.path.join(project_dir, "dataset"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "models"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "artifacts"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "code"), exist_ok=True)
    state["project_dir"] = project_dir
    return state

def master_node(state: WorkflowState) -> WorkflowState:
    state["plan"] = master_plan(state["user_prompt"])
    return state

def research_node(state: WorkflowState) -> WorkflowState:
    state["dataset"] = research_dataset(state["plan"])
    return state

def coder_node(state: WorkflowState) -> WorkflowState:
    state["code"] = generate_training_code(state["plan"], state["dataset"], state["project_dir"])
    return state

def executor_node(state: WorkflowState) -> WorkflowState:
    res = execute_generated_code(state["code"], state["project_dir"])
    state["results"] = res
    if not res["success"]:
        state["error"] = res.get("stderr") or res.get("stdout", "Unknown error")
    return state

def debug_node(state: WorkflowState) -> WorkflowState:
    state["code"] = rewrite_on_error(state["code"], state.get("error", ""))
    return state

def evaluator_node(state: WorkflowState) -> WorkflowState:
    summary = summarize_and_prepare_ui(state["results"]["stdout"])
    state["summary"] = summary
    return state

from langgraph.graph import StateGraph, END, START


# -----------------
# Build Workflow Graph
# -----------------
graph = StateGraph(WorkflowState)

graph.add_node("project_setup", create_project_structure_node)
graph.add_node("master", master_node)
graph.add_node("research", research_node)
graph.add_node("coder", coder_node)
graph.add_node("executor", executor_node)
graph.add_node("debug", debug_node)
graph.add_node("evaluator", evaluator_node)

# Entry point
graph.add_edge(START, "project_setup")
   # ✅ REQUIRED

# Normal flow
graph.add_edge("project_setup", "master")
graph.add_edge("master", "research")
graph.add_edge("research", "coder")
graph.add_edge("coder", "executor")

# Conditional route: executor → evaluator or debug
def route_on_execution(state: WorkflowState) -> str:
    return "debug" if not state["results"].get("success") else "evaluator"

graph.add_conditional_edges(
    "executor", 
    route_on_execution, 
    {"debug": "debug", "evaluator": "evaluator"}
)

# After debug, go back to executor
graph.add_edge("debug", "executor")

# End
graph.add_edge("evaluator", END)

# Compile
app = graph.compile()
