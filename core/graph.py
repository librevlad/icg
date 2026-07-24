from typing import Dict, List
from executors.base import Executor

class CapabilityGraph:
    def __init__(self):
        self._executors: Dict[str, List[Executor]] = {}

    def register_executor(self, executor: Executor):
        for cap in executor.capabilities():
            if cap not in self._executors:
                self._executors[cap] = []
            if executor not in self._executors[cap]:
                self._executors[cap].append(executor)

    def resolve(self, capability: str) -> List[Executor]:
        executors = self._executors.get(capability, [])
        if not executors:
            raise ValueError(f"No executors found for capability: {capability}")
        return executors

    def unregister(self, executor: Executor):
        for cap in list(self._executors.keys()):
            if executor in self._executors[cap]:
                self._executors[cap].remove(executor)
            if not self._executors[cap]:
                del self._executors[cap]

    def capabilities(self) -> List[str]:
        return list(self._executors.keys())

    def has_capability(self, capability: str) -> bool:
        return capability in self._executors
