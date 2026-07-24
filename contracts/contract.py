import time
from dataclasses import dataclass, field
from typing import Dict, List, Any
from core.types import ContractStatus

@dataclass
class Contract:
    id: str
    task_description: str
    requires: List[str]
    constraints: Dict[str, Any] = field(default_factory=dict)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    acceptance_criteria: List[str] = field(default_factory=list)
    workspace: str = ""
    status: ContractStatus = ContractStatus.CREATED
    created_at: float = field(default_factory=time.time)

    def validate(self) -> bool:
        if not self.id or not self.task_description or not self.requires:
            return False
        return True

    def set_status(self, new_status: ContractStatus):
        valid_transitions = {
            ContractStatus.CREATED: [ContractStatus.RUNNING],
            ContractStatus.RUNNING: [ContractStatus.COMPLETED, ContractStatus.FAILED],
            ContractStatus.COMPLETED: [],
            ContractStatus.FAILED: []
        }
        if new_status in valid_transitions[self.status]:
            self.status = new_status
        else:
            raise ValueError(f"Invalid transition from {self.status} to {new_status}")
