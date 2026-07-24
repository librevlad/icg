from abc import ABC, abstractmethod
from typing import List
from contracts.contract import Contract
from workspace.workspace import Workspace
from core.types import ExecutionResult

class Executor(ABC):
    @abstractmethod
    def capabilities(self) -> List[str]:
        pass

    @abstractmethod
    def run(self, contract: Contract, workspace: Workspace) -> ExecutionResult:
        pass
