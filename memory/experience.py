import time
import uuid
from dataclasses import dataclass, field

@dataclass
class Experience:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    contract_id: str = ""
    capability: str = ""
    executor_name: str = ""
    success: bool = False
    duration: float = 0.0
    cost: float = 0.0
    tokens: int = 0
    context_hash: str = ""
    timestamp: float = field(default_factory=time.time)
