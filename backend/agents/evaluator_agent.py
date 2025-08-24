from core.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate
import json, os, re

_evaluator = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Evaluator Agent. Analyze the execution output from a machine learning pipeline "
     "and provide a comprehensive summary. Extract performance metrics, highlight key findings, "
     "and provide insights about the model's performance. Return a JSON with fields: "
     "'summary', 'metrics', 'insights', 'recommendations'."),
    ("human", "Execution output:\n{execution_output}")
])

def summarize_and_prepare_ui(execution_stdout: str):
    """
    Parse metrics from stdout and generate comprehensive evaluation summary.
    """
    llm = get_llm()
    
    # Use LLM to analyze the output
    try:
        response = (_evaluator | llm).invoke({"execution_output": execution_stdout}).content
        
        # Clean up markdown if present
        import re
        analysis = re.sub(r'```json\s*', '', response)
        analysis = re.sub(r'```\s*', '', analysis)
        
        evaluation = json.loads(analysis.strip())
    except Exception as e:
        print(f"Evaluator parsing error: {e}")
        # Fallback to basic parsing
        evaluation = _basic_metric_parsing(execution_stdout)
    
    print("=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Summary: {evaluation.get('summary', 'No summary available')}")
    print(f"Metrics: {evaluation.get('metrics', {})}")
    print(f"Insights: {evaluation.get('insights', 'No insights available')}")
    print(f"Recommendations: {evaluation.get('recommendations', 'No recommendations available')}")
    print("=" * 60)
    
    return evaluation

def _basic_metric_parsing(execution_stdout: str):
    """Fallback metric parsing if LLM analysis fails"""
    metrics = {}
    
    # Enhanced metric parsing patterns
    patterns = {
        'accuracy': r"accuracy[:=\s]*([0-9.]+)",
        'f1': r"f1[_\s]*score[:=\s]*([0-9.]+)",
        'precision': r"precision[:=\s]*([0-9.]+)",
        'recall': r"recall[:=\s]*([0-9.]+)",
        'mae': r"mae[:=\s]*([0-9.]+)",
        'rmse': r"rmse[:=\s]*([0-9.]+)",
        'r2': r"r2[:=\s]*([0-9.]+)"
    }
    
    for metric_name, pattern in patterns.items():
        match = re.search(pattern, execution_stdout, re.I)
        if match:
            metrics[metric_name] = float(match.group(1))
    
    return {
        "summary": "Basic metric extraction completed",
        "metrics": metrics,
        "insights": "Model training completed successfully",
        "recommendations": "Review detailed metrics above"
    }
