"""
Agent Manager for ByteBreaker
"""
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

class AgentManager:
    """Manage autonomous agents"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.agents = {}
        self.active_tasks = []
    
    def register_agent(self, name: str, agent_class, *args, **kwargs) -> None:
        """Register an agent"""
        try:
            agent = agent_class(*args, **kwargs)
            self.agents[name] = agent
            self.logger.info(f"Agent registered: {name}")
        except Exception as e:
            self.logger.error(f"Failed to register agent {name}: {e}")
    
    async def start_agent(self, name: str, *args, **kwargs) -> Dict[str, Any]:
        """Start an agent task"""
        if name not in self.agents:
            raise ValueError(f"Agent {name} not registered")
        
        agent = self.agents[name]
        
        try:
            task = asyncio.create_task(agent.monitor_target(*args, **kwargs))
            self.active_tasks.append({
                "agent": name,
                "task": task,
                "started_at": datetime.now().isoformat()
            })
            
            return {"status": "started", "agent": name}
        except Exception as e:
            self.logger.error(f"Failed to start agent {name}: {e}")
            return {"status": "error", "error": str(e)}
    
    async def stop_agent(self, name: str) -> Dict[str, Any]:
        """Stop an agent task"""
        for task_info in self.active_tasks:
            if task_info["agent"] == name:
                task_info["task"].cancel()
                self.active_tasks.remove(task_info)
                return {"status": "stopped", "agent": name}
        
        return {"status": "not_found", "agent": name}
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "registered_agents": list(self.agents.keys()),
            "active_tasks": [
                {
                    "agent": t["agent"],
                    "started_at": t["started_at"]
                }
                for t in self.active_tasks
            ]
        }
