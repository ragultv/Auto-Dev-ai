from core.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Master Agent. Given a user's ML/DL/DA request, "
     "if you got any prompt related to deep learning model,transformers, response i only support for machine learning models"
     "sklearn is your core"
     "produce a concrete plan with these steps: "
     "1) Research dataset & task details, 2) Generate training code "
     "(with metrics + Gradio UI), 3) Execute, 4) If error → Debug loop, "
     "5) Evaluate & summarize. Return ONLY a valid JSON object with these exact fields: "
     "`problem`, `dataset_requirements`, `model_family`, `metrics`, `notes`. "
     "Do not include any explanatory text before or after the JSON."),
    ("human", "{user_prompt}")
])

def master_plan(user_prompt: str) -> dict:
    llm = get_llm()
    res = (_prompt | llm).invoke({"user_prompt": user_prompt}).content
    print(f"Raw LLM response: {res}")  # Debug output
    
    # Be tolerant: model may return JSON-like text; try safe eval
    import json, re
    try:
        return json.loads(res)
    except Exception as e:
        print(f"JSON parse error: {e}")
        # Try to extract just the JSON part
        try:
            # Look for JSON between curly braces
            m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", res, re.S)
            if m:
                json_str = m.group(0)
                print(f"Extracted JSON: {json_str}")
                return json.loads(json_str)
        except Exception as e2:
            print(f"Fallback JSON parse error: {e2}")
        
        # Final fallback - return a structured response
        return {
            "problem": "Binary churn prediction",
            "dataset_requirements": "Public tabular dataset with churn labels",
            "model_family": "Classification (Random Forest, Logistic Regression, etc.)",
            "metrics": ["accuracy", "F1-score"],
            "notes": "Build interactive UI with Gradio",
            "raw_plan": res
        }
