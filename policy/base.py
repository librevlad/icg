from abc import ABC, abstractmethod
from typing import List
from executors.base import Executor
from core.types import ExecutionContext

class ExecutionPolicy(ABC):
    @abstractmethod
    def select(self, capability: str, candidates: List[Executor], context: ExecutionContext) -> Executor:
        pass
