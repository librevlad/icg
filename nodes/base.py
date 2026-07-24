from abc import ABC, abstractmethod
from typing import Any
from contracts.contract import Contract
from workspace.workspace import Workspace

class Node(ABC):
    """
    Node is an executor in the ICG network. 
    It can be an LLM CLI (Gemini), a local tool (Bash), or any other compute primitive.
    """

    @abstractmethod
    def run(self, capability: str, contract: Contract, workspace: Workspace) -> Any:
        """
        Executes the contract based on the requested capability.
        
        Args:
            capability: The specific capability requested from this Node (e.g. "reasoning", "coding").
            contract: The Contract declarative plan.
            workspace: The context representing the filesystem/repository state.
            
        Returns:
            The execution result (outputs, logs, success status, etc.)
        """
        pass
