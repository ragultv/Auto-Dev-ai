from sqlalchemy.orm import Session
from app.schemas.agent_schema import AgentTrigger, AgentResponse
from app.schemas.execution_schema import EvaluationResponse
from app.agents.evaluator_agent import EvaluatorAgent
from app.models.execution import Execution
from typing import List, Optional

class EvaluatorService:
    def __init__(self, db: Session):
        self.db = db
        self.evaluator_agent = EvaluatorAgent()

    async def trigger_evaluator(self, trigger: AgentTrigger) -> AgentResponse:
        """Trigger the evaluator agent"""
        result = await self.evaluator_agent.evaluate(trigger.prompt)
        return AgentResponse(
            agent_type="evaluator",
            status="completed",
            result=result
        )

    async def get_execution_metrics(self, execution_id: int) -> EvaluationResponse:
        """Get metrics for a specific execution"""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            raise ValueError("Execution not found")
        
        metrics = await self.evaluator_agent.calculate_metrics(execution)
        return EvaluationResponse(
            execution_id=execution_id,
            metrics=metrics
        )

    async def evaluate_execution(self, execution_id: int) -> dict:
        """Evaluate an execution"""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            raise ValueError("Execution not found")
        
        evaluation = await self.evaluator_agent.evaluate_execution(execution)
        return evaluation

    async def get_metrics_summary(self) -> dict:
        """Get overall metrics summary"""
        executions = self.db.query(Execution).all()
        summary = await self.evaluator_agent.calculate_summary_metrics(executions)
        return summary 