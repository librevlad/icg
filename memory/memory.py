from typing import List, Dict, Optional
from .history import History
from .metrics import Metrics
from .experience import Experience
from .knowledge import Knowledge

class Memory:
    def __init__(self, db_path: str = "icg_memory.db"):
        self.history = History(db_path)
        self.metrics = Metrics(db_path)
        self.knowledge = Knowledge(db_path)
        self._experiences: List[Experience] = []
        
    def append(self, experience: Experience):
        self._experiences.append(experience)
        self.knowledge.update(experience)
        
    def query(self, capability: str = None, executor: str = None) -> List[Experience]:
        return [
            e for e in self._experiences 
            if (capability is None or e.capability == capability) and 
               (executor is None or e.executor_name == executor)
        ]
        
    def summarize(self) -> Dict:
        return {
            "total_experiences": len(self._experiences),
            "knowledge": self.knowledge.get_all_stats()
        }
        
    def compact(self):
        self._experiences.clear()
