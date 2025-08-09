from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.prompt_schema import PromptCreate, PromptResponse
from app.services.planner_service import PlannerService
from typing import List

router = APIRouter()

@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt: PromptCreate,
    db: Session = Depends(get_db)
):
    """Submit a new prompt for processing"""
    planner_service = PlannerService(db)
    return await planner_service.create_prompt(prompt)

@router.get("/", response_model=List[PromptResponse])
async def get_prompts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all prompts"""
    planner_service = PlannerService(db)
    return await planner_service.get_prompts(skip=skip, limit=limit)

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prompt by ID"""
    planner_service = PlannerService(db)
    return await planner_service.get_prompt(prompt_id) 