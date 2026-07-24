from typing import Dict, List
from .provider import Provider

class CapabilityRegistry:
    def __init__(self):
        self._providers: Dict[str, Provider] = {}
        
    def register(self, name: str, provider: Provider):
        self._providers[name] = provider
        
    def get_all(self) -> List[Provider]:
        return list(self._providers.values())
