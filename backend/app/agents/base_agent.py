from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
    
    @abstractmethod
    async def execute(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    async def validate_input(self, prompt: str) -> bool:
        """Validate input prompt"""
        if not prompt or not prompt.strip():
            return False
        return True
    
    async def log_execution(self, prompt: str, result: Dict[str, Any]):
        """Log execution details"""
        self.logger.info(f"Agent {self.name} executed with prompt: {prompt[:100]}...")
        self.logger.debug(f"Result: {result}")
    
    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors during execution"""
        self.logger.error(f"Error in agent {self.name}: {str(error)}")
        return {
            "status": "error",
            "error": str(error),
            "agent": self.name
        } 