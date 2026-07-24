from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from core.types import ExecutionNodeStatus, ExecutionResult

@dataclass
class ExecutionNode:
    id: str
    capability: str
    dependencies: List[str] = field(default_factory=list)
    status: ExecutionNodeStatus = ExecutionNodeStatus.PENDING
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    result: Optional[ExecutionResult] = None
