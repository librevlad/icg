from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ProviderManifest:
    id: str
    version: str
    capabilities: List[str]
    config: Dict = field(default_factory=dict)
