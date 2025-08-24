from core.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate

_research = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Research Agent. For the given problem, propose 1-2 public datasets "
     "(Hugging Face Datasets preferred), include: name, task type, target variable, "
     "feature summary, download snippet (datasets.load_dataset), license notes. "
     "Output strict JSON: {{\"dataset\": {{\"name\": \"...\", \"hf_id\": \"...\", \"task\": \"...\", \"target\": \"...\", \"features\": [], "
     "\"load_snippet\": \"...\", \"notes\": \"...\"}}}}"),
    ("human", "{plan_json}")
])

def research_dataset(plan_json: dict) -> dict:
    llm = get_llm()
    res = (_research | llm).invoke({"plan_json": str(plan_json)}).content
    print(f"Research agent response: {res}")  # Debug output
    
    import json, re
    try:
        return json.loads(res)
    except Exception as e:
        print(f"Research JSON parse error: {e}")
        # Try to extract JSON
        try:
            m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", res, re.S)
            if m:
                json_str = m.group(0)
                print(f"Extracted research JSON: {json_str}")
                return json.loads(json_str)
        except Exception as e2:
            print(f"Research fallback JSON parse error: {e2}")
        
        # Final fallback
        return {
            "dataset": {
                "name": "Telco Customer Churn",
                "hf_id": "kaggle/telco-customer-churn",
                "task": "binary_classification",
                "target": "Churn",
                "features": ["categorical", "numerical"],
                "load_snippet": "datasets.load_dataset('kaggle/telco-customer-churn')",
                "notes": "Public dataset for churn prediction"
            },
            "raw_response": res
        }
