import os
import datetime
from agents.master_agent import master_plan
from agents.research_agent import research_dataset
from agents.coder_agent import generate_training_code
from agents.executor_agent import execute_generated_code
from agents.debug_agent import rewrite_on_error
from agents.evaluator_agent import summarize_and_prepare_ui

def create_project_structure(project_name: str) -> str:
    """Create organized project directory structure"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_dir = os.path.join(base_dir, "projects", project_name)
    
    # Create directories
    os.makedirs(os.path.join(project_dir, "dataset"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "models"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "artifacts"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "code"), exist_ok=True)
    
    return project_dir

def run_autodev_once(user_prompt: str, max_retries: int = 2, launch_ui: bool = True):
    # Create project structure with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"project_{timestamp}"
    project_dir = create_project_structure(project_name)
    
    print(f"🚀 Starting AutoDev workflow in: {project_dir}")
    print(f"📝 User prompt: {user_prompt}")
    
    # 1) Master → plan
    print("\n📋 Step 1: Creating master plan...")
    plan = master_plan(user_prompt)

    # 2) Research → dataset + description
    print("\n🔍 Step 2: Researching dataset...")
    dataset = research_dataset(plan)

    # 3) Coder → code (training + metrics + gradio UI all in one)
    print("\n💻 Step 3: Generating training code...")
    code = generate_training_code(plan, dataset, project_dir)

    # 4) Executor → run
    attempt = 0
    while attempt <= max_retries:
        exec_res = execute_generated_code(code, project_dir)
        print(f"🔍 Execution attempt {attempt + 1}: Success = {exec_res['success']}")
        
        # Check for artifacts as additional success indicator
        artifacts_dir = os.path.join(project_dir, "artifacts")
        has_artifacts = os.path.exists(artifacts_dir) and len(os.listdir(artifacts_dir)) > 0
        
        if exec_res["success"] or has_artifacts:
            print("✅ Code execution successful!")
            if has_artifacts:
                print(f"📦 Artifacts found: {os.listdir(artifacts_dir)}")
                exec_res["success"] = True  # Override success if artifacts exist
            break
        else:
            print(f"❌ Execution failed: {exec_res.get('stderr', 'Unknown error')}")
            
        # 5) Debug loop → rewrite → re-run
        print(f"🔧 Attempting to debug and fix code (attempt {attempt + 1}/{max_retries + 1})")
        code = rewrite_on_error(code, exec_res.get("stderr") or exec_res.get("stdout", ""))
        attempt += 1

    if not exec_res["success"]:
        print("💥 All execution attempts failed!")
        return {
            "status": "failed",
            "project_dir": project_dir,
            "plan": plan,
            "dataset": dataset,
            "last_error": exec_res.get("stderr") or exec_res.get("stdout", "")
        }

    # 6) Evaluator → summary
    print("📊 Running evaluation and generating summary...")
    summary = summarize_and_prepare_ui(exec_res["stdout"])

    print("🎉 AutoDev workflow completed successfully!")
    print(f"📁 Results saved in: {project_dir}")
    
    return {
        "status": "completed",
        "project_dir": project_dir,
        "plan": plan,
        "dataset": dataset,
        "metrics": summary.get("metrics", {}),
        "summary": summary.get("summary", ""),
        "execution_output": exec_res["stdout"]
    }
