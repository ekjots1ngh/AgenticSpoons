"""
Base Agent Class
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any
import time
from loguru import logger

class BaseAgent(ABC):
    """Base class for all agents in AgentSpoons"""
    
    def __init__(self, agent_id: str, wallet_address: str = ""):
        self.agent_id = agent_id
        self.wallet_address = wallet_address
        self.is_running = False
        self.last_execution = 0
        self.execution_interval = 60  # Default: 60 seconds
        
        logger.info(f"Initialized {self.agent_id}")
    
    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Main execution logic - must be implemented by subclasses"""
        pass
    
    async def run(self):
        """Run agent in continuous loop"""
        self.is_running = True
        logger.info(f"[{self.agent_id}] Starting agent loop...")
        
        while self.is_running:
            try:
                current_time = time.time()
                
                if current_time - self.last_execution >= self.execution_interval:
                    logger.debug(f"[{self.agent_id}] Executing...")
                    result = await self.execute()
                    self.last_execution = current_time
                    
                    logger.success(f"[{self.agent_id}] ✓ {result.get('status', 'completed')}")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Stop the agent"""
        self.is_running = False
        logger.info(f"[{self.agent_id}] Stopping...")
