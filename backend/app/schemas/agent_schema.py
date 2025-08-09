from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentTrigger(BaseModel):
    prompt: str
    agent_type: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    agent_type: str
    status: str
    result: Dict[str, Any]
    timestamp: Optional[str] = None 