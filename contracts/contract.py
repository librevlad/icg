from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Contract:
    """
    Contract represents a declarative plan of execution.
    It defines what needs to be done, what capabilities are required,
    and what the constraints and acceptance criteria are.
    """
    id: str
    task_description: str
    requires: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    acceptance_criteria: List[str] = field(default_factory=list)
