import time
import psutil
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MetricsUtils:
    def __init__(self):
        self.start_time = None
    
    def start_timer(self):
        """Start a timer"""
        self.start_time = time.time()
    
    def stop_timer(self) -> float:
        """Stop the timer and return elapsed time"""
        if self.start_time is None:
            return 0.0
        elapsed = time.time() - self.start_time
        self.start_time = None
        return elapsed
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_io": psutil.net_io_counters()._asdict()
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    async def calculate_performance_metrics(self, execution_time: float, memory_usage: float) -> Dict[str, Any]:
        """Calculate performance metrics"""
        return {
            "execution_time": execution_time,
            "memory_usage": memory_usage,
            "performance_score": self._calculate_score(execution_time, memory_usage)
        }
    
    def _calculate_score(self, execution_time: float, memory_usage: float) -> float:
        """Calculate a performance score"""
        # Simple scoring algorithm
        time_score = max(0, 100 - (execution_time * 10))
        memory_score = max(0, 100 - memory_usage)
        return (time_score + memory_score) / 2 