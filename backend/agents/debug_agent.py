from core.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate

_debug = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Debug Agent. Given the original Python training script and the execution error logs, "
     "return a corrected full script. Keep same responsibilities (train, metrics, save artifacts, write ui_spec.json and model_entry.py). "
     "Return ONLY code."),
    ("human", "Original code:\n```python\n{code}\n```\n\nError logs:\n```\n{error}\n```")
])

def rewrite_on_error(original_code: str, error: str) -> str:
    llm = get_llm()
    response = (_debug | llm).invoke({"code": original_code, "error": error}).content
    
    # Clean up markdown formatting more aggressively
    import re
    
    # Remove all markdown code blocks
    code = re.sub(r'```python\s*', '', response)
    code = re.sub(r'```\s*', '', code)
    
    return code.strip()
