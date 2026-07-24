import time
from dataclasses import dataclass, field
from typing import List

@dataclass
class RouteStep:
    capability: str
    executor_name: str

@dataclass 
class Route:
    id: str
    steps: List[RouteStep]
    success_rate: float = 0.0
    avg_duration: float = 0.0
    total_executions: int = 0
    score: float = 0.0
    last_used: float = field(default_factory=time.time)
    
    def compute_score(self, freshness_decay: float = 0.95) -> float:
        confidence = min(1.0, self.total_executions / 10.0)
        age_days = (time.time() - self.last_used) / 86400
        freshness = freshness_decay ** age_days
        self.score = self.success_rate * confidence * freshness
        return self.score
        
    @property
    def signature(self) -> str:
        return "->".join(f"{s.capability}:{s.executor_name}" for s in self.steps)
