import uuid
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any

class EventType(Enum):
    CONTRACT_CREATED = "CONTRACT_CREATED"
    CONTRACT_STARTED = "CONTRACT_STARTED"
    CONTRACT_COMPLETED = "CONTRACT_COMPLETED"
    CONTRACT_FAILED = "CONTRACT_FAILED"
    NODE_STARTED = "NODE_STARTED"
    NODE_COMPLETED = "NODE_COMPLETED"
    NODE_FAILED = "NODE_FAILED"
    EXECUTOR_SELECTED = "EXECUTOR_SELECTED"
    EXECUTOR_STARTED = "EXECUTOR_STARTED"
    EXECUTOR_FINISHED = "EXECUTOR_FINISHED"
    PROVIDER_DISCOVERED = "PROVIDER_DISCOVERED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"

@dataclass
class Event:
    type: EventType
    payload: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type.value, "timestamp": self.timestamp, "payload": self.payload}
