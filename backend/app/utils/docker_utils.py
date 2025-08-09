import docker
import asyncio
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DockerUtils:
    def __init__(self):
        self.client = docker.from_env()
    
    async def start_container(self, code: str) -> str:
        """Start a Docker container with the given code"""
        try:
            # Create a temporary Dockerfile
            dockerfile_content = f"""
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
"""
            
            # Create container
            container = self.client.containers.run(
                "python:3.9-slim",
                command="python -c 'print(\"Hello from container\")'",
                detach=True,
                remove=True
            )
            
            logger.info(f"Started container: {container.id}")
            return container.id
            
        except Exception as e:
            logger.error(f"Error starting container: {e}")
            raise
    
    async def stop_container(self, container_id: str) -> bool:
        """Stop a Docker container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            logger.info(f"Stopped container: {container_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping container {container_id}: {e}")
            return False
    
    async def get_container_status(self, container_id: str) -> Dict[str, Any]:
        """Get the status of a container"""
        try:
            container = self.client.containers.get(container_id)
            return {
                "id": container.id,
                "status": container.status,
                "logs": container.logs().decode()
            }
            
        except Exception as e:
            logger.error(f"Error getting container status {container_id}: {e}")
            return {"error": str(e)} 