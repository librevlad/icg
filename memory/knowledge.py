from typing import Dict, List, Optional
from .experience import Experience

class Knowledge:
    def __init__(self, db_path: str = "icg_memory.db"):
        self.db_path = db_path
        self._stats: Dict[str, Dict] = {}
        
    def update(self, experience: Experience):
        key = f"{experience.capability}:{experience.executor_name}"
        if key not in self._stats:
            self._stats[key] = {
                "capability": experience.capability,
                "executor": experience.executor_name,
                "success_rate": 0.0,
                "avg_duration": 0.0,
                "total_executions": 0,
                "total_cost": 0.0,
                "last_updated": experience.timestamp
            }
        
        stat = self._stats[key]
        n = stat["total_executions"]
        
        stat["success_rate"] = (stat["success_rate"] * n + (1 if experience.success else 0)) / (n + 1)
        stat["avg_duration"] = (stat["avg_duration"] * n + experience.duration) / (n + 1)
        stat["total_executions"] += 1
        stat["total_cost"] += experience.cost
        stat["last_updated"] = experience.timestamp
        
    def get_stats(self, capability: str, executor: str) -> Optional[Dict]:
        key = f"{capability}:{executor}"
        return self._stats.get(key)
        
    def get_all_stats(self) -> List[Dict]:
        return list(self._stats.values())
