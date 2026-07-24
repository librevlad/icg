from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List

class ContractStatus(Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ExecutionNodeStatus(Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class ExecutionResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    artifacts: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0
    error_code: Optional[str] = None

@dataclass
class ExecutionContext:
    contract: Any = None
    workspace: Any = None
    results: Dict[str, 'ExecutionResult'] = field(default_factory=dict)
    memory: Any = None
