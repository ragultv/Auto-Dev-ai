from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ExecutionCreate(BaseModel):
    project_id: int
    code: Optional[str] = None

class ExecutionResponse(BaseModel):
    id: int
    project_id: int
    status: str
    code: Optional[str] = None
    container_id: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationResponse(BaseModel):
    execution_id: int
    metrics: Dict[str, Any] 