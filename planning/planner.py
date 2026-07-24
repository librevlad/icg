from abc import ABC, abstractmethod
from contracts.contract import Contract
from .execution_graph import ExecutionGraph

class Planner(ABC):
    @abstractmethod
    def plan(self, contract: Contract) -> ExecutionGraph:
        pass
