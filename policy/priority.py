from typing import List
from policy.base import ExecutionPolicy
from executors.base import Executor
from core.types import ExecutionContext

class PriorityPolicy(ExecutionPolicy):
    def select(self, capability: str, candidates: List[Executor], context: ExecutionContext) -> Executor:
        if not candidates:
            raise ValueError(f"No candidates provided for {capability}")
        return candidates[0]
