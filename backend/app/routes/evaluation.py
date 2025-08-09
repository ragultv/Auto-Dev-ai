from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.execution_schema import EvaluationResponse
from app.services.evaluator_service import EvaluatorService
from typing import List

router = APIRouter()

@router.get("/{execution_id}/metrics", response_model=EvaluationResponse)
async def get_execution_metrics(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get metrics for a specific execution"""
    evaluator_service = EvaluatorService(db)
    return await evaluator_service.get_execution_metrics(execution_id)

@router.post("/{execution_id}/evaluate")
async def evaluate_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Evaluate an execution"""
    evaluator_service = EvaluatorService(db)
    return await evaluator_service.evaluate_execution(execution_id)

@router.get("/metrics/summary")
async def get_metrics_summary(
    db: Session = Depends(get_db)
):
    """Get overall metrics summary"""
    evaluator_service = EvaluatorService(db)
    return await evaluator_service.get_metrics_summary() 