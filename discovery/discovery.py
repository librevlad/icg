from typing import List
from providers.registry import CapabilityRegistry
from providers.provider import Provider

class DiscoveryService:
    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
        
    def discover(self) -> List[Provider]:
        # MVP: simply returns registered providers
        return self.registry.get_all()
