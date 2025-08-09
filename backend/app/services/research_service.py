from sqlalchemy.orm import Session
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.agents.research_agent import ResearchAgent
from typing import List, Optional

class ResearchService:
    def __init__(self, db: Session):
        self.db = db
        self.research_agent = ResearchAgent()

    async def trigger_research(self, trigger: AgentTrigger) -> AgentResponse:
        """Trigger the research agent"""
        result = await self.research_agent.research(trigger.prompt)
        return AgentResponse(
            agent_type="research",
            status="completed",
            result=result
        )

    async def search_web(self, query: str) -> dict:
        """Search the web for information"""
        return await self.research_agent.search_web(query)

    async def search_dataset(self, query: str) -> dict:
        """Search the dataset for information"""
        return await self.research_agent.search_dataset(query) 