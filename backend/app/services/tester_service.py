from sqlalchemy.orm import Session
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.agents.tester_agent import TesterAgent
from typing import List, Optional

class TesterService:
    def __init__(self, db: Session):
        self.db = db
        self.tester_agent = TesterAgent()

    async def trigger_tester(self, trigger: AgentTrigger) -> AgentResponse:
        """Trigger the tester agent"""
        result = await self.tester_agent.test_code(trigger.prompt)
        return AgentResponse(
            agent_type="tester",
            status="completed",
            result=result
        )

    async def run_unit_tests(self, code: str) -> dict:
        """Run unit tests on code"""
        return await self.tester_agent.run_unit_tests(code)

    async def retry_failed_tests(self, test_results: dict) -> dict:
        """Retry failed tests"""
        return await self.tester_agent.retry_failed_tests(test_results) 