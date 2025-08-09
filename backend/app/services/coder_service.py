from sqlalchemy.orm import Session
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.agents.coder_agent import CoderAgent
from typing import List, Optional

class CoderService:
    def __init__(self, db: Session):
        self.db = db
        self.coder_agent = CoderAgent()

    async def trigger_coder(self, trigger: AgentTrigger) -> AgentResponse:
        """Trigger the coder agent"""
        result = await self.coder_agent.generate_code(trigger.prompt)
        return AgentResponse(
            agent_type="coder",
            status="completed",
            result=result
        )

    async def generate_ml_code(self, requirements: str) -> dict:
        """Generate ML/DL code"""
        return await self.coder_agent.generate_ml_code(requirements)

    async def generate_dl_code(self, requirements: str) -> dict:
        """Generate deep learning code"""
        return await self.coder_agent.generate_dl_code(requirements) 