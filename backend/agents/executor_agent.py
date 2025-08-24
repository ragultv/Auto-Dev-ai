import os, subprocess, textwrap, uuid, shlex

def _write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def execute_generated_code(code: str, project_dir: str):
    """
    Saves generated code to project directory, executes in a subprocess,
    returns success flag, stdout, stderr.
    """
    code_dir = os.path.join(project_dir, "code")
    os.makedirs(code_dir, exist_ok=True)
    code_path = os.path.join(code_dir, "ml_pipeline.py")
    _write_file(code_path, code)

    # Use absolute path to avoid issues
    abs_code_path = os.path.abspath(code_path)
    print(f"📁 Project directory: {project_dir}")
    print(f"▶️ Executing code at: {abs_code_path}")
    
    # For Windows, we need to be more careful with paths
    if os.name == 'nt':  # Windows
        cmd = f'python "{abs_code_path}"'
    else:
        cmd = f"python {shlex.quote(abs_code_path)}"
    
    try:
        # Set working directory to project directory
        print(f"🔄 Running command: {cmd}")
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=1800, cwd=project_dir)
        
        print(f"✅ Process completed with return code: {proc.returncode}")
        if proc.stdout:
            print(f"📤 STDOUT:\n{proc.stdout}")
        if proc.stderr:
            print(f"❌ STDERR:\n{proc.stderr}")
            
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }
    except subprocess.TimeoutExpired:
        print("⏰ Execution timed out")
        return {"success": False, "stdout": "", "stderr": "Execution timed out"}
    except Exception as e:
        print(f"💥 Exception during execution: {e}")
        return {"success": False, "stdout": "", "stderr": str(e)}
