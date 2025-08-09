from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.execution_schema import ExecutionCreate, ExecutionResponse
from app.services.executor_service import ExecutorService
from typing import List

router = APIRouter()

@router.post("/", response_model=ExecutionResponse)
async def create_execution(
    execution: ExecutionCreate,
    db: Session = Depends(get_db)
):
    """Create a new execution"""
    executor_service = ExecutorService(db)
    return await executor_service.create_execution(execution)

@router.get("/", response_model=List[ExecutionResponse])
async def get_executions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all executions"""
    executor_service = ExecutorService(db)
    return await executor_service.get_executions(skip=skip, limit=limit)

@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific execution by ID"""
    executor_service = ExecutorService(db)
    return await executor_service.get_execution(execution_id)

@router.post("/{execution_id}/start")
async def start_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Start an execution"""
    executor_service = ExecutorService(db)
    return await executor_service.start_execution(execution_id)

@router.post("/{execution_id}/stop")
async def stop_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Stop an execution"""
    executor_service = ExecutorService(db)
    return await executor_service.stop_execution(execution_id) 