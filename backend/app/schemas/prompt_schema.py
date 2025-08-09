from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PromptCreate(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    id: int
    prompt: str
    status: str
    plan: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 