from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.services.planner_service import PlannerService
from app.services.research_service import ResearchService
from app.services.coder_service import CoderService
from app.services.tester_service import TesterService
from app.services.evaluator_service import EvaluatorService

router = APIRouter()

@router.post("/planner", response_model=AgentResponse)
async def trigger_planner(
    trigger: AgentTrigger,
    db: Session = Depends(get_db)
):
    """Trigger the planner agent"""
    planner_service = PlannerService(db)
    return await planner_service.trigger_planner(trigger)

@router.post("/research", response_model=AgentResponse)
async def trigger_research(
    trigger: AgentTrigger,
    db: Session = Depends(get_db)
):
    """Trigger the research agent"""
    research_service = ResearchService(db)
    return await research_service.trigger_research(trigger)

@router.post("/coder", response_model=AgentResponse)
async def trigger_coder(
    trigger: AgentTrigger,
    db: Session = Depends(get_db)
):
    """Trigger the coder agent"""
    coder_service = CoderService(db)
    return await coder_service.trigger_coder(trigger)

@router.post("/tester", response_model=AgentResponse)
async def trigger_tester(
    trigger: AgentTrigger,
    db: Session = Depends(get_db)
):
    """Trigger the tester agent"""
    tester_service = TesterService(db)
    return await tester_service.trigger_tester(trigger)

@router.post("/evaluator", response_model=AgentResponse)
async def trigger_evaluator(
    trigger: AgentTrigger,
    db: Session = Depends(get_db)
):
    """Trigger the evaluator agent"""
    evaluator_service = EvaluatorService(db)
    return await evaluator_service.trigger_evaluator(trigger) 