from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.prompt_schema import PromptCreate, PromptResponse
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.agents.planner_agent import PlannerAgent
from typing import List, Optional

class PlannerService:
    def __init__(self, db: Session):
        self.db = db
        self.planner_agent = PlannerAgent()

    async def create_prompt(self, prompt: PromptCreate) -> PromptResponse:
        """Create a new prompt and trigger planning"""
        # Create project record
        project = Project(
            prompt=prompt.prompt,
            status="planning"
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        
        # Trigger planner agent
        plan = await self.planner_agent.plan(prompt.prompt)
        
        return PromptResponse(
            id=project.id,
            prompt=prompt.prompt,
            status=project.status,
            plan=plan
        )

    async def get_prompts(self, skip: int = 0, limit: int = 100) -> List[PromptResponse]:
        """Get all prompts"""
        projects = self.db.query(Project).offset(skip).limit(limit).all()
        return [PromptResponse.from_orm(project) for project in projects]

    async def get_prompt(self, prompt_id: int) -> PromptResponse:
        """Get a specific prompt"""
        project = self.db.query(Project).filter(Project.id == prompt_id).first()
        if not project:
            raise ValueError("Prompt not found")
        return PromptResponse.from_orm(project)

    async def trigger_planner(self, trigger: AgentTrigger) -> AgentResponse:
        """Trigger the planner agent"""
        result = await self.planner_agent.plan(trigger.prompt)
        return AgentResponse(
            agent_type="planner",
            status="completed",
            result=result
        ) 