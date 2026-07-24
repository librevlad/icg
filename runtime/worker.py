from abc import ABC, abstractmethod
from contracts.contract import Contract
from core.types import ExecutionResult

class Worker(ABC):
    @abstractmethod
    def execute(self, contract: Contract) -> ExecutionResult:
        pass
