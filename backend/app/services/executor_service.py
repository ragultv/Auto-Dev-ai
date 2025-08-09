from sqlalchemy.orm import Session
from app.schemas.execution_schema import ExecutionCreate, ExecutionResponse
from app.models.execution import Execution
from app.utils.docker_utils import DockerUtils
from typing import List, Optional

class ExecutorService:
    def __init__(self, db: Session):
        self.db = db
        self.docker_utils = DockerUtils()

    async def create_execution(self, execution: ExecutionCreate) -> ExecutionResponse:
        """Create a new execution"""
        db_execution = Execution(
            project_id=execution.project_id,
            status="created",
            code=execution.code
        )
        self.db.add(db_execution)
        self.db.commit()
        self.db.refresh(db_execution)
        return ExecutionResponse.from_orm(db_execution)

    async def get_executions(self, skip: int = 0, limit: int = 100) -> List[ExecutionResponse]:
        """Get all executions"""
        executions = self.db.query(Execution).offset(skip).limit(limit).all()
        return [ExecutionResponse.from_orm(execution) for execution in executions]

    async def get_execution(self, execution_id: int) -> ExecutionResponse:
        """Get a specific execution"""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            raise ValueError("Execution not found")
        return ExecutionResponse.from_orm(execution)

    async def start_execution(self, execution_id: int) -> dict:
        """Start an execution"""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            raise ValueError("Execution not found")
        
        # Start Docker container
        container_id = await self.docker_utils.start_container(execution.code)
        
        # Update execution status
        execution.status = "running"
        execution.container_id = container_id
        self.db.commit()
        
        return {"status": "started", "container_id": container_id}

    async def stop_execution(self, execution_id: int) -> dict:
        """Stop an execution"""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            raise ValueError("Execution not found")
        
        # Stop Docker container
        if execution.container_id:
            await self.docker_utils.stop_container(execution.container_id)
        
        # Update execution status
        execution.status = "stopped"
        self.db.commit()
        
        return {"status": "stopped"} 